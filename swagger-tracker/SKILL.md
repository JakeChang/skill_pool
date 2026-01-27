---
name: swagger-tracker
description: |
  Swagger/OpenAPI 文件追蹤與版本比較工具。自動抓取遠端 Swagger JSON，轉換成易讀的 Markdown 格式（包含 API、輸入參數、回傳結構、錯誤碼四大區塊），並支援版本間差異比較。

  使用時機：
  (1) 需要抓取並儲存 Swagger API 文件時
  (2) 需要比較兩個版本的 API 差異時
  (3) 需要追蹤 API 變更（新增、修改、刪除）時
  (4) 需要將 OpenAPI 規格轉換成易讀文件時

  觸發詞：swagger、openapi、api 文件、api 追蹤、api 比較、api 版本
---

# Swagger Tracker

追蹤並比較 Swagger/OpenAPI 文件的版本變更。

## 功能

1. **抓取 API 文件** - 從遠端 URL 抓取 Swagger JSON 並轉換成結構化格式
2. **自動版本管理** - 檔名格式：`{專案名稱}-{日期}`（如 `bistro-backend-service-20260121`）
3. **自動差異比較** - 重複執行同一指令時，自動與既有版本比較並產生差異報告

## 資料儲存位置

所有 API 文件儲存在專案根目錄的 `swagger-docs/` 資料夾：

- `swagger-docs/{專案名稱}-{日期}.json` - 結構化 JSON（供比較用）
- `swagger-docs/{專案名稱}-{日期}.md` - 易讀的 Markdown 文件
- `swagger-docs/diff-{舊版本}-vs-{新版本}.md` - 版本差異報告（有變更時產生）

## 用法

```bash
mkdir -p swagger-docs
python scripts/fetch_swagger.py <swagger_json_url> swagger-docs
```

**參數：**
- `swagger_json_url` - Swagger JSON 的 URL（通常是 `/api-json` 或 `/swagger.json`）
- `swagger-docs` - 輸出至 swagger-docs 資料夾

**Markdown 包含四大區塊：**
1. **API** - 路徑、方法、摘要、描述
2. **輸入參數** - 名稱、位置、必填、類型、說明
3. **回傳結構** - 各狀態碼的回應 schema
4. **錯誤碼** - 4xx/5xx 錯誤碼說明

## 自動比較機制

重複執行相同指令時：
- 自動偵測既有版本
- 比較 API 差異
- 若無變更，顯示「無變更」
- 若有變更，儲存新版本並產生差異報告 `diff-{舊版本}-vs-{新版本}.md`

**追蹤的變更類型：**
- 🆕 新增的 API
- 🗑️ 刪除的 API
- ✏️ 修改的 API（名稱、參數、回傳結構、錯誤碼）

### update - 更新此技能

更新本機的 swagger-tracker skill 到最新版本。

```bash
npx openskills update
```

## 範例

```bash
# 首次抓取（或追蹤變更，同一個指令）
# 檔案會儲存在 swagger-docs 資料夾
mkdir -p swagger-docs
python scripts/fetch_swagger.py https://bistro-backend-dev.gomore.net/api-json swagger-docs
```

**首次執行輸出：**
```
swagger-docs/bistro-backend-service-20260121.json
swagger-docs/bistro-backend-service-20260121.md
```

**再次執行（有變更時）輸出：**
```
swagger-docs/bistro-backend-service-20260122.json
swagger-docs/bistro-backend-service-20260122.md
swagger-docs/diff-bistro-backend-service-20260121-vs-bistro-backend-service-20260122.md
```

## 常見 Swagger JSON URL

- NestJS (Swagger UI): `/api-json`
- Spring Boot: `/v3/api-docs` 或 `/swagger.json`
- FastAPI: `/openapi.json`

若只知道 Swagger UI 頁面（如 `/api#/`），嘗試將 `#/` 改為 `-json`。
