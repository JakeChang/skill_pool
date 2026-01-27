#!/usr/bin/env python3
"""
Swagger API 文件抓取、儲存與自動比較腳本

用法:
    python fetch_swagger.py <swagger_json_url> <output_dir>

範例:
    python fetch_swagger.py https://api.example.com/api-json ./api-docs

功能:
    - 自動從 API title 產生檔名（專案名稱-日期）
    - 自動偵測已存在的版本並進行比較
    - 若有變更，產生差異報告
"""

import json
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path
from typing import Any


def fetch_swagger(url: str) -> dict:
    """從 URL 抓取 Swagger JSON"""
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.URLError as e:
        print(f"錯誤：無法連接到 {url}")
        print(f"詳細資訊：{e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"錯誤：無法解析 JSON 回應")
        print(f"詳細資訊：{e}")
        sys.exit(1)


def slugify(text: str) -> str:
    """將文字轉換成適合檔名的格式"""
    # 移除特殊字元，保留中英文、數字、空格和連字號
    text = re.sub(r'[^\w\s\-\u4e00-\u9fff]', '', text)
    # 將空格轉換成連字號
    text = re.sub(r'\s+', '-', text.strip())
    # 移除連續的連字號
    text = re.sub(r'-+', '-', text)
    return text.lower()


def extract_error_codes(responses: dict) -> list[dict]:
    """從回應中提取錯誤碼"""
    error_codes = []
    for status_code, response_info in responses.items():
        if status_code.startswith(('4', '5')) or status_code == 'default':
            error_codes.append({
                'code': status_code,
                'description': response_info.get('description', ''),
            })
    return error_codes


# 全域變數儲存 schemas 供展開 $ref 使用
_schemas: dict = {}


def extract_schema(obj: dict) -> dict | None:
    """提取 schema 結構"""
    if 'content' in obj:
        for content_type, content_info in obj['content'].items():
            if 'schema' in content_info:
                return resolve_schema(content_info['schema'])
    if 'schema' in obj:
        return resolve_schema(obj['schema'])
    return None


def resolve_schema(schema: dict, depth: int = 0, visited: set | None = None) -> dict:
    """解析 schema，展開 $ref 引用"""
    if depth > 15:
        return {'type': 'object', 'note': '...'}

    if visited is None:
        visited = set()

    if '$ref' in schema:
        ref_path = schema['$ref']
        ref_name = ref_path.split('/')[-1]

        # 防止循環引用
        if ref_name in visited:
            return {'type': 'object', 'note': f'(circular: {ref_name})'}

        # 展開引用
        if ref_name in _schemas:
            visited = visited | {ref_name}
            return resolve_schema(_schemas[ref_name], depth + 1, visited)

        return {'$ref': ref_name}

    if schema.get('type') == 'array' and 'items' in schema:
        return {
            'type': 'array',
            'items': resolve_schema(schema['items'], depth + 1, visited)
        }

    if 'allOf' in schema:
        # 合併 allOf 中的所有 properties
        merged_props = {}
        merged_required = []
        for item in schema['allOf']:
            resolved = resolve_schema(item, depth + 1, visited)
            if 'properties' in resolved:
                merged_props.update(resolved['properties'])
            if 'required' in resolved:
                merged_required.extend(resolved['required'])
        result = {'type': 'object', 'properties': merged_props}
        if merged_required:
            result['required'] = sorted(set(merged_required))
        return result

    if 'oneOf' in schema:
        return {'oneOf': [resolve_schema(s, depth + 1, visited) for s in schema['oneOf']]}

    if 'anyOf' in schema:
        return {'anyOf': [resolve_schema(s, depth + 1, visited) for s in schema['anyOf']]}

    # 處理 object 的 properties
    if schema.get('type') == 'object' and 'properties' in schema:
        resolved_props = {}
        for prop_name, prop_schema in schema['properties'].items():
            resolved_props[prop_name] = resolve_schema(prop_schema, depth + 1, visited)
        result = {'type': 'object', 'properties': resolved_props}
        if 'required' in schema:
            result['required'] = sorted(schema['required'])
        return result

    return schema


def extract_parameters(parameters: list) -> list[dict]:
    """提取參數資訊"""
    params = []
    for param in parameters:
        param_info = {
            'name': param.get('name', ''),
            'in': param.get('in', ''),
            'required': param.get('required', False),
            'description': param.get('description', ''),
        }
        if 'schema' in param:
            param_info['schema'] = resolve_schema(param['schema'])
        params.append(param_info)
    return params


def extract_request_body(request_body: dict) -> dict | None:
    """提取請求體資訊"""
    if not request_body:
        return None

    body_info = {
        'required': request_body.get('required', False),
        'description': request_body.get('description', ''),
        'content': {}
    }

    for content_type, content_info in request_body.get('content', {}).items():
        body_info['content'][content_type] = {
            'schema': resolve_schema(content_info.get('schema', {}))
        }

    return body_info


def extract_responses(responses: dict) -> dict:
    """提取回應資訊"""
    result = {}
    for status_code, response_info in responses.items():
        result[status_code] = {
            'description': response_info.get('description', ''),
            'schema': extract_schema(response_info)
        }
    return result


def parse_swagger(swagger_data: dict) -> dict:
    """解析 Swagger 文件並轉換成結構化格式（不含 schemas）"""
    global _schemas

    # 載入 schemas 供展開 $ref 使用
    components = swagger_data.get('components', {})
    if 'schemas' in components:
        _schemas = components['schemas']
    elif 'definitions' in swagger_data:  # Swagger 2.0
        _schemas = swagger_data['definitions']
    else:
        _schemas = {}

    info = swagger_data.get('info', {})

    apis = []
    paths = swagger_data.get('paths', {})

    for path, path_info in paths.items():
        for method, operation in path_info.items():
            if method in ['get', 'post', 'put', 'patch', 'delete', 'options', 'head']:
                api_entry = {
                    'path': path,
                    'method': method.upper(),
                    'operationId': operation.get('operationId', ''),
                    'summary': operation.get('summary', ''),
                    'description': operation.get('description', ''),
                    'tags': operation.get('tags', []),
                    'parameters': extract_parameters(operation.get('parameters', [])),
                    'requestBody': extract_request_body(operation.get('requestBody')),
                    'responses': extract_responses(operation.get('responses', {})),
                    'errorCodes': extract_error_codes(operation.get('responses', {})),
                    'deprecated': operation.get('deprecated', False),
                    'security': operation.get('security', [])
                }
                apis.append(api_entry)

    return {
        'info': {
            'title': info.get('title', ''),
            'version': info.get('version', ''),
            'description': info.get('description', '')
        },
        'servers': swagger_data.get('servers', []),
        'apis': apis,
        'fetchedAt': datetime.now().isoformat()
    }


def schema_to_example(schema: dict) -> Any:
    """將 schema 轉換成只有欄位名稱和範例值的簡化結構"""
    if not schema or not isinstance(schema, dict):
        return None

    schema_type = schema.get('type', '')

    # 有 example 就直接用
    if 'example' in schema:
        return schema['example']

    # 處理 oneOf / anyOf - 取第一個
    if 'oneOf' in schema and schema['oneOf']:
        return schema_to_example(schema['oneOf'][0])
    if 'anyOf' in schema and schema['anyOf']:
        return schema_to_example(schema['anyOf'][0])

    # 處理 object
    if schema_type == 'object' and 'properties' in schema:
        result = {}
        for prop_name, prop_schema in schema['properties'].items():
            result[prop_name] = schema_to_example(prop_schema)
        return result

    # 處理 array
    if schema_type == 'array' and 'items' in schema:
        item_example = schema_to_example(schema['items'])
        return [item_example] if item_example is not None else []

    # 簡單類型的預設值
    if schema_type == 'string':
        if schema.get('format') == 'date-time':
            return "2024-01-01T00:00:00Z"
        if schema.get('enum'):
            return schema['enum'][0]
        return ""
    if schema_type == 'number' or schema_type == 'integer':
        return 0
    if schema_type == 'boolean':
        return False

    return None


def format_schema_json(schema: dict) -> str:
    """將 schema 轉換成簡化的 JSON 字串"""
    example = schema_to_example(schema)
    if example is not None:
        return json.dumps(example, indent=2, ensure_ascii=False)
    return ''


def generate_anchor_id(method: str, path: str) -> str:
    """產生標準化的錨點 ID"""
    # 移除開頭的 /，將其他 / 和特殊字元轉成 -
    anchor = f"{method.lower()}-{path.lstrip('/').replace('/', '-').replace('{', '').replace('}', '')}"
    # 移除連續的連字號
    while '--' in anchor:
        anchor = anchor.replace('--', '-')
    return anchor


def format_api_markdown(api: dict) -> str:
    """將單一 API 格式化為 Markdown"""
    lines = []

    anchor_id = generate_anchor_id(api['method'], api['path'])
    deprecated_mark = ' ⚠️ DEPRECATED' if api['deprecated'] else ''
    lines.append(f"<a id=\"{anchor_id}\"></a>")
    lines.append("")
    lines.append(f"### {api['method']} `{api['path']}`{deprecated_mark}")
    lines.append("")

    if api['summary']:
        lines.append(f"**{api['summary']}**")
        lines.append("")

    if api['description']:
        lines.append(api['description'])
        lines.append("")

    if api['tags']:
        lines.append(f"**Tags:** {', '.join(api['tags'])}")
        lines.append("")

    # 輸入參數
    lines.append("#### 輸入參數")
    lines.append("")

    if api['parameters']:
        lines.append("| 名稱 | 位置 | 必填 | 類型 | 說明 |")
        lines.append("|------|------|------|------|------|")
        for param in api['parameters']:
            required = '✓' if param['required'] else ''
            param_type = ''
            if 'schema' in param:
                schema = param['schema']
                if isinstance(schema, dict):
                    if '$ref' in schema:
                        param_type = f"`{schema['$ref']}`"
                    else:
                        param_type = schema.get('type', '')
                        if schema.get('format'):
                            param_type += f" ({schema['format']})"
            lines.append(f"| {param['name']} | {param['in']} | {required} | {param_type} | {param['description']} |")
        lines.append("")
    else:
        lines.append("無路徑/查詢參數")
        lines.append("")

    # Request Body
    if api['requestBody']:
        lines.append("**Request Body:**")
        lines.append("")
        if api['requestBody']['required']:
            lines.append("*必填*")
        if api['requestBody']['description']:
            lines.append(api['requestBody']['description'])
        lines.append("")
        for content_type, content_info in api['requestBody']['content'].items():
            lines.append(f"Content-Type: `{content_type}`")
            lines.append("")
            schema_json = format_schema_json(content_info['schema'])
            if schema_json:
                lines.append("```json")
                lines.append(schema_json)
                lines.append("```")
                lines.append("")

    # 回傳結構
    lines.append("#### 回傳結構")
    lines.append("")

    for status_code, response in api['responses'].items():
        if not status_code.startswith(('4', '5')):
            lines.append(f"**{status_code}**: {response['description']}")
            lines.append("")
            if response['schema']:
                schema_json = format_schema_json(response['schema'])
                if schema_json:
                    lines.append("```json")
                    lines.append(schema_json)
                    lines.append("```")
                    lines.append("")

    # 錯誤碼
    lines.append("#### 錯誤碼")
    lines.append("")

    if api['errorCodes']:
        lines.append("| 狀態碼 | 說明 |")
        lines.append("|--------|------|")
        for error in api['errorCodes']:
            lines.append(f"| {error['code']} | {error['description']} |")
        lines.append("")
    else:
        lines.append("無特定錯誤碼定義")
        lines.append("")

    lines.append("---")
    lines.append("")

    return '\n'.join(lines)


def format_full_markdown(parsed_data: dict, filename: str) -> str:
    """將完整解析結果格式化為 Markdown"""
    lines = []

    info = parsed_data['info']
    lines.append(f"# {info['title']}")
    lines.append("")
    lines.append(f"**檔案:** {filename}")
    lines.append(f"**API 版本:** {info['version']}")
    lines.append(f"**抓取時間:** {parsed_data['fetchedAt']}")
    lines.append("")

    if info['description']:
        lines.append(info['description'])
        lines.append("")

    if parsed_data['servers']:
        lines.append("## 伺服器")
        lines.append("")
        for server in parsed_data['servers']:
            lines.append(f"- {server.get('url', '')} - {server.get('description', '')}")
        lines.append("")

    # API 目錄
    lines.append("## API 目錄")
    lines.append("")

    apis_by_tag: dict[str, list] = {}
    for api in parsed_data['apis']:
        tags = api['tags'] if api['tags'] else ['其他']
        for tag in tags:
            if tag not in apis_by_tag:
                apis_by_tag[tag] = []
            apis_by_tag[tag].append(api)

    for tag in sorted(apis_by_tag.keys()):
        lines.append(f"### {tag}")
        lines.append("")
        for api in apis_by_tag[tag]:
            anchor_id = generate_anchor_id(api['method'], api['path'])
            lines.append(f"- [{api['method']} {api['path']}](#{anchor_id})")
        lines.append("")

    # API 詳細資訊
    lines.append("## API 詳細資訊")
    lines.append("")

    for tag in sorted(apis_by_tag.keys()):
        lines.append(f"## {tag}")
        lines.append("")
        for api in apis_by_tag[tag]:
            lines.append(format_api_markdown(api))

    return '\n'.join(lines)


# ============ 比較功能 ============

def get_api_key(api: dict) -> str:
    """產生 API 的唯一識別 key"""
    return f"{api['method']}:{api['path']}"


def build_api_index(apis: list) -> dict[str, dict]:
    """建立 API 索引"""
    return {get_api_key(api): api for api in apis}


def compare_parameters(old_params: list, new_params: list) -> dict | None:
    """比較參數差異"""
    old_map = {p['name']: p for p in old_params}
    new_map = {p['name']: p for p in new_params}

    added = [p for name, p in new_map.items() if name not in old_map]
    removed = [p for name, p in old_map.items() if name not in new_map]
    modified = []

    for name in set(old_map.keys()) & set(new_map.keys()):
        old_p = old_map[name]
        new_p = new_map[name]
        if json.dumps(old_p, sort_keys=True) != json.dumps(new_p, sort_keys=True):
            modified.append({'name': name, 'old': old_p, 'new': new_p})

    if added or removed or modified:
        return {'added': added, 'removed': removed, 'modified': modified}
    return None


def compare_request_body(old_body: dict | None, new_body: dict | None) -> dict | None:
    """比較 Request Body 差異"""
    if old_body is None and new_body is None:
        return None
    if old_body is None:
        return {'change': 'added', 'new': new_body}
    if new_body is None:
        return {'change': 'removed', 'old': old_body}

    if json.dumps(old_body, sort_keys=True) != json.dumps(new_body, sort_keys=True):
        return {'change': 'modified', 'old': old_body, 'new': new_body}
    return None


def compare_responses(old_resp: dict, new_resp: dict) -> dict | None:
    """比較回應差異，分開處理 description 和 schema"""
    old_keys = set(old_resp.keys())
    new_keys = set(new_resp.keys())

    added = {k: new_resp[k] for k in new_keys - old_keys}
    removed = {k: old_resp[k] for k in old_keys - new_keys}
    modified = {}

    for key in old_keys & new_keys:
        old_item = old_resp[key]
        new_item = new_resp[key]

        # 分開比較 schema 和 description
        old_schema = old_item.get('schema')
        new_schema = new_item.get('schema')
        old_desc = old_item.get('description', '')
        new_desc = new_item.get('description', '')

        schema_changed = json.dumps(old_schema, sort_keys=True) != json.dumps(new_schema, sort_keys=True)
        desc_changed = old_desc != new_desc

        if schema_changed or desc_changed:
            modified[key] = {
                'old': old_item,
                'new': new_item,
                'schema_changed': schema_changed,
                'desc_changed': desc_changed
            }

    if added or removed or modified:
        return {'added': added, 'removed': removed, 'modified': modified}
    return None


def compare_api(old_api: dict, new_api: dict) -> dict | None:
    """比較單一 API 的差異"""
    changes = {}

    if old_api.get('summary') != new_api.get('summary'):
        changes['summary'] = {'old': old_api.get('summary'), 'new': new_api.get('summary')}

    if old_api.get('description') != new_api.get('description'):
        changes['description'] = {'old': old_api.get('description'), 'new': new_api.get('description')}

    if old_api.get('deprecated') != new_api.get('deprecated'):
        changes['deprecated'] = {'old': old_api.get('deprecated', False), 'new': new_api.get('deprecated', False)}

    param_diff = compare_parameters(old_api.get('parameters', []), new_api.get('parameters', []))
    if param_diff:
        changes['parameters'] = param_diff

    body_diff = compare_request_body(old_api.get('requestBody'), new_api.get('requestBody'))
    if body_diff:
        changes['requestBody'] = body_diff

    resp_diff = compare_responses(old_api.get('responses', {}), new_api.get('responses', {}))
    if resp_diff:
        changes['responses'] = resp_diff

    old_errors = {e['code']: e for e in old_api.get('errorCodes', [])}
    new_errors = {e['code']: e for e in new_api.get('errorCodes', [])}
    if old_errors != new_errors:
        changes['errorCodes'] = {'old': old_api.get('errorCodes', []), 'new': new_api.get('errorCodes', [])}

    return changes if changes else None


def compare_versions(old_data: dict, new_data: dict) -> dict:
    """比較兩個版本的差異"""
    old_index = build_api_index(old_data.get('apis', []))
    new_index = build_api_index(new_data.get('apis', []))

    old_keys = set(old_index.keys())
    new_keys = set(new_index.keys())

    added_apis = [new_index[k] for k in new_keys - old_keys]
    removed_apis = [old_index[k] for k in old_keys - new_keys]

    modified_apis = []
    for key in old_keys & new_keys:
        diff = compare_api(old_index[key], new_index[key])
        if diff:
            modified_apis.append({'api': new_index[key], 'changes': diff})

    return {
        'added': added_apis,
        'removed': removed_apis,
        'modified': modified_apis,
        'summary': {
            'added_count': len(added_apis),
            'removed_count': len(removed_apis),
            'modified_count': len(modified_apis)
        }
    }


def format_diff_markdown(diff: dict, old_filename: str, new_filename: str) -> str:
    """將差異格式化為 Markdown"""
    lines = []

    lines.append(f"# API 變更報告")
    lines.append("")
    lines.append(f"**比較版本:** {old_filename} → {new_filename}")
    lines.append(f"**產生時間:** {datetime.now().isoformat()}")
    lines.append("")

    summary = diff['summary']
    lines.append("## 變更摘要")
    lines.append("")
    lines.append(f"| 類型 | 數量 |")
    lines.append(f"|------|------|")
    lines.append(f"| 🆕 新增 API | {summary['added_count']} |")
    lines.append(f"| 🗑️ 刪除 API | {summary['removed_count']} |")
    lines.append(f"| ✏️ 修改 API | {summary['modified_count']} |")
    lines.append("")

    # API 目錄
    lines.append("## 變更 API 目錄")
    lines.append("")

    if diff['added']:
        lines.append("### 🆕 新增的 API")
        lines.append("")
        for api in diff['added']:
            anchor_id = generate_anchor_id(api['method'], api['path'])
            lines.append(f"- [{api['method']} {api['path']}](#{anchor_id})")
        lines.append("")

    if diff['removed']:
        lines.append("### 🗑️ 刪除的 API")
        lines.append("")
        for api in diff['removed']:
            lines.append(f"- ~~{api['method']} {api['path']}~~ - {api.get('summary', '')}")
        lines.append("")

    if diff['modified']:
        lines.append("### ✏️ 修改的 API")
        lines.append("")

        # 為每個 API 產生變更標記，並按類別分組
        categorized = {}
        for item in diff['modified']:
            api = item['api']
            changes = item['changes']
            anchor_id = generate_anchor_id(api['method'], api['path'])

            # 產生變更標記
            tags = []
            if 'summary' in changes or 'description' in changes:
                tags.append('描述')
            if 'deprecated' in changes:
                tags.append('Deprecated')
            if 'parameters' in changes:
                tags.append('參數')
            if 'requestBody' in changes:
                tags.append('RequestBody')
            if 'responses' in changes:
                # 檢查是否有 schema 變更
                resp_changes = changes['responses']
                has_schema_change = any(
                    v.get('schema_changed', True)
                    for v in resp_changes.get('modified', {}).values()
                )
                if resp_changes.get('added') or resp_changes.get('removed') or has_schema_change:
                    tags.append('回傳')
            if 'errorCodes' in changes:
                tags.append('錯誤碼')

            # 用 tags 組合作為分類 key
            category_key = ', '.join(tags) if tags else '其他'
            if category_key not in categorized:
                categorized[category_key] = []
            categorized[category_key].append({
                'api': api,
                'anchor_id': anchor_id,
                'tags': tags
            })

        # 按類別輸出，優先顯示變更較多的類別
        for category_key in sorted(categorized.keys(), key=lambda k: (-len(k.split(', ')), k)):
            items = categorized[category_key]
            lines.append(f"**`[{category_key}]`** ({len(items)} 個)")
            lines.append("")
            for item in items:
                lines.append(f"- [{item['api']['method']} {item['api']['path']}](#{item['anchor_id']})")
            lines.append("")

    # 新增的 API 詳細資訊
    if diff['added']:
        lines.append("## 🆕 新增的 API")
        lines.append("")
        for api in diff['added']:
            anchor_id = generate_anchor_id(api['method'], api['path'])
            lines.append(f"<a id=\"{anchor_id}\"></a>")
            lines.append("")
            lines.append(f"### {api['method']} `{api['path']}`")
            lines.append("")
            if api.get('summary'):
                lines.append(f"**{api['summary']}**")
                lines.append("")
            if api.get('tags'):
                lines.append(f"**Tags:** {', '.join(api['tags'])}")
                lines.append("")

            lines.append("#### 輸入參數")
            lines.append("")
            if api.get('parameters'):
                lines.append("| 名稱 | 位置 | 必填 | 說明 |")
                lines.append("|------|------|------|------|")
                for param in api['parameters']:
                    required = '✓' if param.get('required') else ''
                    lines.append(f"| {param['name']} | {param['in']} | {required} | {param.get('description', '')} |")
                lines.append("")
            else:
                lines.append("無")
                lines.append("")

            if api.get('requestBody'):
                lines.append("**Request Body:**")
                lines.append("```json")
                lines.append(json.dumps(api['requestBody'], indent=2, ensure_ascii=False))
                lines.append("```")
                lines.append("")

            lines.append("#### 回傳結構")
            lines.append("")
            for status, resp in api.get('responses', {}).items():
                if not status.startswith(('4', '5')):
                    lines.append(f"**{status}**: {resp.get('description', '')}")
                    if resp.get('schema'):
                        lines.append("```json")
                        lines.append(json.dumps(resp['schema'], indent=2, ensure_ascii=False))
                        lines.append("```")
                    lines.append("")

            lines.append("#### 錯誤碼")
            lines.append("")
            if api.get('errorCodes'):
                lines.append("| 狀態碼 | 說明 |")
                lines.append("|--------|------|")
                for err in api['errorCodes']:
                    lines.append(f"| {err['code']} | {err.get('description', '')} |")
                lines.append("")
            else:
                lines.append("無特定錯誤碼")
                lines.append("")

            lines.append("---")
            lines.append("")

    # 刪除的 API
    if diff['removed']:
        lines.append("## 🗑️ 刪除的 API")
        lines.append("")
        for api in diff['removed']:
            lines.append(f"- ~~{api['method']} `{api['path']}`~~ - {api.get('summary', '')}")
        lines.append("")

    # 修改的 API
    if diff['modified']:
        lines.append("## ✏️ 修改的 API")
        lines.append("")
        for item in diff['modified']:
            api = item['api']
            changes = item['changes']

            anchor_id = generate_anchor_id(api['method'], api['path'])
            lines.append(f"<a id=\"{anchor_id}\"></a>")
            lines.append("")
            lines.append(f"### {api['method']} `{api['path']}`")
            lines.append("")

            if 'summary' in changes:
                lines.append(f"**Summary 變更:**")
                lines.append(f"- 舊: {changes['summary']['old']}")
                lines.append(f"- 新: {changes['summary']['new']}")
                lines.append("")

            if 'deprecated' in changes:
                if changes['deprecated']['new']:
                    lines.append("⚠️ **此 API 已被標記為 Deprecated**")
                else:
                    lines.append("✅ **此 API 已取消 Deprecated 標記**")
                lines.append("")

            if 'parameters' in changes:
                lines.append("#### 輸入參數變更")
                lines.append("")
                param_changes = changes['parameters']
                if param_changes.get('added'):
                    lines.append("**🆕 新增參數:**")
                    lines.append("")
                    lines.append("| 名稱 | 位置 | 必填 | 類型 | 說明 |")
                    lines.append("|------|------|------|------|------|")
                    for p in param_changes['added']:
                        required = '✓' if p.get('required') else ''
                        param_type = ''
                        if 'schema' in p and isinstance(p['schema'], dict):
                            param_type = p['schema'].get('type', '')
                        lines.append(f"| {p['name']} | {p['in']} | {required} | {param_type} | {p.get('description', '')} |")
                    lines.append("")
                if param_changes.get('removed'):
                    lines.append("**🗑️ 移除參數:**")
                    lines.append("")
                    lines.append("| 名稱 | 位置 | 說明 |")
                    lines.append("|------|------|------|")
                    for p in param_changes['removed']:
                        lines.append(f"| ~~{p['name']}~~ | {p['in']} | {p.get('description', '')} |")
                    lines.append("")
                if param_changes.get('modified'):
                    lines.append("**✏️ 修改參數:**")
                    lines.append("")
                    for p in param_changes['modified']:
                        lines.append(f"**`{p['name']}`**")
                        lines.append("")
                        lines.append("舊:")
                        lines.append("```json")
                        lines.append(json.dumps(p['old'], indent=2, ensure_ascii=False))
                        lines.append("```")
                        lines.append("")
                        lines.append("新:")
                        lines.append("```json")
                        lines.append(json.dumps(p['new'], indent=2, ensure_ascii=False))
                        lines.append("```")
                        lines.append("")

            if 'requestBody' in changes:
                lines.append("#### Request Body 變更")
                lines.append("")
                rb = changes['requestBody']
                if rb['change'] == 'added':
                    lines.append("**🆕 新增 Request Body:**")
                    lines.append("")
                    for content_type, content_info in rb['new'].get('content', {}).items():
                        lines.append(f"Content-Type: `{content_type}`")
                        lines.append("")
                        schema_json = format_schema_json(content_info.get('schema', {}))
                        if schema_json:
                            lines.append("```json")
                            lines.append(schema_json)
                            lines.append("```")
                            lines.append("")
                elif rb['change'] == 'removed':
                    lines.append("**🗑️ 移除 Request Body**")
                    lines.append("")
                elif rb['change'] == 'modified':
                    # 顯示舊的 Request Body
                    lines.append("**舊 Request Body:**")
                    lines.append("")
                    for content_type, content_info in rb['old'].get('content', {}).items():
                        lines.append(f"Content-Type: `{content_type}`")
                        lines.append("")
                        schema_json = format_schema_json(content_info.get('schema', {}))
                        if schema_json:
                            lines.append("```json")
                            lines.append(schema_json)
                            lines.append("```")
                            lines.append("")
                    # 顯示新的 Request Body
                    lines.append("**新 Request Body:**")
                    lines.append("")
                    for content_type, content_info in rb['new'].get('content', {}).items():
                        lines.append(f"Content-Type: `{content_type}`")
                        lines.append("")
                        schema_json = format_schema_json(content_info.get('schema', {}))
                        if schema_json:
                            lines.append("```json")
                            lines.append(schema_json)
                            lines.append("```")
                            lines.append("")

            if 'responses' in changes:
                resp_changes = changes['responses']
                has_added = bool(resp_changes.get('added'))
                has_removed = bool(resp_changes.get('removed'))
                # 過濾出真正有 schema 變更的回應
                schema_modified = {k: v for k, v in resp_changes.get('modified', {}).items()
                                   if v.get('schema_changed', True)}

                # 只有在有實質變更時才顯示標題
                if has_added or has_removed or schema_modified:
                    lines.append("#### 回傳結構變更")
                    lines.append("")

                    if has_added:
                        lines.append("**🆕 新增回應:**")
                        lines.append("")
                        for code, resp in resp_changes['added'].items():
                            lines.append(f"**{code}**: {resp.get('description', '')}")
                            lines.append("")
                            if resp.get('schema'):
                                schema_json = format_schema_json(resp['schema'])
                                if schema_json:
                                    lines.append("```json")
                                    lines.append(schema_json)
                                    lines.append("```")
                                    lines.append("")

                    if has_removed:
                        lines.append("**🗑️ 移除回應:**")
                        lines.append("")
                        for code, resp in resp_changes['removed'].items():
                            lines.append(f"- ~~`{code}`~~ - {resp.get('description', '')}")
                        lines.append("")

                    if schema_modified:
                        lines.append("**✏️ 修改回應:**")
                        lines.append("")
                        for code, resp in schema_modified.items():
                            lines.append(f"**{code}**")
                            lines.append("")
                            # 舊的回應
                            lines.append("舊:")
                            lines.append("")
                            if resp['old'].get('schema'):
                                schema_json = format_schema_json(resp['old']['schema'])
                                if schema_json:
                                    lines.append("```json")
                                    lines.append(schema_json)
                                    lines.append("```")
                                    lines.append("")
                            # 新的回應
                            lines.append("新:")
                            lines.append("")
                            if resp['new'].get('schema'):
                                schema_json = format_schema_json(resp['new']['schema'])
                                if schema_json:
                                    lines.append("```json")
                                    lines.append(schema_json)
                                    lines.append("```")
                                    lines.append("")

            if 'errorCodes' in changes:
                lines.append("#### 錯誤碼變更")
                lines.append("")
                old_errors = changes['errorCodes']['old']
                new_errors = changes['errorCodes']['new']
                old_codes = {e['code']: e for e in old_errors}
                new_codes = {e['code']: e for e in new_errors}

                # 新增的錯誤碼
                added_codes = [e for e in new_errors if e['code'] not in old_codes]
                # 移除的錯誤碼
                removed_codes = [e for e in old_errors if e['code'] not in new_codes]
                # 修改的錯誤碼
                modified_codes = [(old_codes[e['code']], e) for e in new_errors
                                  if e['code'] in old_codes and old_codes[e['code']] != e]

                if added_codes:
                    lines.append("**🆕 新增錯誤碼:**")
                    lines.append("")
                    lines.append("| 狀態碼 | 說明 |")
                    lines.append("|--------|------|")
                    for err in added_codes:
                        lines.append(f"| {err['code']} | {err.get('description', '')} |")
                    lines.append("")

                if removed_codes:
                    lines.append("**🗑️ 移除錯誤碼:**")
                    lines.append("")
                    lines.append("| 狀態碼 | 說明 |")
                    lines.append("|--------|------|")
                    for err in removed_codes:
                        lines.append(f"| ~~{err['code']}~~ | {err.get('description', '')} |")
                    lines.append("")

                if modified_codes:
                    lines.append("**✏️ 修改錯誤碼:**")
                    lines.append("")
                    lines.append("| 狀態碼 | 舊說明 | 新說明 |")
                    lines.append("|--------|--------|--------|")
                    for old_err, new_err in modified_codes:
                        lines.append(f"| {new_err['code']} | {old_err.get('description', '')} | {new_err.get('description', '')} |")
                    lines.append("")

            lines.append("---")
            lines.append("")

    return '\n'.join(lines)


def find_latest_version(output_dir: Path, project_slug: str) -> Path | None:
    """找到最新的版本檔案"""
    pattern = f"{project_slug}-*.json"
    files = sorted(output_dir.glob(pattern), reverse=True)
    return files[0] if files else None


def save_outputs(parsed_data: dict, output_dir: Path, filename: str):
    """儲存輸出檔案"""
    output_dir.mkdir(parents=True, exist_ok=True)

    # 儲存 JSON（供比較用）
    json_file = output_dir / f"{filename}.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(parsed_data, f, indent=2, ensure_ascii=False)
    print(f"✅ 已儲存 JSON: {json_file}")

    # 儲存 Markdown
    md_file = output_dir / f"{filename}.md"
    md_content = format_full_markdown(parsed_data, filename)
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(md_content)
    print(f"✅ 已儲存 Markdown: {md_file}")

    return json_file, md_file


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    url = sys.argv[1]
    output_dir = Path(sys.argv[2])

    print(f"🔄 正在抓取 Swagger 文件: {url}")
    swagger_data = fetch_swagger(url)

    print(f"📝 正在解析 API 結構...")
    parsed_data = parse_swagger(swagger_data)

    # 產生檔名：專案名稱-日期
    project_title = parsed_data['info']['title'] or 'api'
    project_slug = slugify(project_title)
    date_str = datetime.now().strftime('%Y%m%d')
    filename = f"{project_slug}-{date_str}"

    print(f"📊 統計:")
    print(f"   - API 數量: {len(parsed_data['apis'])}")

    # 檢查是否有既有版本
    latest_file = find_latest_version(output_dir, project_slug)

    if latest_file:
        print(f"\n🔍 發現既有版本: {latest_file.name}")

        # 載入舊版本
        with open(latest_file, 'r', encoding='utf-8') as f:
            old_data = json.load(f)

        # 比較差異
        diff = compare_versions(old_data, parsed_data)
        summary = diff['summary']

        total_changes = summary['added_count'] + summary['removed_count'] + summary['modified_count']

        if total_changes == 0:
            print(f"✅ 無變更，與 {latest_file.name} 相同")
            return

        print(f"\n📊 發現變更:")
        print(f"   - 新增 API: {summary['added_count']}")
        print(f"   - 刪除 API: {summary['removed_count']}")
        print(f"   - 修改 API: {summary['modified_count']}")

        # 儲存新版本
        print(f"\n💾 正在儲存新版本: {filename}")
        save_outputs(parsed_data, output_dir, filename)

        # 儲存差異報告
        old_filename = latest_file.stem
        diff_file = output_dir / f"diff-{old_filename}-vs-{filename}.md"
        diff_content = format_diff_markdown(diff, old_filename, filename)
        with open(diff_file, 'w', encoding='utf-8') as f:
            f.write(diff_content)
        print(f"✅ 已儲存差異報告: {diff_file}")

    else:
        print(f"\n💾 首次儲存: {filename}")
        save_outputs(parsed_data, output_dir, filename)


if __name__ == '__main__':
    main()
