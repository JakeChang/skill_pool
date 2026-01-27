# HTML 模板參考

所有頁面使用 TailwindCSS CDN 和 Noto Sans TC 字型。

## 基礎 HTML 結構

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{頁面標題}} - 閱讀筆記</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;500;700&display=swap');
        body { font-family: 'Noto Sans TC', sans-serif; }
    </style>
</head>
<body class="bg-gray-50 min-h-screen">
    {{內容}}
</body>
</html>
```

## 書籍列表頁 (index.html)

```html
<div class="max-w-6xl mx-auto py-8 px-4">
    <!-- 標題區 -->
    <div class="text-center mb-12">
        <h1 class="text-4xl font-bold text-gray-800 mb-4">我的閱讀筆記</h1>
        <p class="text-gray-600">記錄閱讀的每一本書，累積知識的每一步</p>
    </div>

    <!-- 統計區 -->
    <div class="grid grid-cols-3 gap-4 mb-12">
        <div class="bg-white rounded-xl shadow-md p-6 text-center">
            <p class="text-4xl font-bold text-indigo-600">{{總數}}</p>
            <p class="text-gray-600">書籍總數</p>
        </div>
        <div class="bg-white rounded-xl shadow-md p-6 text-center">
            <p class="text-4xl font-bold text-green-600">{{已完成}}</p>
            <p class="text-gray-600">已完成</p>
        </div>
        <div class="bg-white rounded-xl shadow-md p-6 text-center">
            <p class="text-4xl font-bold text-yellow-600">{{閱讀中}}</p>
            <p class="text-gray-600">閱讀中</p>
        </div>
    </div>

    <!-- 書籍列表 -->
    <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {{書籍卡片們}}
    </div>
</div>
```

## 書籍卡片元件

```html
<div class="bg-white rounded-xl shadow-md hover:shadow-lg transition-shadow p-6">
    <div class="flex justify-between items-start mb-4">
        <div>
            <h2 class="text-xl font-bold text-gray-800">{{書名}}</h2>
            <p class="text-gray-600">{{作者}}</p>
        </div>
        <!-- 狀態標籤：閱讀中用 bg-yellow-100 text-yellow-800，已完成用 bg-green-100 text-green-800 -->
        <span class="px-3 py-1 rounded-full text-sm font-medium {{狀態樣式}}">
            {{狀態文字}}
        </span>
    </div>
    <!-- 標籤 -->
    <div class="flex flex-wrap gap-2 mb-4">
        {{標籤們}}
    </div>
    <div class="flex justify-between items-center text-sm text-gray-500">
        <span>章節數: {{章節數}}</span>
        <span class="text-yellow-500">{{星級評分}}</span>
    </div>
    <a href="{{書籍ID}}.html" class="mt-4 block text-center bg-indigo-600 text-white py-2 px-4 rounded-lg hover:bg-indigo-700 transition-colors">
        查看詳情
    </a>
