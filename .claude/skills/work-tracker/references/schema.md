# Work Tracker 資料結構

## 資料夾結構

```
work-tracker/
├── daily/
│   └── YYYY-MM-DD.json
├── goals/
│   ├── YYYY.json        # 年度目標
│   ├── YYYY-QN.json     # 季度目標
│   └── YYYY-MM.json     # 月度目標
└── calendar/
    └── YYYY-MM.html     # 行事曆報表
```

## JSON Schema

### 每日記錄 (daily/YYYY-MM-DD.json)

```json
{
  "date": "2026-01-22",
  "entries": [
    {
      "id": "a1b2c3",
      "task": "完成 API 文件",
      "status": "completed",
      "createdAt": "09:30"
    }
  ]
}
```

| 欄位 | 類型 | 說明 |
|------|------|------|
| date | string | 日期 YYYY-MM-DD |
| entries | array | 工作項目列表 |
| entries[].id | string | 唯一識別碼（6 碼） |
| entries[].task | string | 工作內容 |
| entries[].status | string | pending / completed |
| entries[].createdAt | string | 建立時間 HH:MM |

### 目標 (goals/*.json)

```json
{
  "period": "2026-Q1",
  "type": "quarterly",
  "goals": [
    {
      "id": "g1h2i3",
      "title": "完成新功能開發",
      "progress": 45,
      "createdAt": "2026-01-01"
    }
  ]
}
```

| 欄位 | 類型 | 說明 |
|------|------|------|
| period | string | 週期標識（2026 / 2026-Q1 / 2026-01） |
| type | string | yearly / quarterly / monthly |
| goals | array | 目標列表 |
| goals[].id | string | 唯一識別碼（6 碼） |
| goals[].title | string | 目標標題 |
| goals[].progress | number | 進度 0-100 |
| goals[].createdAt | string | 建立日期 |

## ID 生成規則

使用 6 碼隨機英數字：`a-z0-9`
