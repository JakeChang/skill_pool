# 書籍筆記 JSON Schema

## 資料儲存

- 位置：專案根目錄 `data/`
- 命名：`{book-slug}.json`（小寫、連字號）
- 日期格式：ISO 8601（YYYY-MM-DD）

## 完整結構

```json
{
  "id": "unique-book-id",
  "title": "書名",
  "author": "作者",
  "isbn": "ISBN（選填）",
  "startDate": "2024-01-15",
  "endDate": "2024-02-10",
  "status": "reading | completed",
  "chapters": [
    {
      "number": 1,
      "title": "章節標題",
      "notes": ["重點1", "重點2"],
      "quotes": ["引用句子"],
      "thoughts": "個人想法",
      "dateRecorded": "2024-01-16"
    }
  ],
  "summary": {
    "mainIdeas": ["主要觀點"],
    "keyTakeaways": ["關鍵收穫"],
    "analysis": "深度分析文字",
    "rating": 5,
    "recommendation": "推薦理由",
    "generatedAt": "2024-02-10"
  },
  "tags": ["分類標籤"],
  "createdAt": "2024-01-15",
  "updatedAt": "2024-02-10"
}
```

## 欄位說明

| 欄位 | 類型 | 必填 | 說明 |
|------|------|------|------|
| id | string | 是 | 書名的 slug 格式 |
| title | string | 是 | 書名 |
| author | string | 是 | 作者 |
| isbn | string | 否 | ISBN 編號 |
| startDate | string | 是 | 開始閱讀日期 |
| endDate | string | 否 | 完成閱讀日期 |
| status | string | 是 | `reading` 或 `completed` |
| chapters | array | 是 | 章節陣列 |
| summary | object | 否 | 書籍摘要（完成時填寫） |
| tags | array | 否 | 分類標籤 |
| createdAt | string | 是 | 建立日期 |
| updatedAt | string | 是 | 更新日期 |
