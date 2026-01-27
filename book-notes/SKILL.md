---
name: book-notes
description: 個人閱讀筆記管理系統。用於記錄書籍章節重點、生成摘要與分析。當用戶提到「閱讀筆記」、「讀書筆記」、「書籍筆記」、「記錄這本書」、「章節重點」、「書籍摘要」時使用此 Skill。
---

# 閱讀筆記管理系統

管理個人閱讀筆記，支援章節記錄、摘要生成和 HTML 輸出。

## 資料結構

- 儲存位置：`data/{book-slug}.json`
- 詳細 schema：見 [references/schema.md](references/schema.md)

## 工作流程

### 新增書籍

1. 詢問書名和作者
2. 建立 `data/{slug}.json`，設定 `status: "reading"`
3. id 使用書名 slug（小寫、連字號）

### 記錄章節

1. 讀取現有 JSON
2. 解析用戶提供的重點、引用、想法
3. 新增章節到 `chapters` 陣列
4. 儲存並回報進度

### 生成摘要

當用戶說「完成閱讀」或「生成摘要」：

1. 讀取所有章節筆記
2. 生成 `mainIdeas`、`keyTakeaways`、`analysis`
3. 詢問評分（1-5）與推薦理由
4. 設定 `status: "completed"`

### 查看書籍列表

使用 Glob 讀取 `data/*.json`，列出書籍與狀態。

### 生成 HTML

1. 讀取 [assets/html-templates.md](assets/html-templates.md) 取得模板
2. 用書籍資料填充模板變數
3. 輸出到 `output/` 目錄：
   - `index.html` - 書籍列表
   - `{book-id}.html` - 書籍詳情
