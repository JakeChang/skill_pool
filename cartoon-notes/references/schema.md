# JSON 資料結構

每部動畫儲存為獨立 JSON 檔案，位於 `data/{anime-slug}.json`。

## 完整結構

```json
{
  "id": "anime-slug",
  "title": "動畫名稱",
  "titleOriginal": "原文標題（日文/英文）",
  "studio": "製作公司",
  "director": "導演（選填）",
  "year": "2024",
  "totalSeasons": 1,
  "status": "watching | completed | on-hold | dropped",
  "seasons": [
    {
      "seasonNumber": 1,
      "title": "季標題（選填）",
      "episodes": [
        {
          "episodeNumber": 1,
          "title": "集標題",
          "watchedDate": "YYYY-MM-DD",
          "rating": 5,
          "highlights": ["精彩片段"],
          "thoughts": "心得感想",
          "favoriteScenes": ["喜愛場景"],
          "characters": ["重點角色"],
          "quotes": ["經典台詞"],
          "notes": "補充資訊（選填）"
        }
      ],
      "seasonSummary": "本季總評（選填）",
      "seasonRating": 5
    }
  ],
  "summary": {
    "plot": "劇情概要",
    "themes": ["主題"],
    "bestEpisodes": [{"season": 1, "episode": 3, "reason": "原因"}],
    "favoriteCharacters": ["角色"],
    "analysis": "深度分析",
    "overallRating": 5,
    "recommendation": "推薦理由",
    "generatedAt": "YYYY-MM-DD"
  },
  "tags": ["標籤"],
  "genres": ["類型"],
  "createdAt": "YYYY-MM-DD",
  "updatedAt": "YYYY-MM-DD"
}
```

## 欄位說明

### 必填欄位

| 欄位 | 說明 |
|------|------|
| `id` | slug 格式，小寫英文加連字號 |
| `title` | 動畫中文名稱 |
| `studio` | 製作公司 |
| `status` | watching/completed/on-hold/dropped |
| `createdAt` | ISO 8601 日期 |
| `updatedAt` | ISO 8601 日期 |

### 集數欄位

| 欄位 | 必填 | 說明 |
|------|------|------|
| `episodeNumber` | ✓ | 集數編號 |
| `title` | ✓ | 集標題 |
| `watchedDate` | ✓ | 觀看日期 |
| `highlights` | ✓ | 精彩片段陣列 |
| `thoughts` | ✓ | 心得感想 |
| `rating` | | 1-5 評分 |
| `favoriteScenes` | | 喜愛場景陣列 |
| `characters` | | 重點角色陣列 |
| `quotes` | | 經典台詞陣列 |
| `notes` | | 補充資訊 |

### Summary 欄位（完成觀看後生成）

僅在 `status: "completed"` 時填寫：

| 欄位 | 說明 |
|------|------|
| `plot` | 整體劇情概要 |
| `themes` | 作品主題分析 |
| `bestEpisodes` | 最佳集數與原因 |
| `favoriteCharacters` | 最愛角色列表 |
| `analysis` | 深度分析文字 |
| `overallRating` | 整體評分 1-5 |
| `recommendation` | 推薦理由 |

## 命名規則

- 檔案名：`{slug}.json`（例：`frieren.json`）
- ID 格式：小寫英文、數字、連字號
- 日期格式：`YYYY-MM-DD`（ISO 8601）
