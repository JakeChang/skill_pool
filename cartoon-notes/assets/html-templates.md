# HTML 模板參考

所有頁面使用 TailwindCSS CDN，深色主題配色。

## 基礎結構

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{頁面標題}} - 動畫觀看紀錄</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;500;700&display=swap');
        body { font-family: 'Noto Sans TC', sans-serif; }
    </style>
</head>
<body class="bg-slate-900 min-h-screen text-gray-100">
    {{內容}}
</body>
</html>
```

---

## 列表頁 (index.html)

```html
<div class="max-w-6xl mx-auto py-8 px-4">
    <!-- 標題區 -->
    <div class="text-center mb-12">
        <h1 class="text-4xl font-bold text-cyan-400 mb-4">我的動畫紀錄</h1>
        <p class="text-gray-400">記錄每一部追過的動畫，留下觀看的感動</p>
    </div>

    <!-- 統計區 -->
    <div class="grid grid-cols-4 gap-4 mb-12">
        <div class="bg-slate-800 rounded-xl shadow-lg p-6 text-center border border-slate-700">
            <p class="text-4xl font-bold text-cyan-400">{{總數}}</p>
            <p class="text-gray-400">動畫總數</p>
        </div>
        <div class="bg-slate-800 rounded-xl shadow-lg p-6 text-center border border-slate-700">
            <p class="text-4xl font-bold text-green-400">{{已完成}}</p>
            <p class="text-gray-400">已完成</p>
        </div>
        <div class="bg-slate-800 rounded-xl shadow-lg p-6 text-center border border-slate-700">
            <p class="text-4xl font-bold text-yellow-400">{{追番中}}</p>
            <p class="text-gray-400">追番中</p>
        </div>
        <div class="bg-slate-800 rounded-xl shadow-lg p-6 text-center border border-slate-700">
            <p class="text-4xl font-bold text-purple-400">{{總集數}}</p>
            <p class="text-gray-400">觀看集數</p>
        </div>
    </div>

    <!-- 動畫列表 -->
    <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {{動畫卡片們}}
    </div>
</div>
```

---

## 動畫卡片元件

```html
<div class="bg-slate-800 rounded-xl shadow-lg hover:shadow-cyan-500/20 transition-all hover:scale-105 p-6 border border-slate-700">
    <div class="flex justify-between items-start mb-4">
        <div>
            <h2 class="text-xl font-bold text-white">{{動畫名}}</h2>
            <p class="text-gray-400 text-sm">{{製作公司}}</p>
        </div>
        <!-- 狀態標籤 -->
        <span class="px-3 py-1 rounded-full text-sm font-medium {{狀態樣式}}">
            {{狀態文字}}
        </span>
    </div>

    <!-- 類型標籤 -->
    <div class="flex flex-wrap gap-2 mb-4">
        {{類型標籤們}}
    </div>

    <!-- 進度條 -->
    <div class="mb-4">
        <div class="flex justify-between text-sm text-gray-400 mb-1">
            <span>觀看進度</span>
            <span>{{已看集數}}/{{總集數}}</span>
        </div>
        <div class="w-full bg-slate-700 rounded-full h-2">
            <div class="bg-cyan-500 h-2 rounded-full" style="width: {{進度百分比}}%"></div>
        </div>
    </div>

    <div class="flex justify-between items-center text-sm text-gray-400">
        <span>{{年份}}</span>
        <span class="text-yellow-400">{{星級評分}}</span>
    </div>
    <a href="{{動畫ID}}.html" class="mt-4 block text-center bg-cyan-600 text-white py-2 px-4 rounded-lg hover:bg-cyan-700 transition-colors">
        查看詳情
    </a>
