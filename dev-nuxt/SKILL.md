---
name: dev-nuxt
description: Nuxt 模組化開發技能。當需要：(1) 規劃 Nuxt 專案功能需求、(2) 撰寫開發計劃書、(3) 新增功能模組（composable、service、頁面元件）、(4) 撰寫測試、(5) 檢查程式碼是否符合架構規範時使用。適用於任何 Nuxt 4 專案，遵循四層式架構（Pages → Composables → Services → Utils）。
---

# Nuxt 模組化開發

適用於任何 Nuxt 4 專案的模組化開發技能，涵蓋需求規劃、計劃書撰寫、模組開發與測試。

遵循四層式架構：

```
Pages → Composables → Services → Utils
路由/佈局   狀態管理/業務邏輯   客戶端 CRUD 操作   純函式工具
```

依賴規則：上層可依賴下層，下層不可依賴上層。

## 為什麼要模組化

模組化設計讓 AI 輔助開發更高效。AI 工具受限於 context window，**單一檔案超過 1000 行時，AI 的理解力與修改精準度會顯著下降**。

模組化的核心原則：

- **每個檔案控制在 300 行以內**，最多不超過 1000 行
- **單一職責**：一個檔案只做一件事，composable 過大時依功能拆分（Form、Table、Event 等）
- **明確邊界**：透過四層架構劃定責任範圍，檔案間透過 import/export 溝通
- **可獨立理解**：任何一個檔案都能在不讀其他檔案的情況下被理解其用途

這不只對 AI 有益——小檔案更容易 code review、更容易測試、更容易多人協作。

架構細節與模組建立模式請見 [references/architecture.md](references/architecture.md)。
Nuxt 最佳實踐（SSR、hydration、效能等）請見 [references/best-practices.md](references/best-practices.md)。

---

## 指令

### `/dev-nuxt plan`

分析使用者需求，產出功能需求清單。

**流程：**

1. 與使用者確認功能範圍，釐清以下問題：
   - 這個功能要解決什麼問題？
   - 使用者角色與操作流程是什麼？
   - 需要哪些資料欄位？
   - 是否需要權限控管？
   - 是否有外部 API 整合？

2. 產出需求清單，格式：

```markdown
# {功能名稱} 需求規劃

## 目標
簡述功能目的與解決的問題。

## 使用者故事
- 作為 {角色}，我希望能 {操作}，以便 {目的}

## 功能範圍
- [ ] 功能項目 1
- [ ] 功能項目 2
- ...

## 資料模型
| 欄位 | 型別 | 必填 | 說明 |
|------|------|------|------|

## 頁面清單
| 路徑 | 用途 |
|------|------|

## 相依模組
列出需要整合的現有模組或外部服務。

## 不包含
明確列出此次不做的項目，避免範圍蔓延。
```

3. 將需求文件儲存至專案中：`docs/requirements/{module-name}.md`

---

### `/dev-nuxt spec`

基於需求清單，撰寫技術計劃書。

**前置條件：** 已有需求文件（手動撰寫或透過 `/dev-nuxt plan` 產出）。

**流程：**

1. 讀取需求文件
2. 閱讀專案現有結構，了解已有的 service、composable、元件
3. 產出計劃書，格式：

```markdown
# {功能名稱} 技術計劃書

## 概要
基於 {需求文件路徑} 的技術實作方案。

## 模組複雜度評估
- 類型：簡單 / 中等 / 複雜
- 預估 composable 數量：N 個
- 預估頁面數量：N 個

## 檔案清單

### Service 層
| 檔案 | 用途 |
|------|------|
| `app/service/{module}Service.ts` | 客戶端 CRUD（$fetch） |

### Composable 層
| 檔案 | 用途 |
|------|------|
| `app/composables/{module}/use{Module}.ts` | 主邏輯 |
| `app/composables/{module}/index.ts` | Barrel export |

### 頁面層
| 檔案 | 用途 |
|------|------|
| `app/pages/{module}/index.vue` | 列表頁 |

### 元件
| 檔案 | 用途 |
|------|------|

## 實作順序
1. Service 層（API 介接）
2. Composable 層（業務邏輯）
3. 頁面與元件（UI）
4. 路由與導航設定
5. 權限設定（如需要）

## 可複用的現有資源
列出專案中已有的、可直接使用的 service / composable / 元件。

## 測試計劃
- [ ] Service 層單元測試
- [ ] Composable 層單元測試
- [ ] 頁面整合測試
```

