---
name: cartoon-notes
description: 個人動畫卡通觀看紀錄管理系統。用於記錄動畫每集心得、生成摘要與分析，並可搜尋網路補充資訊。當用戶提到「動畫筆記」、「卡通紀錄」、「追番紀錄」、「記錄這部動畫」、「集數心得」、「動畫摘要」、「看了XX動畫」時使用此 Skill。
---

# 動畫觀看紀錄系統

管理個人動畫觀看紀錄，支援：記錄心得、生成摘要、搜尋補充資訊、輸出 HTML。

## 資料位置

**重要：所有資料必須儲存在本 skill 目錄內的指定資料夾。**

**禁止事項：**
- **絕對禁止** 將任何紀錄或設定檔案寫入 `.claude/` 目錄
- **絕對禁止** 使用 `.claude/memories/`、`.claude/settings/` 或任何 `.claude/` 子目錄
- 如果資料夾不存在，請先建立它

**正確的檔案位置：**
- 紀錄檔：`cartoon-notes/{anime-slug}.json`
- HTML 輸出：`cartoon-notes/reports/`

## 資源文件

### 參考文件（references/）
- **JSON 結構**：[schema.md](references/schema.md) - 資料格式規格
- **網路搜尋**：[web-search.md](references/web-search.md) - 搜尋策略指南

### 模板素材（assets/）
- **HTML 模板**：[html-templates.md](assets/html-templates.md) - 輸出頁面模板

---

## 核心工作流程

### 1. 新增動畫

用戶說「記錄《動畫名》」或「新增動畫 XXX」時：

1. 詢問基本資訊（名稱、製作公司、年份）
2. 建立 `cartoon-notes/{slug}.json`，status 設為 `watching`
3. id 使用 slug 格式（小寫、連字號）

### 2. 記錄集數心得

用戶說「記錄第 X 集」或「看了芙莉蓮第 X 集」時：

1. 讀取現有 JSON
2. 解析心得內容，填入結構化欄位
3. 儲存回 JSON
4. **主動詢問**是否搜尋網路補充資訊（參考 [web-search.md](references/web-search.md)）

### 3. 生成摘要

用戶說「完成觀看」或「生成摘要」時：

1. 讀取所有季/集筆記
2. 生成 summary 區塊（plot, themes, bestEpisodes 等）
3. 詢問整體評分（1-5）與推薦理由
4. 更新 status 為 `completed`

### 4. 查看列表

用戶說「我的動畫」或「追番列表」時：

1. 用 Glob 讀取 `cartoon-notes/*.json`
2. 列出清單，顯示狀態與進度

### 5. 生成 HTML

用戶說「生成 HTML」或「輸出網頁」時：

1. 讀取 JSON 資料
2. 依照 [html-templates.md](assets/html-templates.md) 生成 HTML
3. 使用 Write 工具輸出到 `cartoon-notes/reports/`

---

## 注意事項

- 檔案命名：slug 格式（小寫、連字號）
- 日期格式：ISO 8601（YYYY-MM-DD）
- HTML 生成：直接用 Write 工具，無需腳本
- 網路搜尋：記錄後主動詢問，避免打擾
