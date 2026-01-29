# Asset Tracker

個人資產負債管理工具，追蹤你的財務狀況。

## 功能

- 追蹤銀行帳戶餘額
- 追蹤加密貨幣持倉與即時價格（使用 CoinGecko API）
- 管理負債（房貸、信貸、車貸、信用卡）
- 記錄存款、提款、還款等交易
- 產生資產淨值報表

## 安裝

```bash
npx openskills install asset-tracker
```

## 使用方式

### 自然語言操作

直接用口語描述財務變動：

```
永豐銀行有 30 萬
比特幣有 0.5
今天領了 2 萬
房貸還了 3.5 萬
```

### 指令

| 指令 | 說明 |
|------|------|
| `add bank <名稱> <餘額>` | 新增銀行帳戶 |
| `add crypto <幣種> <數量>` | 新增加密貨幣 |
| `add liability <類型> <名稱> <總額> <剩餘> [月繳]` | 新增負債 |
| `update bank <名稱> <新餘額>` | 更新銀行餘額 |
| `price [幣種]` | 查詢加密貨幣價格 |
| `summary` | 資產總覽 |
| `transactions [YYYY-MM]` | 查看交易紀錄 |
| `snapshot` | 儲存當日快照 |
| `report` | 產生報表 |

## 資料儲存

所有資料儲存在專案根目錄的 `asset-tracker/` 資料夾：

```
asset-tracker/
├── config.json           # 設定檔
├── assets.json           # 資產紀錄
├── liabilities.json      # 負債紀錄
├── transactions/
│   └── YYYY-MM.json      # 每月交易紀錄
├── snapshots/
│   └── YYYY-MM-DD.json   # 每日快照
└── reports/
    └── dashboard.html    # 報表
```

## 加密貨幣價格 API

使用 CoinGecko 免費 API 查詢即時價格，無需 API key：

```
https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd,twd
```

支援直接取得 TWD 價格，無需額外換算匯率。

## 支援的加密貨幣

| 符號 | CoinGecko ID |
|------|--------------|
| BTC | bitcoin |
| ETH | ethereum |
| ADA | cardano |
| SOL | solana |
| POL/MATIC | polygon-ecosystem-token |
| DOT | polkadot |
| LINK | chainlink |
| UNI | uniswap |

## 更新

```bash
npx openskills update
```

## 授權

MIT
