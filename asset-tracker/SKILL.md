---
name: asset-tracker
description: |
  個人資產負債管理工具。追蹤銀行帳戶、加密貨幣投資、各類負債，即時查詢最新價格，產生資產淨值報表。

  使用時機：
  (1) 記錄或更新銀行帳戶餘額
  (2) 追蹤加密貨幣持倉與即時價格
  (3) 管理負債（房貸、信貸、車貸等）
  (4) 查看資產淨值與配置分析
  (5) 產生資產報表

  觸發詞：資產管理、asset tracker、財務追蹤、淨資產、加密貨幣
---

# Asset Tracker

個人資產負債管理工具，追蹤你的財務狀況。

## 初始化檢查

**每次執行指令前，先檢查 `asset-tracker/config.json`：**

```
如果 config.json 不存在 → 執行初始化流程
否則 → 執行指令
```

### 初始化流程

使用 `AskUserQuestion` 詢問使用者：

1. **偏好貨幣**：「你偏好的顯示貨幣？」
   - TWD 新台幣（預設）
   - USD 美元
   - 其他

2. **資產類別**：「你想追蹤哪些資產類別？（可多選）」
   - 銀行帳戶
   - 加密貨幣
   - 股票/基金
   - 其他資產

3. **負債類別**：「你有哪些負債需要追蹤？（可多選）」
   - 房貸
   - 信貸
   - 車貸
   - 信用卡
   - 其他負債

建立 config.json 後，再執行原本的指令。

## 資料儲存

**重要：所有資料必須儲存在專案根目錄的 `asset-tracker/` 資料夾內。**

**禁止事項：**
- **絕對禁止** 將任何紀錄或設定檔案寫入 `.claude/` 目錄
- **絕對禁止** 使用 `.claude/memories/`、`.claude/settings/` 或任何 `.claude/` 子目錄
- 如果 `asset-tracker/` 或其子資料夾不存在，請先建立它

**正確的檔案位置：**
- 設定檔：`asset-tracker/config.json`
- 資產紀錄：`asset-tracker/assets.json`
- 負債紀錄：`asset-tracker/liabilities.json`
- 交易紀錄：`asset-tracker/transactions/YYYY-MM.json`（按月份分檔）
- 歷史快照：`asset-tracker/snapshots/YYYY-MM-DD.json`
- 報表輸出：`asset-tracker/reports/`

**交易紀錄說明：**
- 交易紀錄按月份分開存放，避免單一檔案過大
- 檔名格式：`YYYY-MM.json`（如 `2026-01.json`）
- 記錄存款、提款、還款等所有交易明細
- 每個月份檔案包含該月摘要（總存款、總提款、淨現金流）

詳細 JSON 結構請見 [references/schema.md](references/schema.md)。

## 自然語言操作

使用者可以用口語化的方式描述財務變動，系統會自動解析並執行對應操作。

### 更新帳戶餘額

使用者說出目前帳戶剩餘金額：

| 使用者輸入 | 解析動作 |
|------------|----------|
| 「台新銀行剩 15 萬」 | 更新台新銀行餘額為 150,000 |
| 「國泰戶頭還有 28 萬」 | 更新國泰銀行餘額為 280,000 |
| 「玉山帳戶目前 50000」 | 更新玉山銀行餘額為 50,000 |

**處理邏輯：**
1. 解析帳戶名稱（模糊比對現有帳戶）
2. 解析金額（支援「萬」、「千」等單位）
3. 如果帳戶不存在，詢問是否新增
4. 更新 assets.json 中的餘額
5. 記錄變動到 `transactions/YYYY-MM.json`（依交易日期的月份）

### 記錄存款/提款

使用者說出今天的存提款：

| 使用者輸入 | 解析動作 |
|------------|----------|
| 「今天領了 2 萬」 | 從預設帳戶扣除 20,000 |
| 「台新領了 5000」 | 從台新銀行扣除 5,000 |
| 「存了 3 萬到國泰」 | 國泰銀行增加 30,000 |
| 「薪水入帳 5 萬」 | 預設帳戶增加 50,000 |
| 「ATM 領 1 萬」 | 從預設帳戶扣除 10,000 |