4. 將計劃書儲存至：`docs/specs/{module-name}.md`

---

### `/dev-nuxt dev`

依照四層架構新增功能模組。

**前置條件：** 已有計劃書（手動撰寫或透過 `/dev-nuxt spec` 產出）。無計劃書時，先快速確認模組範圍再開發。

**流程：**

1. 讀取計劃書（如有）
2. 依照架構參考文件 [references/architecture.md](references/architecture.md) 的模式，按順序建立：
   - **Service 層** → **Composable 層** → **頁面與元件** → **路由/權限設定**
3. 每完成一層，簡要回報進度
4. 開發完成後執行型別檢查確認無誤：
   ```bash
   npx nuxi typecheck
   ```
   不需要執行 `npm run dev`，型別檢查通過即可。
5. 列出所有新增/修改的檔案

先從 `use{Module}.ts` + `index.ts` 開始，功能增長時再拆分。複雜度判斷與拆分策略見 [references/architecture.md](references/architecture.md)。

---

### `/dev-nuxt review`

檢查模組程式碼是否符合四層式架構規範。

**用法：** `/dev-nuxt review` 或 `/dev-nuxt review {module-name}`

**流程：**

1. 執行型別檢查，確認編譯無誤（不需要 `npm run dev`）：
   ```bash
   npx nuxi typecheck
   ```
2. 掃描專案的 `app/` 目錄結構
3. 針對以下規則逐一檢查：

#### 依賴方向檢查

違規：下層依賴上層。

| 被檢查的層 | 不應出現的 import |
|------------|-------------------|
| `service/*.ts` | `~/composables/`、`~/pages/` |
| `utils/*.ts` | `~/composables/`、`~/service/`、`~/pages/` |
| `composables/**/*.ts` | `~/pages/` |

#### 檔案命名檢查

| 類型 | 規範 | 違規範例 |
|------|------|----------|
| Service | `{module}Service.ts` | `order.ts`、`OrderService.ts` |
| Composable | `use{Module}.ts` | `order.ts`、`UseOrder.ts` |
| 頁面元件 | `PascalCase.vue` | `order-table.vue` |
| Utils | `{name}Utils.ts` | `format.ts` |

#### 結構完整性檢查

- Composable 目錄是否有 `index.ts`（barrel export）
- Service 匯出是否為物件（非 class）
- 型別定義是否放在正確位置（API 型別在 service，UI 型別在 composable）

#### 檔案大小檢查

- **警告**：超過 300 行的檔案，建議拆分
- **嚴重**：超過 1000 行的檔案，必須拆分（AI 工具在超過此限制時理解力與精準度顯著下降）

#### Nuxt 最佳實踐檢查

依據 [references/best-practices.md](references/best-practices.md) 檢查：

- 頁面初始資料是否使用 `useFetch` / `useAsyncData`（而非 `onMounted` + `$fetch`）
- 是否有瀏覽器 API（`window`、`document`、`localStorage`）在 SSR 路徑中被呼叫
- 敏感資訊（API key、token）是否只在 `server/` 目錄下使用
- 內部連結是否使用 `NuxtLink`（而非 `<a>`）
- `definePageMeta` 與 `useHead` / `useSeoMeta` 是否正確分工
- 狀態管理是否 request-safe（使用 `useState` 而非模組層級變數）

#### Composable 品質檢查

- 是否有統一回應格式（`{ success, error }`）
- 表單 composable 是否包含 `validate`、`save`、`resetForm`
- 是否有錯誤處理（try/catch）

#### 程式碼內容檢查

逐一讀取模組內的 `.ts` 和 `.vue` 檔案，檢查以下項目：

**型別安全**
- `any` 濫用：使用 `any` 超過 3 處的檔案標記警告，應改用明確型別或 `unknown`
- 缺少型別定義：函式參數或回傳值未標註型別
- 未使用的 import / 變數

**硬編碼與重複**
- 硬編碼值：直接寫死的 URL、port、magic number，應抽到 `runtimeConfig` 或常數檔
- 重複邏輯：多個 composable 中出現相似的 loading/error 處理模式，應抽取共用

**資訊安全**

XSS：
- `v-html` 渲染未消毒的使用者輸入
- 動態 `:href` / `:src` 可能注入 `javascript:` URL
- 動態元件名稱（`:is`）來自使用者輸入

