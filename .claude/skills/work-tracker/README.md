# Work Tracker 使用指南

個人工作記錄與目標追蹤工具。記錄每日工作、設定月/季/年度目標、產生行事曆視圖報表。

## 安裝

**安裝到當前專案：**

```bash
git clone --depth 1 https://github.com/JakeChang/skill_pool.git /tmp/skill_pool && mkdir -p .claude/skills && cp -r /tmp/skill_pool/.claude/skills/work-tracker .claude/skills/ && rm -rf /tmp/skill_pool
```

**安裝到全域：**

```bash
git clone --depth 1 https://github.com/JakeChang/skill_pool.git /tmp/skill_pool && mkdir -p ~/.claude/skills && cp -r /tmp/skill_pool/.claude/skills/work-tracker ~/.claude/skills/ && rm -rf /tmp/skill_pool
```

## 指令一覽

| 指令 | 說明 |
|------|------|
| `/work-tracker add [工作內容]` | 新增今日工作 |
| `/work-tracker today` | 查看今日記錄 |
| `/work-tracker done [id]` | 標記工作完成 |
| `/work-tracker goal set [週期] [目標]` | 設定目標 |
| `/work-tracker goal update [id] [進度%]` | 更新目標進度 |
| `/work-tracker goal list` | 查看所有目標 |
| `/work-tracker goal init` | 重新初始化目標 |
| `/work-tracker calendar [YYYY-MM]` | 產生行事曆 HTML |
| `/work-tracker update` | 更新到最新版本 |

## 使用範例

### 記錄工作

```
/work-tracker add 完成 API 文件撰寫
```

輸出：
```
已新增工作：

| ID     | 工作內容           | 狀態    |
|--------|-------------------|---------|
| a1b2c3 | 完成 API 文件撰寫  | pending |
```

### 查看今日記錄

```
/work-tracker today
```

輸出：
```
2026-01-22 今日工作：

| ID     | 工作內容           | 狀態      |
|--------|-------------------|-----------|
| a1b2c3 | 完成 API 文件撰寫  | pending   |
| d4e5f6 | 開會討論需求       | completed |
```

### 標記完成

```
/work-tracker done a1b2c3
```

### 設定目標

```
/work-tracker goal set quarterly 完成 Phase3 功能開發
/work-tracker goal set monthly 完成報表模組
/work-tracker goal set yearly 提升程式碼品質
```

**週期選項：** `weekly`、`monthly`、`quarterly`、`yearly`

### 更新目標進度

```
/work-tracker goal update bst50p 30
```

### 產生行事曆

```
/work-tracker calendar 2026-01
```

產生 `work-tracker/calendar/2026-01.html`，包含：
- 月曆視圖顯示每日工作
- 目標進度條
- 完成率統計

## 資料儲存

所有紀錄儲存在專案根目錄的 `./work-tracker/`：

```
work-tracker/
├── daily/
│   ├── 2026-01-22.json      # 每日工作記錄
│   └── ...
├── goals/
│   ├── 2026.json            # 年度目標
│   ├── 2026-Q1.json         # 季度目標
│   └── 2026-01.json         # 月度目標
└── calendar/
    └── 2026-01.html         # 行事曆報表
```

## 核心功能

- **每日記錄**：快速記錄工作項目，追蹤完成狀態
- **目標管理**：設定月度、季度、年度目標，手動更新進度
- **行事曆視圖**：產生 HTML 報表，以月曆格式呈現工作分佈
- **初始化引導**：首次使用自動詢問目標設定

## 相關檔案

| 檔案 | 說明 |
|------|------|
| `references/schema.md` | JSON 資料結構定義 |
| `assets/calendar-template.html` | 行事曆 HTML 模板 |