</div>
```

### 狀態樣式

- 追番中：`bg-yellow-500/20 text-yellow-400`
- 已完成：`bg-green-500/20 text-green-400`

### 類型標籤顏色

```html
<span class="px-2 py-1 rounded text-xs bg-pink-500/20 text-pink-400">奇幻</span>
<span class="px-2 py-1 rounded text-xs bg-blue-500/20 text-blue-400">冒險</span>
<span class="px-2 py-1 rounded text-xs bg-purple-500/20 text-purple-400">劇情</span>
<span class="px-2 py-1 rounded text-xs bg-green-500/20 text-green-400">日常</span>
<span class="px-2 py-1 rounded text-xs bg-red-500/20 text-red-400">動作</span>
<span class="px-2 py-1 rounded text-xs bg-orange-500/20 text-orange-400">喜劇</span>
```

### 星級評分

```html
<span class="text-yellow-400">★★★★★</span>
<span class="text-yellow-400">★★★<span class="text-slate-600">☆☆</span></span>
```

---

## 動畫詳細頁 ({anime-id}.html)

```html
<div class="max-w-4xl mx-auto py-8 px-4">
    <!-- 動畫標題區 -->
    <div class="bg-slate-800 rounded-xl shadow-lg p-8 mb-8 border border-slate-700">
        <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
            <div>
                <h1 class="text-3xl font-bold text-white mb-2">{{動畫名}}</h1>
                <p class="text-gray-400">{{原文標題}}</p>
                <p class="text-lg text-cyan-400 mt-2">{{製作公司}}</p>
            </div>
            <div class="flex flex-col items-end gap-2">
                <span class="px-4 py-2 rounded-full text-sm font-medium {{狀態樣式}}">
                    {{狀態文字}}
                </span>
                <span class="text-yellow-400 text-xl">{{星級評分}}</span>
            </div>
        </div>

        <div class="flex flex-wrap gap-2 mt-4">
            {{類型標籤們}}
        </div>

        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6 pt-6 border-t border-slate-700">
            <div class="text-center">
                <p class="text-sm text-gray-500">播出年份</p>
                <p class="font-medium text-white">{{年份}}</p>
            </div>
            <div class="text-center">
                <p class="text-sm text-gray-500">季數</p>
                <p class="font-medium text-white">{{季數}}</p>
            </div>
            <div class="text-center">
                <p class="text-sm text-gray-500">觀看集數</p>
                <p class="font-medium text-white">{{觀看集數}}</p>
            </div>
            <div class="text-center">
                <p class="text-sm text-gray-500">導演</p>
                <p class="font-medium text-white">{{導演}}</p>
            </div>
        </div>
    </div>

    <!-- 摘要區（僅已完成的動畫顯示）-->
    {{摘要區塊}}

    <!-- 季/集筆記 -->
    <h2 class="text-2xl font-bold text-white mb-6">觀看紀錄</h2>
    {{季列表}}

    <!-- 頁尾 -->
    <div class="text-center text-gray-500 text-sm mt-8 pt-8 border-t border-slate-700">
        <p>建立於 {{建立日期}} | 最後更新 {{更新日期}}</p>
    </div>
