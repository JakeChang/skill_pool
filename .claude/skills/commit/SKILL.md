---
name: commit
description: 請建立 git commit，不要在 commit 訊息中加入 "Generated with [Claude Code]" 或 "Co-Authored-By: Claude" 等標記。
---

# Git Commit 技能

建立簡潔、符合規範的 git commit。

## 工作流程

1. 執行 `git status` 和 `git diff` 查看變更
2. 分析變更內容，撰寫清晰簡潔的 commit 訊息
3. 執行 `git add .` 加入變更的檔案
4. 執行 `git commit -m` 建立 commit

## Commit 訊息格式

```
<type>: <簡短描述>

- <詳細變更項目 1>
- <詳細變更項目 2>
- <詳細變更項目 3>
```

**type 類型：**
- `feat` - 新功能
- `fix` - 錯誤修復
- `refactor` - 重構
- `chore` - 雜項維護
- `docs` - 文件更新
- `style` - 格式調整
- `test` - 測試相關

## 完成後

執行 `git log -1 --stat` 顯示剛建立的 commit 詳情。

---

## 更新技能

### `/commit update`
更新本機的 commit skill 到最新版本。

**步驟：**
1. 使用 AskUserQuestion 詢問使用者要更新哪個位置：
   - 全域（~/.claude/）：更新所有專案共用的 skills
   - 當前專案（./.claude/）：只更新當前專案的 skills

2. 根據選擇設定目標路徑

3. 執行更新流程：
   ```bash
   rm -rf /tmp/skill_pool
   git clone --depth 1 https://github.com/JakeChang/skill_pool.git /tmp/skill_pool
   ```

4. 複製 commit skill 到目標位置：
   ```bash
   mkdir -p <目標路徑>/skills
   cp -r /tmp/skill_pool/.claude/skills/commit <目標路徑>/skills/
   ```

5. 清理臨時檔案：
   ```bash
   rm -rf /tmp/skill_pool
   ```

6. 顯示更新結果

**輸出範例：**
```
[更新完成] commit 已更新至最新版本

更新位置：~/.claude/skills/commit
```
