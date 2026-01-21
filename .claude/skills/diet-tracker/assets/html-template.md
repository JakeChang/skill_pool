# HTML 每日報告範本

每次更新飲食紀錄後，產生一份 HTML 報告。使用 Tailwind CSS CDN。

## 報告內容
1. 日期標題
2. 健康評分卡（大數字顯示）
3. 熱量進度條
4. 營養素統計卡片（蛋白質、碳水、脂肪、纖維、Omega-3）
5. 蛋白質分配圖表（各餐是否達標）
6. 每餐詳細紀錄
7. 今日亮點與改善建議

## HTML 範本

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>營養報告 - {{DATE}}</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 min-h-screen py-8">
  <div class="max-w-2xl mx-auto px-4">

    <!-- 標題與健康評分 -->
    <div class="bg-gradient-to-r from-emerald-500 to-teal-500 rounded-lg shadow-md p-6 mb-6 text-white">
      <div class="flex justify-between items-center">
        <div>
          <h1 class="text-2xl font-bold">營養報告</h1>
          <p class="opacity-80">{{DATE}}</p>
        </div>
        <div class="text-center">
          <div class="text-5xl font-bold">{{HEALTH_SCORE}}</div>
          <div class="text-sm opacity-80">健康分數</div>
        </div>
      </div>
    </div>

    <!-- 熱量進度 -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-6">
      <div class="flex justify-between items-center mb-2">
        <span class="text-lg font-semibold text-gray-700">今日熱量</span>
        <span class="text-lg font-bold {{CALORIE_COLOR}}">{{TOTAL_CALORIES}} / {{GOAL_CALORIES}} kcal</span>
      </div>
      <div class="w-full bg-gray-200 rounded-full h-4">
        <div class="{{PROGRESS_BG}} h-4 rounded-full transition-all duration-300" style="width: {{CALORIE_PERCENT}}%"></div>
      </div>
      <p class="text-sm text-gray-500 mt-2">{{CALORIE_STATUS}}</p>
    </div>

    <!-- 主要營養素卡片 -->
    <div class="grid grid-cols-3 gap-4 mb-6">
      <div class="bg-white rounded-lg shadow-md p-4 text-center">
        <div class="text-2xl mb-1 font-bold text-red-400">[P]</div>
        <div class="text-sm text-gray-500">蛋白質</div>
        <div class="text-xl font-bold text-red-500">{{PROTEIN}}g</div>
        <div class="text-xs text-gray-400">目標 {{PROTEIN_GOAL}}g</div>
      </div>
      <div class="bg-white rounded-lg shadow-md p-4 text-center">
        <div class="text-2xl mb-1 font-bold text-yellow-400">[C]</div>
        <div class="text-sm text-gray-500">碳水</div>
        <div class="text-xl font-bold text-yellow-500">{{CARBS}}g</div>
        <div class="text-xs text-gray-400">目標 {{CARBS_GOAL}}g</div>
      </div>
      <div class="bg-white rounded-lg shadow-md p-4 text-center">
        <div class="text-2xl mb-1 font-bold text-green-400">[F]</div>
        <div class="text-sm text-gray-500">脂肪</div>
        <div class="text-xl font-bold text-green-500">{{FAT}}g</div>
        <div class="text-xs text-gray-400">目標 {{FAT_GOAL}}g</div>
      </div>
    </div>

    <!-- 進階營養素卡片 -->
    <div class="grid grid-cols-2 gap-4 mb-6">
      <div class="bg-white rounded-lg shadow-md p-4">
        <div class="flex items-center justify-between">
          <div>
            <div class="text-sm text-gray-500">纖維</div>
            <div class="text-xl font-bold text-amber-600">{{FIBER}}g</div>
          </div>
          <div class="text-xl font-bold text-amber-400">[Fiber]</div>
        </div>
        <div class="w-full bg-gray-200 rounded-full h-2 mt-2">
          <div class="bg-amber-500 h-2 rounded-full" style="width: {{FIBER_PERCENT}}%"></div>
        </div>
        <div class="text-xs text-gray-400 mt-1">目標 {{FIBER_GOAL}}g</div>
      </div>
      <div class="bg-white rounded-lg shadow-md p-4">
        <div class="flex items-center justify-between">
          <div>
            <div class="text-sm text-gray-500">Omega-3</div>
            <div class="text-xl font-bold text-blue-600">{{OMEGA3}}g</div>
          </div>
          <div class="text-xl font-bold text-blue-400">[O3]</div>
        </div>
        <div class="w-full bg-gray-200 rounded-full h-2 mt-2">
          <div class="bg-blue-500 h-2 rounded-full" style="width: {{OMEGA3_PERCENT}}%"></div>
        </div>
        <div class="text-xs text-gray-400 mt-1">目標 {{OMEGA3_GOAL}}g</div>
      </div>
    </div>

    <!-- 蛋白質分配 -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-6">
      <h2 class="text-lg font-semibold text-gray-700 mb-4">蛋白質分配（亮氨酸門檻）</h2>
      <div class="space-y-3">
        {{#PROTEIN_DISTRIBUTION}}
        <div class="flex items-center">
          <span class="w-16 text-sm text-gray-600">{{MEAL_NAME}}</span>
          <div class="flex-1 mx-3">
            <div class="w-full bg-gray-200 rounded-full h-3">
              <div class="{{MEAL_BAR_COLOR}} h-3 rounded-full" style="width: {{MEAL_PROTEIN_PERCENT}}%"></div>
            </div>
          </div>
          <span class="w-20 text-sm text-right {{MEAL_TEXT_COLOR}}">{{MEAL_PROTEIN}}g {{MEAL_STATUS}}</span>
        </div>
        {{/PROTEIN_DISTRIBUTION}}
      </div>
      <p class="text-xs text-gray-500 mt-3">* 每餐建議 30-40g 蛋白質以達到亮氨酸門檻（2.5-3g）</p>
    </div>

    <!-- 餐點紀錄 -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-6">
      <h2 class="text-lg font-semibold text-gray-700 mb-4">今日餐點</h2>
      {{#MEALS}}
      <div class="border-b border-gray-100 pb-4 mb-4 last:border-0 last:pb-0 last:mb-0">
        <div class="flex justify-between items-center mb-2">
          <span class="font-medium text-gray-800">{{MEAL_TYPE}}</span>
          <span class="text-sm text-gray-500">{{MEAL_TIME}}</span>
        </div>
        {{#ITEMS}}
        <div class="flex justify-between items-center text-sm py-1">
          <div>
            <span class="text-gray-600">{{ITEM_NAME}} ({{ITEM_QUANTITY}})</span>
            {{#ITEM_TAGS}}
            <span class="ml-2 px-2 py-0.5 bg-emerald-100 text-emerald-700 text-xs rounded-full">{{TAG}}</span>
            {{/ITEM_TAGS}}
          </div>
          <span class="text-gray-500">{{ITEM_CALORIES}} kcal</span>
        </div>
        {{/ITEMS}}
        <div class="flex justify-end mt-2">
          <span class="text-sm font-medium text-blue-600">小計：{{MEAL_TOTAL}} kcal</span>
        </div>
      </div>
      {{/MEALS}}
    </div>

    <!-- 抗發炎指數 -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-6">
      <div class="flex justify-between items-center">
        <div>
          <h2 class="text-lg font-semibold text-gray-700">抗發炎指數</h2>
          <p class="text-sm text-gray-500">正分=抗發炎，負分=促發炎</p>
        </div>
        <div class="text-3xl font-bold {{INFLAMMATION_COLOR}}">{{INFLAMMATION_SCORE}}</div>
      </div>
    </div>

    <!-- 今日建議 -->
    <div class="bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg shadow-md p-6 text-white mb-6">
      <h2 class="text-lg font-semibold mb-2">[TIP] 今日建議</h2>
      <p>{{DAILY_SUGGESTION}}</p>
    </div>

    <!-- 快速改善提示 -->
    <div class="bg-amber-50 border border-amber-200 rounded-lg p-4 mb-6">
      <h3 class="font-semibold text-amber-800 mb-2">[!] 快速提升健康分數</h3>
      <ul class="text-sm text-amber-700 space-y-1">
        {{#IMPROVEMENT_TIPS}}
        <li>* {{TIP}}</li>
        {{/IMPROVEMENT_TIPS}}
      </ul>
    </div>

    <!-- 頁尾 -->
    <div class="text-center text-gray-400 text-sm mt-6">
      由專業營養追蹤助手產生 | 基於 2025 營養科學
    </div>
  </div>
</body>
</html>
```