</div>
```

---

## 摘要區塊（僅已完成的動畫）

```html
<div class="bg-gradient-to-br from-cyan-900/50 to-purple-900/50 rounded-xl p-8 mb-8 border border-cyan-500/30">
    <h2 class="text-2xl font-bold text-white mb-6">動畫總評與分析</h2>

    <div class="bg-slate-800/50 rounded-lg p-5 mb-6">
        <h3 class="font-bold text-cyan-400 mb-3">劇情概要</h3>
        <p class="text-gray-300 leading-relaxed">{{劇情概要}}</p>
    </div>

    <div class="grid md:grid-cols-2 gap-6 mb-6">
        <div class="bg-slate-800/50 rounded-lg p-5">
            <h3 class="font-bold text-pink-400 mb-3">主題分析</h3>
            <ul class="list-disc list-inside space-y-2">
                <li class="text-gray-300">{{主題}}</li>
            </ul>
        </div>
        <div class="bg-slate-800/50 rounded-lg p-5">
            <h3 class="font-bold text-green-400 mb-3">最愛角色</h3>
            <ul class="list-disc list-inside space-y-2">
                <li class="text-gray-300">{{角色}}</li>
            </ul>
        </div>
    </div>

    <div class="bg-slate-800/50 rounded-lg p-5 mb-6">
        <h3 class="font-bold text-purple-400 mb-3">最佳集數</h3>
        <p class="text-gray-300">第 {{季}} 季第 {{集}} 集：{{原因}}</p>
    </div>

    <div class="bg-slate-800/50 rounded-lg p-5 mb-6">
        <h3 class="font-bold text-yellow-400 mb-3">深度分析</h3>
        <p class="text-gray-300 leading-relaxed">{{分析內容}}</p>
    </div>

    <div class="bg-slate-800/50 rounded-lg p-5">
        <div class="flex justify-between items-center mb-3">
            <h3 class="font-bold text-orange-400">推薦評價</h3>
            <span class="text-yellow-400 text-xl">{{星級評分}}</span>
        </div>
        <p class="text-gray-300">{{推薦理由}}</p>
    </div>
</div>
```

---

## 季區塊

```html
<div class="mb-8">
    <div class="flex items-center gap-4 mb-4">
        <h3 class="text-xl font-bold text-cyan-400">第 {{季數}} 季</h3>
        <span class="text-gray-400">{{季標題}}</span>
        <span class="text-yellow-400">{{季評分}}</span>
    </div>

    <!-- 季總評（如果有）-->
    <div class="bg-slate-800/30 rounded-lg p-4 mb-4 border-l-4 border-cyan-500">
        <p class="text-gray-300">{{季總評}}</p>
    </div>

    <!-- 集數列表 -->
    <div class="space-y-4">
        {{集卡片們}}
    </div>
</div>
```

---

## 集卡片

```html
<div class="bg-slate-800 rounded-xl shadow-lg p-6 border border-slate-700">
    <div class="flex justify-between items-center mb-4">
        <h4 class="text-lg font-bold text-white">
            EP{{集數}}：{{集標題}}
        </h4>
        <div class="flex items-center gap-4">
            <span class="text-yellow-400">{{集評分}}</span>
            <span class="text-sm text-gray-500">{{觀看日期}}</span>
        </div>
    </div>

    <!-- 精彩片段 -->
    <div class="mb-4">
        <h5 class="font-medium text-cyan-400 mb-2">精彩片段</h5>
        <ul class="list-disc list-inside space-y-1">
            <li class="text-gray-300">{{精彩片段}}</li>
        </ul>
    </div>

    <!-- 喜愛場景（如果有）-->
    <div class="mb-4">
        <h5 class="font-medium text-pink-400 mb-2">喜愛場景</h5>
        <p class="text-gray-300">{{場景描述}}</p>
    </div>

    <!-- 本集重點角色（如果有）-->
    <div class="mb-4">
        <h5 class="font-medium text-green-400 mb-2">重點角色</h5>
        <div class="flex flex-wrap gap-2">
            <span class="px-2 py-1 rounded bg-slate-700 text-gray-300 text-sm">{{角色}}</span>
        </div>
    </div>

    <!-- 經典台詞（如果有）-->
    <div class="mb-4">
        <h5 class="font-medium text-purple-400 mb-2">經典台詞</h5>
        <blockquote class="border-l-4 border-purple-500 pl-4 italic text-gray-400 my-2">
            "{{台詞內容}}"
        </blockquote>
    </div>

    <!-- 心得感想 -->
    <div class="bg-cyan-900/20 p-4 rounded-lg mt-4 border border-cyan-500/30">
        <h5 class="font-medium text-cyan-400 mb-2">心得感想</h5>
        <p class="text-gray-300">{{心得感想}}</p>
    </div>
</div>
```