**處理邏輯：**
1. 判斷是存款還是提款（領、提、取 = 扣除；存、入帳 = 增加）
2. 解析帳戶名稱（無指定時使用預設帳戶或詢問）
3. 解析金額
4. 計算新餘額並更新 assets.json
5. 記錄交易到 `transactions/YYYY-MM.json`（依交易日期的月份）
6. 更新月份檔案的 summary 摘要

**輸出範例：**
```
[提款] 台新銀行
- 提款金額：NT$20,000
- 原餘額：NT$150,000
- 新餘額：NT$130,000
```

### 記錄負債還款

使用者說出各類負債的還款：

| 使用者輸入 | 解析動作 |
|------------|----------|
| 「房貸還了 3.5 萬」 | 房貸剩餘本金扣除 35,000 |
| 「今天繳房貸 35000」 | 房貸剩餘本金扣除 35,000 |
| 「信貸還了 1.5 萬」 | 信貸剩餘本金扣除 15,000 |
| 「車貸繳了 18000」 | 車貸剩餘本金扣除 18,000 |
| 「信用卡還 5000」 | 信用卡剩餘扣除 5,000 |
| 「這個月貸款都繳了」 | 所有負債扣除各自的月繳金額 |

**處理邏輯：**
1. 解析負債類型（房貸、信貸、車貸、信用卡）
2. 如果有多筆同類型負債，詢問是哪一筆
3. 解析還款金額
4. 更新 liabilities.json 中的剩餘本金
5. 記錄還款到 `transactions/YYYY-MM.json`（依還款日期的月份）
6. 計算還款進度

**輸出範例：**
```
[還款] 房貸 - 台北房貸
- 還款金額：NT$35,000
- 原剩餘本金：NT$8,500,000
- 新剩餘本金：NT$8,465,000
- 還款進度：15.4% (已還 NT$1,535,000)
```

### 批次還款

使用者可以一次記錄多筆還款：

```
「這個月房貸還了 3.5 萬，信貸 1.5 萬，車貸 1.8 萬」
```

**輸出範例：**
```
[批次還款] 2026-01-29

| 項目 | 還款金額 | 剩餘本金 | 進度 |
|------|----------|----------|------|
| 房貸 | NT$35,000 | NT$8,465,000 | 15.4% |
| 信貸 | NT$15,000 | NT$185,000 | 63.0% |
| 車貸 | NT$18,000 | NT$432,000 | 46.0% |

本月還款總額：NT$68,000
```

### 金額解析規則

| 輸入格式 | 解析結果 |
|----------|----------|
| 15 萬 | 150,000 |
| 3.5 萬 | 35,000 |
| 1 萬 5 | 15,000 |
| 2 萬 5 千 | 25,000 |
| 5000 | 5,000 |
| 35000 | 35,000 |
| 一萬五 | 15,000 |
| 三萬五千 | 35,000 |

### 帳戶模糊比對

系統會自動比對使用者輸入的帳戶名稱：

| 輸入 | 可能比對 |
|------|----------|
| 台新 | 台新銀行 |
| 國泰 | 國泰世華 |
| 玉山 | 玉山銀行 |
| 中信 | 中國信託 |
| 郵局 | 中華郵政 |

如果無法確定是哪個帳戶，使用 `AskUserQuestion` 詢問使用者。

### 預設帳戶設定

如果使用者只說「領了 2 萬」沒有指定帳戶：
1. 檢查 config.json 是否有設定 `default_account`
2. 如果有，使用預設帳戶
3. 如果沒有，使用 `AskUserQuestion` 詢問：「請問是從哪個帳戶？」並列出所有帳戶選項
4. 詢問是否要設為預設帳戶

## 指令

### add - 新增資產或負債