</div>
```

## 標籤元件（輪替顏色）

```html
<span class="px-2 py-1 rounded text-xs bg-blue-100 text-blue-800">{{標籤}}</span>
<span class="px-2 py-1 rounded text-xs bg-green-100 text-green-800">{{標籤}}</span>
<span class="px-2 py-1 rounded text-xs bg-purple-100 text-purple-800">{{標籤}}</span>
<span class="px-2 py-1 rounded text-xs bg-pink-100 text-pink-800">{{標籤}}</span>
<span class="px-2 py-1 rounded text-xs bg-orange-100 text-orange-800">{{標籤}}</span>
```

## 星級評分

```html
<!-- 5星 -->
<span class="text-yellow-500">★★★★★</span>
<!-- 3星 -->
<span class="text-yellow-500">★★★☆☆</span>
```

## 書籍詳細頁 ({book-id}.html)

```html
<div class="max-w-4xl mx-auto py-8 px-4">
    <!-- 書籍標題區 -->
    <div class="bg-white rounded-xl shadow-lg p-8 mb-8">
        <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
            <div>
                <h1 class="text-3xl font-bold text-gray-800 mb-2">{{書名}}</h1>
                <p class="text-xl text-gray-600">作者：{{作者}}</p>
            </div>
            <div class="flex flex-col items-end gap-2">
                <span class="px-4 py-2 rounded-full text-sm font-medium {{狀態樣式}}">
                    {{狀態文字}}
                </span>
                <span class="text-yellow-500">{{星級評分}}</span>
            </div>
        </div>

        <div class="flex flex-wrap gap-2 mt-4">
            {{標籤們}}
        </div>

        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6 pt-6 border-t">
            <div class="text-center">
                <p class="text-sm text-gray-500">開始日期</p>
                <p class="font-medium">{{開始日期}}</p>
            </div>
            <div class="text-center">
                <p class="text-sm text-gray-500">完成日期</p>
                <p class="font-medium">{{完成日期}}</p>
            </div>
            <div class="text-center">
                <p class="text-sm text-gray-500">章節數</p>
                <p class="font-medium">{{章節數}}</p>
            </div>
            <div class="text-center">
                <p class="text-sm text-gray-500">ISBN</p>
                <p class="font-medium text-sm">{{ISBN}}</p>
            </div>
        </div>
    </div>

    <!-- 摘要區（僅已完成的書顯示）-->
    {{摘要區塊}}

    <!-- 章節筆記 -->
    <h2 class="text-2xl font-bold text-gray-800 mb-6">章節筆記</h2>
    {{章節列表}}

    <!-- 頁尾 -->
    <div class="text-center text-gray-500 text-sm mt-8 pt-8 border-t">
        <p>建立於 {{建立日期}} | 最後更新 {{更新日期}}</p>
    </div>
</div>
```

## 摘要區塊（僅已完成的書）

```html
<div class="bg-gradient-to-br from-indigo-50 to-purple-50 rounded-xl p-8 mb-8">
    <h2 class="text-2xl font-bold text-gray-800 mb-6">書籍摘要與分析</h2>

    <div class="grid md:grid-cols-2 gap-6 mb-6">
        <div class="bg-white rounded-lg p-5 shadow-sm">
            <h3 class="font-bold text-indigo-700 mb-3">主要觀點</h3>
            <ul class="list-disc list-inside space-y-2">
                <li class="text-gray-700">{{觀點}}</li>
            </ul>
        </div>

        <div class="bg-white rounded-lg p-5 shadow-sm">
            <h3 class="font-bold text-green-700 mb-3">關鍵收穫</h3>
            <ul class="list-disc list-inside space-y-2">
                <li class="text-gray-700">{{收穫}}</li>
            </ul>
        </div>
    </div>

    <div class="bg-white rounded-lg p-5 shadow-sm mb-6">
        <h3 class="font-bold text-purple-700 mb-3">深度分析</h3>
        <p class="text-gray-700 leading-relaxed">{{分析內容}}</p>
    </div>

    <div class="bg-white rounded-lg p-5 shadow-sm">
        <div class="flex justify-between items-center mb-3">
            <h3 class="font-bold text-orange-700">推薦評價</h3>
            <span class="text-yellow-500">{{星級評分}}</span>
        </div>
        <p class="text-gray-700">{{推薦理由}}</p>
    </div>
</div>
```

## 章節卡片

```html
<div class="bg-white rounded-xl shadow-md p-6 mb-6">
    <div class="flex justify-between items-center mb-4">
        <h3 class="text-lg font-bold text-gray-800">
            第 {{章節號}} 章：{{章節標題}}
        </h3>
        <span class="text-sm text-gray-500">{{記錄日期}}</span>
    </div>

    <div class="mb-4">
        <h4 class="font-medium text-gray-700 mb-2">重點筆記</h4>
        <ul class="list-disc list-inside space-y-1">
            <li class="text-gray-700">{{重點}}</li>
        </ul>
    </div>

    <!-- 引用（如果有）-->
    <div class="mb-4">
        <h4 class="font-medium text-gray-700 mb-2">精選引用</h4>
        <blockquote class="border-l-4 border-indigo-500 pl-4 italic text-gray-600 my-2">
            "{{引用內容}}"
        </blockquote>
    </div>

    <!-- 個人想法（如果有）-->
    <div class="bg-yellow-50 p-4 rounded-lg mt-4">
        <h4 class="font-medium text-yellow-800 mb-2">個人想法</h4>
        <p class="text-gray-700">{{個人想法}}</p>
    </div>
</div>
```
