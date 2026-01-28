# HTML 行事曆首頁範本

產生 `diet-tracker/reports/index.html` 作為所有報告的入口頁面。

## 報告內容
1. 標題與當月摘要
2. 月份選擇器
3. 月曆格式顯示（週日到週六）
4. 每日格子顯示健康分數，點擊可連結到當日報告
5. 月份統計摘要

## HTML 範本

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>營養追蹤日曆 - {{YEAR}}年{{MONTH}}月</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 min-h-screen py-8">
  <div class="max-w-4xl mx-auto px-4">

    <!-- 標題 -->
    <div class="bg-gradient-to-r from-emerald-500 to-teal-500 rounded-lg shadow-md p-6 mb-6 text-white">
      <div class="flex justify-between items-center">
        <div>
          <h1 class="text-2xl font-bold">營養追蹤日曆</h1>
          <p class="opacity-80">記錄每一天的健康旅程</p>
        </div>
        <div class="text-center">
          <div class="text-3xl font-bold">{{YEAR}}年{{MONTH}}月</div>
        </div>
      </div>
    </div>

    <!-- 月份導航 -->
    <div class="bg-white rounded-lg shadow-md p-4 mb-6">
      <div class="flex justify-between items-center">
        <a href="{{PREV_MONTH_FILE}}" class="px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded-lg text-gray-700 {{PREV_DISABLED}}">
          [<] 上個月
        </a>
        <span class="text-lg font-semibold text-gray-700">{{YEAR}}年{{MONTH}}月</span>
        <a href="{{NEXT_MONTH_FILE}}" class="px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded-lg text-gray-700 {{NEXT_DISABLED}}">
          下個月 [>]
        </a>
      </div>
    </div>

    <!-- 月份統計 -->
    <div class="grid grid-cols-4 gap-4 mb-6">
      <div class="bg-white rounded-lg shadow-md p-4 text-center">
        <div class="text-sm text-gray-500">記錄天數</div>
        <div class="text-2xl font-bold text-emerald-600">{{RECORDED_DAYS}}</div>
      </div>
      <div class="bg-white rounded-lg shadow-md p-4 text-center">
        <div class="text-sm text-gray-500">平均分數</div>
        <div class="text-2xl font-bold text-blue-600">{{AVG_SCORE}}</div>
      </div>
      <div class="bg-white rounded-lg shadow-md p-4 text-center">
        <div class="text-sm text-gray-500">平均熱量</div>
        <div class="text-2xl font-bold text-amber-600">{{AVG_CALORIES}}</div>
      </div>
      <div class="bg-white rounded-lg shadow-md p-4 text-center">
        <div class="text-sm text-gray-500">平均蛋白質</div>
        <div class="text-2xl font-bold text-red-500">{{AVG_PROTEIN}}g</div>
      </div>
    </div>

    <!-- 日曆 -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-6">
      <!-- 星期標題 -->
      <div class="grid grid-cols-7 gap-2 mb-4">
        <div class="text-center text-sm font-semibold text-red-400 py-2">日</div>
        <div class="text-center text-sm font-semibold text-gray-600 py-2">一</div>
        <div class="text-center text-sm font-semibold text-gray-600 py-2">二</div>
        <div class="text-center text-sm font-semibold text-gray-600 py-2">三</div>
        <div class="text-center text-sm font-semibold text-gray-600 py-2">四</div>
        <div class="text-center text-sm font-semibold text-gray-600 py-2">五</div>
        <div class="text-center text-sm font-semibold text-blue-400 py-2">六</div>
      </div>

      <!-- 日期格子 -->
      <div class="grid grid-cols-7 gap-2">
        {{#CALENDAR_DAYS}}
        {{/CALENDAR_DAYS}}
      </div>
    </div>

    <!-- 圖例說明 -->
    <div class="bg-white rounded-lg shadow-md p-4 mb-6">
      <h3 class="text-sm font-semibold text-gray-700 mb-3">健康分數圖例</h3>
      <div class="flex flex-wrap gap-4 text-sm">
        <div class="flex items-center">
          <div class="w-6 h-6 bg-emerald-500 rounded mr-2"></div>
          <span class="text-gray-600">80-100 優秀</span>
        </div>
        <div class="flex items-center">
          <div class="w-6 h-6 bg-green-400 rounded mr-2"></div>
          <span class="text-gray-600">60-79 良好</span>
        </div>
        <div class="flex items-center">
          <div class="w-6 h-6 bg-amber-400 rounded mr-2"></div>
          <span class="text-gray-600">40-59 普通</span>
        </div>
        <div class="flex items-center">
          <div class="w-6 h-6 bg-red-400 rounded mr-2"></div>
          <span class="text-gray-600">0-39 需改善</span>
        </div>
        <div class="flex items-center">
          <div class="w-6 h-6 bg-gray-200 rounded mr-2"></div>
          <span class="text-gray-600">無紀錄</span>
        </div>
      </div>
    </div>

    <!-- 頁尾 -->
    <div class="text-center text-gray-400 text-sm mt-6">
      由專業營養追蹤助手產生 | 基於 2025 營養科學
    </div>
  </div>
</body>
</html>
```

## 日期格子範本

### 有紀錄的日期（可點擊）
```html
<a href="{{DATE}}.html" class="block aspect-square rounded-lg {{BG_COLOR}} hover:opacity-80 transition-opacity p-2 text-center">
  <div class="text-sm {{TEXT_COLOR}}">{{DAY}}</div>
  <div class="text-lg font-bold {{SCORE_COLOR}}">{{SCORE}}</div>
  <div class="text-xs {{TEXT_COLOR}}">{{CALORIES}}kcal</div>
</a>
```

### 無紀錄的日期
```html
<div class="aspect-square rounded-lg bg-gray-100 p-2 text-center">
  <div class="text-sm text-gray-400">{{DAY}}</div>
</div>
```

### 空白格子（月初/月末填充）
```html
<div class="aspect-square"></div>
```

### 今天（特殊標記）
```html
<a href="{{DATE}}.html" class="block aspect-square rounded-lg {{BG_COLOR}} ring-2 ring-emerald-500 hover:opacity-80 transition-opacity p-2 text-center">
  <div class="text-sm {{TEXT_COLOR}}">[今天]</div>
  <div class="text-lg font-bold {{SCORE_COLOR}}">{{SCORE}}</div>
  <div class="text-xs {{TEXT_COLOR}}">{{CALORIES}}kcal</div>
</a>
```

## 顏色對應

根據健康分數設定背景色：
- 80-100: `bg-emerald-500 text-white`
- 60-79: `bg-green-400 text-white`
- 40-59: `bg-amber-400 text-gray-800`
- 0-39: `bg-red-400 text-white`
- 無紀錄: `bg-gray-100 text-gray-400`

## 檔案命名規則

- 首頁：`index.html`（顯示當月）
- 月份頁：`index-YYYY-MM.html`（歷史月份）