**新增銀行帳戶：**
```
/asset-tracker add bank <帳戶名稱> <餘額>
```
範例：`/asset-tracker add bank 台新銀行 150000`

**新增加密貨幣：**
```
/asset-tracker add crypto <幣種> <數量>
```
範例：`/asset-tracker add crypto BTC 0.5`

**新增負債：**
```
/asset-tracker add liability <類型> <名稱> <總額> <剩餘本金> [月繳金額]
```
類型：mortgage（房貸）、credit（信貸）、car（車貸）、card（信用卡）、other
範例：`/asset-tracker add liability mortgage 台北房貸 10000000 8500000 35000`

### update - 更新餘額

**更新銀行餘額：**
```
/asset-tracker update bank <帳戶名稱或ID> <新餘額>
```

**更新加密貨幣數量：**
```
/asset-tracker update crypto <幣種> <新數量>
```

**更新負債剩餘本金：**
```
/asset-tracker update liability <名稱或ID> <新剩餘本金>
```

### delete - 刪除資產或負債

```
/asset-tracker delete <類型> <名稱或ID>
```
類型：bank、crypto、liability

### price - 查詢加密貨幣價格

```
/asset-tracker price [幣種]
```

**使用 CoinGecko API 查詢價格（免費、無需 API key）：**

**步驟：**
1. 使用 `WebFetch` 呼叫 CoinGecko API
2. 解析 JSON 回應取得 USD 和 TWD 價格
3. 更新 assets.json 中的價格紀錄
4. 計算持倉價值並顯示

**CoinGecko API 端點：**
```
https://api.coingecko.com/api/v3/simple/price?ids={幣種ID}&vs_currencies=usd,twd
```

**常用幣種 ID 對照表：**

| 符號 | CoinGecko ID |
|------|--------------|
| BTC | bitcoin |
| ETH | ethereum |
| ADA | cardano |
| SOL | solana |
| DOT | polkadot |
| AVAX | avalanche-2 |
| MATIC/POL | polygon-ecosystem-token |
| LINK | chainlink |
| UNI | uniswap |
| ATOM | cosmos |

**查詢多幣種範例：**
```
https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,cardano,polygon-ecosystem-token&vs_currencies=usd,twd
```

**回應格式：**
```json
{
  "bitcoin": { "usd": 87863, "twd": 2754204 },
  "ethereum": { "usd": 2942.69, "twd": 92243 },
  "cardano": { "usd": 0.349, "twd": 10.94 },
  "polygon-ecosystem-token": { "usd": 0.117, "twd": 3.66 }
}
```

**無參數時**，更新所有持有幣種的價格。

**輸出範例：**
```
[價格更新] 2026-01-29 14:30

| 幣種 | 數量 | 單價 (USD) | 價值 (USD) | 價值 (TWD) |
|------|------|-----------|-----------|-----------|
| BTC  | 0.5  | $87,863   | $43,932   | NT$1,377,102 |
| ETH  | 2.0  | $2,943    | $5,886    | NT$184,486 |

加密貨幣總值：$49,818 (NT$1,561,588)
```

### summary - 資產總覽

```
/asset-tracker summary
```

顯示所有資產、負債與淨資產：

```
[資產總覽] 2026-01-29

## 資產
| 類型 | 名稱 | 金額 (TWD) |
|------|------|-----------|
| 銀行 | 台新銀行 | NT$150,000 |
| 銀行 | 國泰銀行 | NT$280,000 |
| 加密 | BTC (0.5) | NT$1,665,625 |
| 加密 | ETH (2.0) | NT$208,000 |
資產小計：NT$2,303,625

## 負債
| 類型 | 名稱 | 剩餘本金 (TWD) |
|------|------|---------------|
| 房貸 | 台北房貸 | NT$8,500,000 |
| 信貸 | 裝潢貸款 | NT$200,000 |
負債小計：NT$8,700,000

## 淨資產
淨資產 = 資產 - 負債 = NT$2,303,625 - NT$8,700,000 = NT$-6,396,375
```

