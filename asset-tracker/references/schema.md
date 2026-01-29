# Asset Tracker 資料結構

## 資料夾結構

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
    ├── dashboard.html    # 最新儀表板
    └── YYYY-MM-DD.html   # 歷史報表
```

## JSON Schema

### 設定檔 (config.json)

```json
{
  "currency": "TWD",
  "default_account": "b1a2c3",
  "asset_categories": ["bank", "crypto", "stock", "other"],
  "liability_categories": ["mortgage", "credit", "car", "card", "other"],
  "price_api": {
    "provider": "coingecko",
    "base_url": "https://api.coingecko.com/api/v3",
    "endpoints": {
      "simple_price": "/simple/price",
      "exchange_rates": "/exchange_rates"
    },
    "last_updated": "2026-01-29"
  },
  "coingecko_ids": {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "ADA": "cardano",
    "POL": "polygon-ecosystem-token",
    "SOL": "solana",
    "DOT": "polkadot",
    "AVAX": "avalanche-2",
    "LINK": "chainlink",
    "UNI": "uniswap",
    "ATOM": "cosmos",
    "USDT": "tether",
    "USDC": "usd-coin"
  },
  "goals": [
    {
      "id": "g1h2i3",
      "type": "networth",
      "target": 5000000,
      "deadline": "2026-12-31",
      "created_at": "2026-01-01"
    }
  ],
  "created_at": "2026-01-01",
  "version": "1.1.0"
}
```

| 欄位 | 類型 | 說明 |
|------|------|------|
| currency | string | 顯示貨幣（TWD/USD） |
| default_account | string | 預設銀行帳戶 ID（選填） |
| asset_categories | array | 啟用的資產類別 |
| liability_categories | array | 啟用的負債類別 |
| price_api | object | CoinGecko API 設定 |
| coingecko_ids | object | 幣種符號對應 CoinGecko ID |
| goals | array | 財務目標 |
| version | string | 設定檔版本 |

#### price_api 欄位

| 欄位 | 類型 | 說明 |
|------|------|------|
| provider | string | API 提供者（coingecko） |
| base_url | string | API 基礎網址 |
| endpoints | object | API 端點路徑 |
| last_updated | string | 最後更新日期 |

### 資產紀錄 (assets.json)

```json
{
  "updated_at": "2026-01-29T14:30:00",
  "bank_accounts": [
    {
      "id": "b1a2c3",
      "name": "台新銀行",
      "balance": 150000,
      "currency": "TWD",
      "notes": "薪轉戶",
      "updated_at": "2026-01-29"
    }
  ],
  "crypto": [
    {
      "id": "c1d2e3",
      "symbol": "BTC",
      "name": "Bitcoin",
      "coingecko_id": "bitcoin",
      "quantity": 0.5,
      "avg_cost": 95000,
      "price_usd": 87863,
      "price_twd": 2754204,
      "price_updated_at": "2026-01-29T14:30:00"
    },
    {
      "id": "c4d5e6",
      "symbol": "ETH",
      "name": "Ethereum",
      "coingecko_id": "ethereum",
      "quantity": 2.0,
      "avg_cost": 2800,
      "price_usd": 2942.69,
      "price_twd": 92243,
      "price_updated_at": "2026-01-29T14:30:00"
    }
  ],
  "stocks": [
    {
      "id": "s1t2u3",
      "symbol": "2330",
      "name": "台積電",
      "shares": 100,
      "avg_cost": 550,
      "current_price": 580,
      "price_currency": "TWD",
      "price_updated_at": "2026-01-29"
    }
  ],
  "other_assets": [
    {
      "id": "o1p2q3",
      "name": "緊急預備金",
      "value": 100000,
      "currency": "TWD",
      "notes": "放在家裡的現金",
      "updated_at": "2026-01-15"
    }
  ]
}
```

#### 銀行帳戶欄位

| 欄位 | 類型 | 說明 |
|------|------|------|
| id | string | 唯一識別碼（6 碼） |
| name | string | 帳戶名稱 |
| balance | number | 餘額 |
| currency | string | 貨幣 |
| notes | string | 備註（選填） |
| updated_at | string | 更新日期 |

#### 加密貨幣欄位

| 欄位 | 類型 | 說明 |
|------|------|------|
| id | string | 唯一識別碼（6 碼） |
| symbol | string | 代號（BTC、ETH 等） |
| name | string | 全名 |
| coingecko_id | string | CoinGecko API 的幣種 ID |
| quantity | number | 持有數量 |
| avg_cost | number | 平均成本（選填） |
| price_usd | number | 目前 USD 價格 |
| price_twd | number | 目前 TWD 價格 |
| price_updated_at | string | 價格更新時間 |

#### 股票/基金欄位

| 欄位 | 類型 | 說明 |
|------|------|------|
| id | string | 唯一識別碼（6 碼） |
| symbol | string | 股票代號 |
| name | string | 股票名稱 |
| shares | number | 持有股數 |
| avg_cost | number | 平均成本（選填） |
| current_price | number | 目前股價 |
| price_currency | string | 價格貨幣 |
| price_updated_at | string | 價格更新時間 |

### 負債紀錄 (liabilities.json)

```json
{
  "updated_at": "2026-01-29",
  "liabilities": [
    {
      "id": "l1m2n3",
      "type": "mortgage",
      "name": "台北房貸",
      "original_amount": 10000000,
      "remaining_principal": 8500000,
      "interest_rate": 2.1,
      "monthly_payment": 35000,
      "start_date": "2022-06-01",
      "end_date": "2042-06-01",
      "currency": "TWD",
      "notes": "寬限期至 2024-06",
      "payment_history": [
        {
          "date": "2026-01-05",
          "amount": 35000,
          "principal": 28000,
          "interest": 7000
        }
      ]
    },
    {
      "id": "l4m5n6",
      "type": "credit",
      "name": "裝潢貸款",
      "original_amount": 500000,
      "remaining_principal": 200000,
      "interest_rate": 3.5,
      "monthly_payment": 15000,
      "start_date": "2024-01-01",
      "end_date": "2027-01-01",
      "currency": "TWD"
    },
    {
      "id": "l7m8n9",
      "type": "car",
      "name": "車貸",
      "original_amount": 800000,
      "remaining_principal": 450000,
      "interest_rate": 2.8,
      "monthly_payment": 18000,
      "start_date": "2024-06-01",
      "end_date": "2028-06-01",
      "currency": "TWD"
    },
    {
      "id": "l0m1n2",
      "type": "card",
      "name": "信用卡分期",
      "original_amount": 60000,
      "remaining_principal": 40000,
      "interest_rate": 0,
      "monthly_payment": 5000,
      "start_date": "2025-10-01",
      "end_date": "2026-10-01",
      "currency": "TWD"
    }
  ]
}
```

#### 負債欄位

| 欄位 | 類型 | 說明 |
|------|------|------|
| id | string | 唯一識別碼（6 碼） |
| type | string | 類型（mortgage/credit/car/card/other） |
| name | string | 負債名稱 |
| original_amount | number | 原始借款金額 |
| remaining_principal | number | 剩餘本金 |
| interest_rate | number | 年利率（%） |
| monthly_payment | number | 每月還款金額 |
| start_date | string | 起始日期 |
| end_date | string | 結束日期 |
| currency | string | 貨幣 |
| notes | string | 備註（選填） |
| payment_history | array | 還款紀錄（選填） |

### 快照 (snapshots/YYYY-MM-DD.json)

```json
{
  "date": "2026-01-29",
  "timestamp": "2026-01-29T14:30:00",
  "summary": {
    "total_assets": 2303625,
    "total_liabilities": 8700000,
    "net_worth": -6396375,
    "currency": "TWD"
  },
  "breakdown": {
    "assets": {
      "bank": 430000,
      "crypto": 1873625,
      "stock": 0,
      "other": 0
    },
    "liabilities": {
      "mortgage": 8500000,
      "credit": 200000,
      "car": 0,
      "card": 0,
      "other": 0
    }
  },
  "exchange_rates": {
    "USD_TWD": 32.5
  },
  "crypto_prices": {
    "BTC": 102500,
    "ETH": 3200
  }
}
```

| 欄位 | 類型 | 說明 |
|------|------|------|
| date | string | 快照日期 |
| timestamp | string | 完整時間戳記 |
| summary | object | 摘要數據 |
| breakdown | object | 分類明細 |
| exchange_rates | object | 當時匯率 |
| crypto_prices | object | 當時加密貨幣價格 |

### 交易紀錄 (transactions/YYYY-MM.json)

記錄每月的存款、提款、還款等交易明細。

```json
{
  "month": "2026-01",
  "transactions": [
    {
      "id": "t1x2y3",
      "date": "2026-01-29",
      "time": "14:30",
      "type": "withdrawal",
      "account_id": "b1a2c3",
      "account_name": "台新銀行",
      "amount": 20000,
      "balance_before": 150000,
      "balance_after": 130000,
      "description": "ATM 提款",
      "category": "cash"
    },
    {
      "id": "t4x5y6",
      "date": "2026-01-29",
      "time": "09:00",
      "type": "deposit",
      "account_id": "b1a2c3",
      "account_name": "台新銀行",
      "amount": 50000,
      "balance_before": 100000,
      "balance_after": 150000,
      "description": "薪水入帳",
      "category": "salary"
    },
    {
      "id": "t7x8y9",
      "date": "2026-01-05",
      "time": "10:00",
      "type": "payment",
      "liability_id": "l1m2n3",
      "liability_name": "台北房貸",
      "liability_type": "mortgage",
      "amount": 35000,
      "principal_before": 8535000,
      "principal_after": 8500000,
      "description": "房貸月繳"
    },
    {
      "id": "t0x1y2",
      "date": "2026-01-29",
      "time": "15:00",
      "type": "balance_update",
      "account_id": "b1a2c3",
      "account_name": "台新銀行",
      "balance_before": 130000,
      "balance_after": 125000,
      "description": "手動更新餘額"
    }
  ],
  "summary": {
    "total_deposits": 50000,
    "total_withdrawals": 20000,
    "total_payments": 68000,
    "net_cash_flow": 30000
  }
}
```

#### 交易欄位

| 欄位 | 類型 | 說明 |
|------|------|------|
| id | string | 唯一識別碼（6 碼） |
| date | string | 交易日期 YYYY-MM-DD |
| time | string | 交易時間 HH:MM |
| type | string | 類型（見下表） |
| amount | number | 交易金額 |
| description | string | 交易說明 |

#### 交易類型

| 類型 | 說明 | 額外欄位 |
|------|------|----------|
| deposit | 存款 | account_id, balance_before, balance_after, category |
| withdrawal | 提款 | account_id, balance_before, balance_after, category |
| payment | 負債還款 | liability_id, liability_type, principal_before, principal_after |
| balance_update | 手動更新餘額 | account_id, balance_before, balance_after |
| transfer | 帳戶間轉帳 | from_account_id, to_account_id |

#### 交易分類 (category)

| 分類 | 說明 |
|------|------|
| salary | 薪資收入 |
| bonus | 獎金 |
| investment | 投資收益 |
| cash | 現金提領 |
| expense | 一般支出 |
| transfer | 轉帳 |
| other | 其他 |

## ID 生成規則

使用 6 碼隨機英數字：`a-z0-9`

## 負債類型對照

| 類型代碼 | 中文名稱 | 說明 |
|----------|----------|------|
| mortgage | 房貸 | 房屋貸款 |
| credit | 信貸 | 個人信用貸款 |
| car | 車貸 | 汽車貸款 |
| card | 信用卡 | 信用卡分期或循環利息 |
| other | 其他 | 其他類型負債 |

## 加密貨幣常見代號與 CoinGecko ID

| 代號 | 全名 | CoinGecko ID |
|------|------|--------------|
| BTC | Bitcoin | bitcoin |
| ETH | Ethereum | ethereum |
| USDT | Tether | tether |
| USDC | USD Coin | usd-coin |
| SOL | Solana | solana |
| ADA | Cardano | cardano |
| DOT | Polkadot | polkadot |
| POL/MATIC | Polygon | polygon-ecosystem-token |
| LINK | Chainlink | chainlink |
| UNI | Uniswap | uniswap |
| AVAX | Avalanche | avalanche-2 |
| ATOM | Cosmos | cosmos |

**CoinGecko API 端點：**
```
https://api.coingecko.com/api/v3/simple/price?ids={幣種ID}&vs_currencies=usd,twd
```
