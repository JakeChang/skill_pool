# Swagger Tracker 使用指南

追蹤並比較 Swagger/OpenAPI 文件的版本變更。

## 安裝

```bash
npx openskills install JakeChang/skill_pool/swagger-tracker
npx openskills sync
```

## 如何觸發此技能

在 Claude Code 對話中使用 `/swagger-tracker` 指令：

```
/swagger-tracker https://api.example.com/api-json
```

```
/swagger-tracker https://api.example.com/swagger.json
```

Claude 會自動抓取 API 文件、儲存並與既有版本比較。

## 使用範例

### 首次抓取 API 文件

**你說：**
> /swagger-tracker https://bistro-backend-dev.gomore.net/api

**Claude 會：**
1. 自動將 `/api` 轉換為 `/api-json`（NestJS 慣例）
2. 抓取並解析 Swagger JSON
3. 產生結構化的 JSON 和易讀的 Markdown 文件

**輸出檔案：**
```
bistro-backend-service-20260121.json
bistro-backend-service-20260121.md
```

### 追蹤版本變更

**你說：**
> /swagger-tracker https://bistro-backend-dev.gomore.net/api

**Claude 會：**
1. 抓取最新的 API 文件
2. 自動與既有版本比較
3. 若有變更，產生差異報告

**輸出範例：**
```
📊 比較結果:
   - 新增 API: 2
   - 刪除 API: 1
   - 修改 API: 5

✅ 已儲存差異報告: diff-bistro-backend-service-20260121-vs-bistro-backend-service-20260122.md
```

### 比較不同環境

**你說：**
> /swagger-tracker https://api-qa.example.com/api-json 請比較 api-service-20260121.json

**Claude 會：**
1. 抓取 QA 環境的 API
2. 與指定的版本進行比較
3. 產生跨環境差異報告

## 差異報告格式

差異報告包含：

1. **變更摘要** - 新增、刪除、修改的 API 數量
2. **變更 API 目錄** - 按變更類型分組，含錨點連結
3. **詳細變更** - 每個 API 的具體變更內容

### 目錄分組範例

```markdown
### ✏️ 修改的 API

**`[RequestBody, 回傳, 錯誤碼]`** (2 個)

- [POST /projects](#post-projects)
- [POST /sales-lead/{id}/convert](#post-sales-lead-id-convert)

**`[RequestBody, 回傳]`** (2 個)

- [POST /clients](#post-clients)
- [PUT /clients/{id}](#put-clients-id)

**`[回傳]`** (4 個)

- [GET /clients/{id}](#get-clients-id)
- [DELETE /clients/{id}](#delete-clients-id)

**`[錯誤碼]`** (19 個)

- [GET /projects](#get-projects)
...
```

### 變更標記說明

| 標記 | 說明 |
|------|------|
| `描述` | Summary 或 Description 變更 |
| `Deprecated` | API 的 Deprecated 狀態變更 |
| `參數` | URL/Query 參數變更 |
| `RequestBody` | Request Body 結構變更 |
| `回傳` | Response Schema 結構變更 |
| `錯誤碼` | 錯誤碼說明變更 |

### 智能比較

- **Schema 與 Description 分開比較**：只有當 Response 的 schema 真正改變時才顯示「回傳結構變更」
- **避免假警報**：錯誤碼說明變更不會觸發「回傳結構變更」
- **穩定輸出**：`required` 欄位排序確保相同 API 每次產生一致的結果

## Markdown 文件格式

產生的 API 文件包含四大區塊：

| 區塊 | 內容 |
|------|------|
| **API 目錄** | 按 Tag 分組的 API 列表，含錨點連結 |
| **輸入參數** | 名稱、位置、必填、類型、說明 |
| **回傳結構** | 各狀態碼的回應 JSON 範例 |
| **錯誤碼** | 4xx/5xx 錯誤碼說明 |

## 更新技能

```
/swagger-tracker update
```

將本機的 swagger-tracker skill 更新到最新版本。

## 常見 Swagger JSON URL

| 框架 | URL 格式 |
|------|----------|
| NestJS | `/api-json` |
| Spring Boot | `/v3/api-docs` 或 `/swagger.json` |
| FastAPI | `/openapi.json` |

> 若只知道 Swagger UI 頁面（如 `/api#/`），嘗試將 `#/` 改為 `-json`。

## 技能結構

```
swagger-tracker/
├── SKILL.md              # 技能定義文件
├── README.md             # 使用指南（本文件）
└── scripts/
    └── fetch_swagger.py  # 抓取與比較腳本
```

## 相關檔案

| 檔案 | 說明 |
|------|------|
| `scripts/fetch_swagger.py` | 抓取 Swagger JSON、解析、比較、產生報告 |
| `SKILL.md` | 技能定義與觸發條件 |

## 輸出檔案說明

| 檔案 | 說明 |
|------|------|
| `{專案名稱}-{日期}.json` | 結構化 JSON（供程式比較用） |
| `{專案名稱}-{日期}.md` | 易讀的 Markdown 文件（含 API 目錄與錨點） |
| `diff-{舊版本}-vs-{新版本}.md` | 版本差異報告（按變更類型分組） |