### report - 產生報表

```
/asset-tracker report [類型]
```

**類型：**
- `dashboard`（預設）- 產生資產儀表板 HTML
- `trend` - 產生趨勢分析報表
- `allocation` - 產生資產配置分析

**步驟：**
1. 讀取 assets.json 和 liabilities.json
2. 查詢最新加密貨幣價格
3. 讀取 assets/html-template.md 或 assets/dashboard-template.md 模板
4. 計算各項統計數據
5. 產生 HTML 報表
6. 儲存至 `asset-tracker/reports/`

### snapshot - 儲存快照

```
/asset-tracker snapshot
```

將當前資產負債狀態儲存為快照，用於歷史追蹤。

**步驟：**
1. 讀取當前 assets.json 和 liabilities.json
2. 查詢最新加密貨幣價格
3. 計算總資產、總負債、淨資產
4. 儲存至 `asset-tracker/snapshots/YYYY-MM-DD.json`

### history - 查看歷史

```
/asset-tracker history [天數]
```

顯示過去 N 天（預設 30 天）的淨資產變化：

```
[淨資產歷史] 過去 30 天

| 日期 | 總資產 | 總負債 | 淨資產 | 變化 |
|------|--------|--------|--------|------|
| 01-29 | NT$2,303,625 | NT$8,700,000 | NT$-6,396,375 | - |
| 01-22 | NT$2,150,000 | NT$8,720,000 | NT$-6,570,000 | +NT$173,625 |
...

30 天淨資產變化：+NT$250,000 (+3.8%)
```

### pay - 記錄還款

```
/asset-tracker pay <負債名稱或ID> <還款金額>
```

記錄負債還款，自動更新剩餘本金。

### transactions - 查看交易紀錄

```
/asset-tracker transactions [YYYY-MM]
```

顯示指定月份（預設當月）的所有交易紀錄：

```
[交易紀錄] 2026-01

| 日期 | 類型 | 帳戶/項目 | 金額 | 說明 |
|------|------|-----------|------|------|
| 01-29 | 提款 | 台新銀行 | -NT$20,000 | ATM 提款 |
| 01-29 | 存款 | 台新銀行 | +NT$50,000 | 薪水入帳 |
| 01-05 | 還款 | 房貸 | -NT$35,000 | 房貸月繳 |
| 01-05 | 還款 | 信貸 | -NT$15,000 | 信貸月繳 |
| 01-05 | 還款 | 車貸 | -NT$18,000 | 車貸月繳 |

本月摘要：
- 總存款：NT$50,000
- 總提款：NT$20,000
- 總還款：NT$68,000
- 淨現金流：+NT$30,000
```

### goal - 設定財務目標

```
/asset-tracker goal set <目標類型> <目標金額> [期限]
```

**目標類型：**
- `networth` - 淨資產目標
- `savings` - 儲蓄目標
- `debt_free` - 負債清償目標

```
/asset-tracker goal list
```

顯示所有目標及進度。

### update - 更新技能

```
/asset-tracker update
```

```bash
npx openskills update
```

## 匯率處理

**使用 CoinGecko API 直接取得 TWD 價格，無需額外換算匯率。**

API 支援多種法幣，查詢時直接指定 `vs_currencies=usd,twd` 即可同時取得 USD 和 TWD 價格。

**如需單獨查詢匯率：**
```
https://api.coingecko.com/api/v3/exchange_rates
```

此端點返回 BTC 對各種法幣的匯率，可用於計算 USD/TWD 匯率。

## 資源

- `references/schema.md` - JSON 資料結構定義
- `assets/html-template.md` - 報表 HTML 模板
- `assets/dashboard-template.md` - 儀表板 HTML 模板

## 回應風格

- 使用繁體中文
- **不使用任何 emoji 符號**
- 金額使用千分位格式（如 NT$1,234,567）
- 加密貨幣保留適當小數位數
- 用 [+] 表示正向變化、[-] 表示負向變化、[!] 表示警告
