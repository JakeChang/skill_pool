#!/usr/bin/env python3
"""
技能快速驗證腳本 - 精簡版
"""

import sys
import os
import re
import yaml
from pathlib import Path

def validate_skill(skill_path):
    """技能基本驗證"""
    skill_path = Path(skill_path)

    # 檢查 SKILL.md 是否存在
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return False, "找不到 SKILL.md"

    # 讀取並驗證 frontmatter
    content = skill_md.read_text()
    if not content.startswith('---'):
        return False, "找不到 YAML frontmatter"

    # 擷取 frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "frontmatter 格式無效"

    frontmatter_text = match.group(1)

    # 解析 YAML frontmatter
    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        if not isinstance(frontmatter, dict):
            return False, "frontmatter 必須是 YAML 字典"
    except yaml.YAMLError as e:
        return False, f"frontmatter 中的 YAML 無效：{e}"

    # 定義允許的屬性
    ALLOWED_PROPERTIES = {'name', 'description', 'license', 'allowed-tools', 'metadata'}

    # 檢查是否有非預期的屬性（排除 metadata 下的巢狀鍵）
    unexpected_keys = set(frontmatter.keys()) - ALLOWED_PROPERTIES
    if unexpected_keys:
        return False, (
            f"SKILL.md frontmatter 中有非預期的鍵：{', '.join(sorted(unexpected_keys))}。"
            f"允許的屬性有：{', '.join(sorted(ALLOWED_PROPERTIES))}"
        )

    # 檢查必要欄位
    if 'name' not in frontmatter:
        return False, "frontmatter 中缺少 'name'"
    if 'description' not in frontmatter:
        return False, "frontmatter 中缺少 'description'"

    # 擷取名稱進行驗證
    name = frontmatter.get('name', '')
    if not isinstance(name, str):
        return False, f"name 必須是字串，但收到 {type(name).__name__}"
    name = name.strip()
    if name:
        # 檢查命名慣例（連字號格式：小寫加連字號）
        if not re.match(r'^[a-z0-9-]+$', name):
            return False, f"名稱 '{name}' 應為連字號格式（僅限小寫字母、數字和連字號）"
        if name.startswith('-') or name.endswith('-') or '--' in name:
            return False, f"名稱 '{name}' 不能以連字號開頭/結尾，也不能包含連續連字號"
        # 檢查名稱長度（規格限制最多 64 字元）
        if len(name) > 64:
            return False, f"名稱太長（{len(name)} 字元）。最多 64 字元。"

    # 擷取並驗證說明
    description = frontmatter.get('description', '')
    if not isinstance(description, str):
        return False, f"description 必須是字串，但收到 {type(description).__name__}"
    description = description.strip()
    if description:
        # 檢查角括號
        if '<' in description or '>' in description:
            return False, "說明不能包含角括號（< 或 >）"
        # 檢查說明長度（規格限制最多 1024 字元）
        if len(description) > 1024:
            return False, f"說明太長（{len(description)} 字元）。最多 1024 字元。"

    return True, "技能驗證通過！"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法：python quick_validate.py <skill_directory>")
        sys.exit(1)

    valid, message = validate_skill(sys.argv[1])
    print(message)
    sys.exit(0 if valid else 1)
