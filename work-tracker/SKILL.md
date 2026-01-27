---
name: work-tracker
description: |
  個人工作記錄與目標追蹤工具。記錄每日工作、設定月/季/年度目標、產生行事曆視圖報表。

  使用時機：
  (1) 記錄每日工作項目
  (2) 設定或查看目標（月度、季度、年度）
  (3) 追蹤目標進度
  (4) 產生工作行事曆報表

  觸發詞：工作記錄、work tracker、目標追蹤、工作日誌
---

# Work Tracker

個人工作記錄與目標追蹤工具。

## 初始化檢查

**每次執行指令前，先檢查 `work-tracker/goals/` 資料夾：**

```
如果 goals/ 不存在或為空 → 執行初始化流程
否則 → 執行指令
```

### 初始化流程

使用 `AskUserQuestion` 依序詢問使用者設定目標：

1. **年度目標**：「你的 {年} 年度目標是什麼？（可設定多個，用逗號分隔）」
2. **季度目標**：「你的 {年} Q{季} 季度目標是什麼？」
3. **月度目標**：「你的 {年} 年 {月} 月目標是什麼？」

建立對應的目標檔案後，再執行原本的指令。

## 資料儲存

所有資料儲存在專案根目錄的 `work-tracker/` 資料夾。

詳細 JSON 結構請見 [references/schema.md](references/schema.md)。

## 指令

### add - 新增工作

```
/work-tracker add <工作內容>
```

1. 讀取或建立 `work-tracker/daily/{今日日期}.json`
2. 新增 entry，狀態設為 `pending`
3. 顯示新增結果

### today - 查看今日

```
/work-tracker today
```

讀取今日的 JSON 檔案，以表格顯示：

```
| ID     | 工作內容       | 狀態      |
|--------|---------------|-----------|
| a1b2c3 | 完成 API 文件  | completed |
| d4e5f6 | 開會討論需求   | pending   |
```

### done - 標記完成

```
/work-tracker done <id>
```

將指定 ID 的工作狀態改為 `completed`。

### goal - 目標管理

**設定目標：**
```
/work-tracker goal set <weekly|monthly|quarterly|yearly> <目標內容>
```

**更新進度：**
```
/work-tracker goal update <id> <進度%>
```

**查看目標：**
```
/work-tracker goal list
```

顯示所有目標及進度：

```
## 2026 年度目標
| ID     | 目標           | 進度 |
|--------|---------------|------|
| g1h2i3 | 完成新功能開發  | 45%  |

## 2026 Q1 季度目標
...

## 2026-01 月度目標
...
```

**重新初始化：**
```
/work-tracker goal init
```

重新執行初始化流程，設定新目標。

### calendar - 產生行事曆

```
/work-tracker calendar [YYYY-MM]
```

1. 讀取 `assets/calendar-template.html` 模板
2. 讀取指定月份的所有 daily JSON
3. 讀取相關目標（月度、季度、年度）
4. 替換模板變數：
   - `{{MONTH_TITLE}}` - 月份標題
   - `{{GOALS_CONTENT}}` - 目標進度 HTML
   - `{{CALENDAR_DAYS}}` - 日曆格子 HTML
   - `{{TOTAL_TASKS}}` - 總工作數
   - `{{COMPLETED_TASKS}}` - 已完成數
   - `{{COMPLETION_RATE}}` - 完成率
5. 儲存至 `work-tracker/calendar/YYYY-MM.html`

### update - 更新技能

```
/work-tracker update
```

```bash
npx openskills update
```

## 資源

- `references/schema.md` - JSON 資料結構定義
- `assets/calendar-template.html` - 行事曆 HTML 模板