注入攻擊：
- SQL / NoSQL query 拼接使用者輸入而非參數化查詢
- server route 的 `readBody` / `getQuery` 未做型別驗證與消毒

認證與授權：
- server route 未檢查登入狀態（缺少 session / token 驗證）
- 敏感操作（刪除、修改權限）未檢查使用者角色
- CSRF：狀態變更的 POST/PUT/DELETE 端點未驗證 CSRF token

敏感資料暴露：
- `runtimeConfig.public` 包含不該公開的 API key 或密鑰
- API 回傳過多欄位（password hash、internal ID、token）未用 `pick` / `transform` 過濾
- `console.log` 輸出 token、password 等敏感值
- `.env` 檔案未加入 `.gitignore`

基礎設施安全：
- 登入 / 註冊 / 密碼重設等端點未做 rate limiting
- server route 未設定 CORS 限制（`setResponseHeaders` 或 Nitro config）
- 依賴安全：執行 `npm audit` 檢查已知漏洞套件

**記憶體洩漏**
- `addEventListener` / `setInterval` / `setTimeout` 未在 `onUnmounted` 中清除
- 第三方庫的 `destroy` / `dispose` 未呼叫

**Vue 響應性陷阱**
- 解構 `reactive` 物件導致失去響應性（應用 `toRefs` 或保持物件存取）
- 直接修改 props（應透過 `emit` 通知父元件）

**console 殘留**
- `console.log` / `console.warn` / `console.error` 留在非除錯用途的程式碼中

**無障礙（a11y）**
- `<img>` 缺少 `alt` 屬性
- 互動元素（按鈕、連結）缺少可辨識的文字或 `aria-label`
- 用 `<div>` / `<span>` 做按鈕而非 `<button>`

**效能**
- 不必要的 `reactive`：僅包含單一值時應用 `ref`
- 無效 `computed`：computed 內無響應式依賴，等同普通變數
- 大陣列未用 `shallowRef`：超過 100 項的列表資料建議用 `shallowRef` 減少深度追蹤開銷

4. 產出審查報告：

```markdown
# 審查報告

## 總覽
- 掃描模組數：N
- 問題數：N（嚴重：N / 警告：N）

## 問題清單

### 嚴重（必須修正）
| # | 檔案:行號 | 類別 | 問題 | 說明 |
|---|-----------|------|------|------|

### 警告（建議修正）
| # | 檔案:行號 | 類別 | 問題 | 說明 |
|---|-----------|------|------|------|

## 架構概覽
各模組結構一覽，標示缺少的層或檔案。
```

---

### `/dev-nuxt test`

透過 Chrome 瀏覽器實際操作測試模組功能。

**前置條件：** 模組已開發完成，開發伺服器運行中（`npm run dev`）。

**流程：**

1. 確認開發伺服器已啟動，取得本機網址（預設 `http://localhost:3000`）
2. 使用 Claude in Chrome 瀏覽器工具，依照以下步驟測試：

#### 頁面載入測試
- 開啟模組頁面，確認頁面正常渲染、無 console 錯誤
- 截圖記錄初始狀態

#### CRUD 流程測試
- **Create**：填寫表單 → 送出 → 確認新資料出現在列表
- **Read**：確認列表正確顯示資料、篩選/排序功能正常
- **Update**：點擊編輯 → 修改欄位 → 送出 → 確認更新成功
- **Delete**：刪除資料 → 確認從列表移除

#### UI/UX 驗證
- 確認 DaisyUI 元件樣式正確（按鈕、表單、卡片等）
- 確認 loading 狀態顯示
- 確認錯誤訊息正確顯示
- 確認表單驗證回饋

#### 每步操作
- 使用 `read_console_messages` 檢查是否有錯誤
- 使用 `get_page_text` 或 `read_page` 驗證頁面內容
- 使用 `gif_creator` 錄製操作過程（可選）

3. 產出測試報告，格式：

```markdown
# {模組名稱} 測試報告

## 測試環境
- URL: http://localhost:3000/{module}
- 時間: {timestamp}

## 測試結果
| 測試項目 | 狀態 | 備註 |
|----------|------|------|
| 頁面載入 | PASS/FAIL | |
| 新增資料 | PASS/FAIL | |
| 列表顯示 | PASS/FAIL | |
| 編輯資料 | PASS/FAIL | |
| 刪除資料 | PASS/FAIL | |
| 表單驗證 | PASS/FAIL | |

## Console 錯誤
（如有）

## 發現的問題
（如有）
```
