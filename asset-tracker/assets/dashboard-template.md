# HTML 資產儀表板範本

產生資產儀表板首頁時使用此模板。使用 Tailwind CSS CDN。適合快速總覽。

## 報告內容

1. 淨資產大卡片
2. 資產/負債雙欄對比
3. 加密貨幣即時價格
4. 近期變化趨勢

## HTML 範本

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>資產儀表板</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-900 min-h-screen py-8">
  <div class="max-w-6xl mx-auto px-4">

    <!-- 標題 -->
    <div class="flex justify-between items-center mb-8">
      <h1 class="text-3xl font-bold text-white">資產儀表板</h1>
      <span class="text-slate-400">更新時間：{{UPDATE_TIME}}</span>
    </div>

    <!-- 淨資產主卡片 -->
    <div class="bg-gradient-to-br {{NET_WORTH_GRADIENT}} rounded-2xl shadow-2xl p-8 mb-8">
      <div class="flex justify-between items-start">
        <div>
          <p class="text-white/70 text-lg mb-2">淨資產</p>
          <p class="text-5xl font-bold text-white mb-4">{{NET_WORTH}}</p>
          <div class="flex items-center space-x-4">
            <span class="{{NET_WORTH_CHANGE_BG}} px-3 py-1 rounded-full text-sm font-medium">
              {{NET_WORTH_CHANGE_ICON}} {{NET_WORTH_CHANGE}}
            </span>
            <span class="text-white/60 text-sm">較上次更新</span>
          </div>
        </div>
        <div class="text-right">
          <div class="text-white/70 text-sm mb-1">匯率 USD/TWD</div>
          <div class="text-white text-2xl font-semibold">{{EXCHANGE_RATE}}</div>
        </div>
      </div>
    </div>

    <!-- 資產/負債對比 -->
    <div class="grid grid-cols-2 gap-6 mb-8">
      <!-- 資產卡片 -->
      <div class="bg-slate-800 rounded-xl p-6">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-xl font-semibold text-white">資產</h2>
          <span class="text-3xl font-bold text-emerald-400">{{TOTAL_ASSETS}}</span>
        </div>

        <!-- 資產配置條 -->
        <div class="flex h-4 rounded-full overflow-hidden mb-4">
          {{#ASSET_BARS}}
          <div class="{{BAR_COLOR}}" style="width: {{BAR_PERCENT}}%" title="{{BAR_LABEL}}"></div>
          {{/ASSET_BARS}}
        </div>

        <!-- 資產明細 -->
        <div class="space-y-3">
          {{#ASSET_ITEMS}}
          <div class="flex justify-between items-center">
            <div class="flex items-center">
              <div class="w-3 h-3 rounded-full {{ITEM_DOT_COLOR}} mr-3"></div>
              <span class="text-slate-300">{{ITEM_NAME}}</span>
            </div>
            <span class="text-white font-medium">{{ITEM_VALUE}}</span>
          </div>
          {{/ASSET_ITEMS}}
        </div>
      </div>

      <!-- 負債卡片 -->
      <div class="bg-slate-800 rounded-xl p-6">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-xl font-semibold text-white">負債</h2>
          <span class="text-3xl font-bold text-red-400">{{TOTAL_LIABILITIES}}</span>
        </div>

        <!-- 負債配置條 -->
        <div class="flex h-4 rounded-full overflow-hidden mb-4 bg-slate-700">
          {{#LIABILITY_BARS}}
          <div class="{{BAR_COLOR}}" style="width: {{BAR_PERCENT}}%" title="{{BAR_LABEL}}"></div>
          {{/LIABILITY_BARS}}
        </div>

        <!-- 負債明細 -->
        <div class="space-y-3">
          {{#LIABILITY_ITEMS}}
          <div class="flex justify-between items-center">
            <div class="flex items-center">
              <div class="w-3 h-3 rounded-full {{ITEM_DOT_COLOR}} mr-3"></div>
              <span class="text-slate-300">{{ITEM_NAME}}</span>
            </div>
            <span class="text-white font-medium">{{ITEM_VALUE}}</span>
          </div>
          {{/LIABILITY_ITEMS}}
        </div>

        <!-- 每月還款總額 -->
        <div class="mt-4 pt-4 border-t border-slate-700">
          <div class="flex justify-between items-center">
            <span class="text-slate-400">每月還款總額</span>
            <span class="text-amber-400 font-semibold">{{MONTHLY_PAYMENT}}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 加密貨幣區塊 -->
    <div class="bg-slate-800 rounded-xl p-6 mb-8">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-xl font-semibold text-white">加密貨幣</h2>
        <div class="flex items-center space-x-2">
          <span class="text-slate-400 text-sm">總值</span>
          <span class="text-2xl font-bold text-orange-400">{{CRYPTO_TOTAL}}</span>
        </div>
      </div>

      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        {{#CRYPTO_CARDS}}
        <div class="bg-slate-700/50 rounded-lg p-4">
          <div class="flex items-center justify-between mb-2">
            <span class="text-lg font-bold text-white">{{SYMBOL}}</span>
            <span class="{{CHANGE_COLOR}} text-sm font-medium">{{CHANGE_24H}}</span>
          </div>
          <div class="text-slate-400 text-sm mb-1">{{QUANTITY}} {{SYMBOL}}</div>
          <div class="text-white font-semibold">${{PRICE_USD}}</div>
          <div class="text-slate-500 text-xs">{{VALUE_TWD}}</div>
        </div>
        {{/CRYPTO_CARDS}}
      </div>
    </div>

    <!-- 銀行帳戶 -->
    <div class="bg-slate-800 rounded-xl p-6 mb-8">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-xl font-semibold text-white">銀行帳戶</h2>
        <span class="text-2xl font-bold text-emerald-400">{{BANK_TOTAL}}</span>
      </div>

      <div class="grid grid-cols-2 md:grid-cols-3 gap-4">
        {{#BANK_CARDS}}
        <div class="bg-slate-700/50 rounded-lg p-4">
          <div class="text-slate-400 text-sm mb-1">{{BANK_NAME}}</div>
          <div class="text-xl font-bold text-white">{{BANK_BALANCE}}</div>
          <div class="text-slate-500 text-xs">{{BANK_NOTES}}</div>
        </div>
        {{/BANK_CARDS}}
      </div>
    </div>

    <!-- 趨勢圖 -->
    <div class="bg-slate-800 rounded-xl p-6 mb-8">
      <h2 class="text-xl font-semibold text-white mb-6">淨資產趨勢 (近 30 天)</h2>
      <div class="space-y-2">
        {{#TREND_ITEMS}}
        <div class="flex items-center">
          <span class="w-20 text-slate-400 text-sm">{{DATE}}</span>
          <div class="flex-1 mx-4">
            <div class="w-full bg-slate-700 rounded-full h-3">
              <div class="{{BAR_COLOR}} h-3 rounded-full transition-all" style="width: {{BAR_WIDTH}}%"></div>
            </div>
          </div>
          <span class="w-32 text-right {{VALUE_COLOR}} font-medium">{{VALUE}}</span>
        </div>
        {{/TREND_ITEMS}}
      </div>
    </div>

    <!-- 財務指標 -->
    <div class="grid grid-cols-4 gap-4 mb-8">
      <div class="bg-slate-800 rounded-xl p-4 text-center">
        <div class="text-slate-400 text-sm mb-2">負債比率</div>
        <div class="text-2xl font-bold {{DEBT_RATIO_COLOR}}">{{DEBT_RATIO}}</div>
      </div>
      <div class="bg-slate-800 rounded-xl p-4 text-center">
        <div class="text-slate-400 text-sm mb-2">流動比率</div>
        <div class="text-2xl font-bold {{LIQUID_RATIO_COLOR}}">{{LIQUID_RATIO}}</div>
      </div>
      <div class="bg-slate-800 rounded-xl p-4 text-center">
        <div class="text-slate-400 text-sm mb-2">財務跑道</div>
        <div class="text-2xl font-bold text-blue-400">{{RUNWAY_MONTHS}} 個月</div>
      </div>
      <div class="bg-slate-800 rounded-xl p-4 text-center">
        <div class="text-slate-400 text-sm mb-2">還款進度</div>
        <div class="text-2xl font-bold text-purple-400">{{PAYOFF_PROGRESS}}</div>
      </div>
    </div>

    <!-- 頁尾 -->
    <div class="text-center text-slate-500 text-sm">
      Asset Tracker | 資料僅供參考
    </div>
  </div>
</body>
</html>
```

## 配色說明

### 淨資產漸層
- 正值：`from-emerald-600 to-teal-600`
- 負值：`from-red-600 to-rose-600`

### 變化標籤背景
- 正變化：`bg-emerald-500/20 text-emerald-400`
- 負變化：`bg-red-500/20 text-red-400`

### 資產類型顏色
- 銀行：`bg-emerald-500` / `bg-emerald-500`
- 加密貨幣：`bg-orange-500` / `bg-orange-500`
- 股票：`bg-blue-500` / `bg-blue-500`
- 其他：`bg-slate-500` / `bg-slate-500`

### 負債類型顏色
- 房貸：`bg-red-500` / `bg-red-500`
- 信貸：`bg-pink-500` / `bg-pink-500`
- 車貸：`bg-amber-500` / `bg-amber-500`
- 信用卡：`bg-purple-500` / `bg-purple-500`

### 財務指標顏色
- 負債比率 < 50%：`text-emerald-400`
- 負債比率 50-80%：`text-amber-400`
- 負債比率 > 80%：`text-red-400`

### 趨勢條顏色
- 正值：`bg-emerald-500`
- 負值：`bg-red-500`
