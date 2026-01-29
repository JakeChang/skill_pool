# HTML 資產報表範本

產生資產報表時使用此模板。使用 Tailwind CSS CDN。

## 報告內容

1. 日期標題
2. 淨資產摘要卡（大數字顯示）
3. 資產/負債比例圖
4. 各類資產明細表
5. 各類負債明細表
6. 加密貨幣價格資訊
7. 歷史趨勢（如有快照資料）

## HTML 範本

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>資產報表 - {{DATE}}</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 min-h-screen py-8">
  <div class="max-w-4xl mx-auto px-4">

    <!-- 標題與淨資產 -->
    <div class="bg-gradient-to-r {{NET_WORTH_GRADIENT}} rounded-lg shadow-md p-6 mb-6 text-white">
      <div class="flex justify-between items-center">
        <div>
          <h1 class="text-2xl font-bold">資產報表</h1>
          <p class="opacity-80">{{DATE}} 更新</p>
        </div>
        <div class="text-right">
          <div class="text-sm opacity-80">淨資產</div>
          <div class="text-4xl font-bold">{{NET_WORTH}}</div>
          <div class="text-sm {{NET_WORTH_CHANGE_COLOR}}">{{NET_WORTH_CHANGE}}</div>
        </div>
      </div>
    </div>

    <!-- 資產/負債摘要卡片 -->
    <div class="grid grid-cols-2 gap-4 mb-6">
      <div class="bg-white rounded-lg shadow-md p-6">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-lg font-semibold text-gray-700">總資產</h2>
          <span class="text-2xl font-bold text-emerald-500">[+]</span>
        </div>
        <div class="text-3xl font-bold text-emerald-600">{{TOTAL_ASSETS}}</div>
        <div class="mt-4 space-y-2">
          {{#ASSET_BREAKDOWN}}
          <div class="flex justify-between text-sm">
            <span class="text-gray-600">{{CATEGORY_NAME}}</span>
            <span class="text-gray-800 font-medium">{{CATEGORY_VALUE}}</span>
          </div>
          {{/ASSET_BREAKDOWN}}
        </div>
      </div>
      <div class="bg-white rounded-lg shadow-md p-6">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-lg font-semibold text-gray-700">總負債</h2>
          <span class="text-2xl font-bold text-red-500">[-]</span>
        </div>
        <div class="text-3xl font-bold text-red-600">{{TOTAL_LIABILITIES}}</div>
        <div class="mt-4 space-y-2">
          {{#LIABILITY_BREAKDOWN}}
          <div class="flex justify-between text-sm">
            <span class="text-gray-600">{{CATEGORY_NAME}}</span>
            <span class="text-gray-800 font-medium">{{CATEGORY_VALUE}}</span>
          </div>
          {{/LIABILITY_BREAKDOWN}}
        </div>
      </div>
    </div>

    <!-- 資產配置圖 -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-6">
      <h2 class="text-lg font-semibold text-gray-700 mb-4">資產配置</h2>
      <div class="flex h-8 rounded-full overflow-hidden">
        {{#ALLOCATION_BARS}}
        <div class="{{BAR_COLOR}}" style="width: {{BAR_PERCENT}}%" title="{{BAR_LABEL}}: {{BAR_PERCENT}}%"></div>
        {{/ALLOCATION_BARS}}
      </div>
      <div class="flex flex-wrap gap-4 mt-4">
        {{#ALLOCATION_LEGEND}}
        <div class="flex items-center">
          <div class="w-3 h-3 rounded-full {{LEGEND_COLOR}} mr-2"></div>
          <span class="text-sm text-gray-600">{{LEGEND_LABEL}} ({{LEGEND_PERCENT}}%)</span>
        </div>
        {{/ALLOCATION_LEGEND}}
      </div>
    </div>

    <!-- 銀行帳戶明細 -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-6">
      <h2 class="text-lg font-semibold text-gray-700 mb-4">銀行帳戶</h2>
      <table class="w-full">
        <thead>
          <tr class="border-b border-gray-200">
            <th class="text-left py-2 text-sm text-gray-500">帳戶</th>
            <th class="text-right py-2 text-sm text-gray-500">餘額</th>
            <th class="text-right py-2 text-sm text-gray-500">更新日期</th>
          </tr>
        </thead>
        <tbody>
          {{#BANK_ACCOUNTS}}
          <tr class="border-b border-gray-100">
            <td class="py-3 text-gray-800">{{ACCOUNT_NAME}}</td>
            <td class="py-3 text-right font-medium text-gray-800">{{ACCOUNT_BALANCE}}</td>
            <td class="py-3 text-right text-sm text-gray-500">{{ACCOUNT_UPDATED}}</td>
          </tr>
          {{/BANK_ACCOUNTS}}
        </tbody>
        <tfoot>
          <tr class="bg-gray-50">
            <td class="py-3 font-semibold text-gray-700">小計</td>
            <td class="py-3 text-right font-bold text-emerald-600">{{BANK_TOTAL}}</td>
            <td></td>
          </tr>
        </tfoot>
      </table>
    </div>

    <!-- 加密貨幣明細 -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-6">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-lg font-semibold text-gray-700">加密貨幣</h2>
        <span class="text-xs text-gray-400">價格更新：{{CRYPTO_PRICE_TIME}}</span>
      </div>
      <table class="w-full">
        <thead>
          <tr class="border-b border-gray-200">
            <th class="text-left py-2 text-sm text-gray-500">幣種</th>
            <th class="text-right py-2 text-sm text-gray-500">數量</th>
            <th class="text-right py-2 text-sm text-gray-500">單價 (USD)</th>
            <th class="text-right py-2 text-sm text-gray-500">價值</th>
            <th class="text-right py-2 text-sm text-gray-500">損益</th>
          </tr>
        </thead>
        <tbody>
          {{#CRYPTO_HOLDINGS}}
          <tr class="border-b border-gray-100">
            <td class="py-3">
              <span class="font-medium text-gray-800">{{CRYPTO_SYMBOL}}</span>
              <span class="text-xs text-gray-500 ml-1">{{CRYPTO_NAME}}</span>
            </td>
            <td class="py-3 text-right text-gray-600">{{CRYPTO_QUANTITY}}</td>
            <td class="py-3 text-right text-gray-600">${{CRYPTO_PRICE}}</td>
            <td class="py-3 text-right font-medium text-gray-800">{{CRYPTO_VALUE}}</td>
            <td class="py-3 text-right font-medium {{CRYPTO_PNL_COLOR}}">{{CRYPTO_PNL}}</td>
          </tr>
          {{/CRYPTO_HOLDINGS}}
        </tbody>
        <tfoot>
          <tr class="bg-gray-50">
            <td colspan="3" class="py-3 font-semibold text-gray-700">小計</td>
            <td class="py-3 text-right font-bold text-emerald-600">{{CRYPTO_TOTAL}}</td>
            <td class="py-3 text-right font-bold {{CRYPTO_TOTAL_PNL_COLOR}}">{{CRYPTO_TOTAL_PNL}}</td>
          </tr>
        </tfoot>
      </table>
    </div>

    <!-- 負債明細 -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-6">
      <h2 class="text-lg font-semibold text-gray-700 mb-4">負債明細</h2>
      <table class="w-full">
        <thead>
          <tr class="border-b border-gray-200">
            <th class="text-left py-2 text-sm text-gray-500">項目</th>
            <th class="text-right py-2 text-sm text-gray-500">原始金額</th>
            <th class="text-right py-2 text-sm text-gray-500">剩餘本金</th>
            <th class="text-right py-2 text-sm text-gray-500">月繳</th>
            <th class="text-right py-2 text-sm text-gray-500">進度</th>
          </tr>
        </thead>
        <tbody>
          {{#LIABILITIES}}
          <tr class="border-b border-gray-100">
            <td class="py-3">
              <span class="font-medium text-gray-800">{{LIABILITY_NAME}}</span>
              <span class="text-xs px-2 py-0.5 rounded {{LIABILITY_TYPE_COLOR}} ml-2">{{LIABILITY_TYPE}}</span>
            </td>
            <td class="py-3 text-right text-gray-600">{{LIABILITY_ORIGINAL}}</td>
            <td class="py-3 text-right font-medium text-red-600">{{LIABILITY_REMAINING}}</td>
            <td class="py-3 text-right text-gray-600">{{LIABILITY_MONTHLY}}</td>
            <td class="py-3 text-right">
              <div class="flex items-center justify-end">
                <div class="w-20 bg-gray-200 rounded-full h-2 mr-2">
                  <div class="bg-emerald-500 h-2 rounded-full" style="width: {{LIABILITY_PROGRESS}}%"></div>
                </div>
                <span class="text-xs text-gray-500">{{LIABILITY_PROGRESS}}%</span>
              </div>
            </td>
          </tr>
          {{/LIABILITIES}}
        </tbody>
        <tfoot>
          <tr class="bg-gray-50">
            <td colspan="2" class="py-3 font-semibold text-gray-700">總負債</td>
            <td class="py-3 text-right font-bold text-red-600">{{LIABILITY_TOTAL}}</td>
            <td class="py-3 text-right font-medium text-gray-600">{{MONTHLY_PAYMENT_TOTAL}}</td>
            <td></td>
          </tr>
        </tfoot>
      </table>
    </div>

    <!-- 淨資產趨勢 -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-6">
      <h2 class="text-lg font-semibold text-gray-700 mb-4">淨資產趨勢</h2>
      <div class="space-y-2">
        {{#HISTORY}}
        <div class="flex items-center">
          <span class="w-24 text-sm text-gray-600">{{HISTORY_DATE}}</span>
          <div class="flex-1 mx-3">
            <div class="w-full bg-gray-200 rounded-full h-4 relative">
              <div class="{{HISTORY_BAR_COLOR}} h-4 rounded-full" style="width: {{HISTORY_BAR_WIDTH}}%"></div>
            </div>
          </div>
          <span class="w-32 text-sm text-right {{HISTORY_VALUE_COLOR}}">{{HISTORY_VALUE}}</span>
        </div>
        {{/HISTORY}}
      </div>
    </div>

    <!-- 財務健康指標 -->
    <div class="bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg shadow-md p-6 text-white mb-6">
      <h2 class="text-lg font-semibold mb-4">財務健康指標</h2>
      <div class="grid grid-cols-3 gap-4">
        <div class="text-center">
          <div class="text-3xl font-bold">{{DEBT_RATIO}}</div>
          <div class="text-sm opacity-80">負債比率</div>
        </div>
        <div class="text-center">
          <div class="text-3xl font-bold">{{LIQUID_RATIO}}</div>
          <div class="text-sm opacity-80">流動性比率</div>
        </div>
        <div class="text-center">
          <div class="text-3xl font-bold">{{MONTHS_RUNWAY}}</div>
          <div class="text-sm opacity-80">財務跑道(月)</div>
        </div>
      </div>
    </div>

    <!-- 目標進度 -->
    {{#HAS_GOALS}}
    <div class="bg-white rounded-lg shadow-md p-6 mb-6">
      <h2 class="text-lg font-semibold text-gray-700 mb-4">財務目標</h2>
      {{#GOALS}}
      <div class="mb-4 last:mb-0">
        <div class="flex justify-between items-center mb-2">
          <span class="font-medium text-gray-800">{{GOAL_NAME}}</span>
          <span class="text-sm text-gray-500">目標：{{GOAL_TARGET}} | 期限：{{GOAL_DEADLINE}}</span>
        </div>
        <div class="w-full bg-gray-200 rounded-full h-3">
          <div class="{{GOAL_BAR_COLOR}} h-3 rounded-full" style="width: {{GOAL_PROGRESS}}%"></div>
        </div>
        <div class="text-right text-sm text-gray-500 mt-1">目前：{{GOAL_CURRENT}} ({{GOAL_PROGRESS}}%)</div>
      </div>
      {{/GOALS}}
    </div>
    {{/HAS_GOALS}}

    <!-- 頁尾 -->
    <div class="text-center text-gray-400 text-sm mt-6">
      由 Asset Tracker 產生 | {{GENERATED_TIME}}
    </div>
  </div>
</body>
</html>
```

## 顏色對照

### 淨資產漸層
- 正值：`from-emerald-500 to-teal-500`
- 負值：`from-red-500 to-orange-500`

### 負債類型標籤
- 房貸：`bg-blue-100 text-blue-700`
- 信貸：`bg-purple-100 text-purple-700`
- 車貸：`bg-amber-100 text-amber-700`
- 信用卡：`bg-pink-100 text-pink-700`
- 其他：`bg-gray-100 text-gray-700`

### 資產配置顏色
- 銀行：`bg-emerald-500`
- 加密貨幣：`bg-orange-500`
- 股票：`bg-blue-500`
- 其他：`bg-gray-400`

### 損益顏色
- 正值：`text-emerald-600`
- 負值：`text-red-600`
