# Skill Creator 使用指南

在 Claude Code 中建立技能的輔助工具。

## 安裝

**安裝到當前專案：**

```bash
git clone --depth 1 https://github.com/JakeChang/skill_pool.git /tmp/skill_pool && mkdir -p .claude/skills && cp -r /tmp/skill_pool/.claude/skills/skill-creator .claude/skills/ && rm -rf /tmp/skill_pool
```

**安裝到全域：**

```bash
git clone --depth 1 https://github.com/JakeChang/skill_pool.git /tmp/skill_pool && mkdir -p ~/.claude/skills && cp -r /tmp/skill_pool/.claude/skills/skill-creator ~/.claude/skills/ && rm -rf /tmp/skill_pool
```

## 如何觸發此技能

在 Claude Code 對話中，直接說明你想要建立技能：

```
幫我建立一個處理 PDF 的技能
```

```
我想建立一個新技能來自動化部署流程
```

```
幫我更新現有的 api-helper 技能
```

Claude 會自動載入此技能並引導你完成建立流程。

## 使用範例

### 建立新技能

**你說：**
> 幫我在 .claude/skills 建立一個叫 pdf-editor 的技能

**Claude 會：**
1. 執行 `init_skill.py` 初始化技能目錄
2. 詢問技能的用途和功能
3. 協助撰寫 SKILL.md
4. 根據需求建立 scripts/references/assets

### 更新現有技能

**你說：**
> 幫我更新 .claude/skills/my-tool 的技能說明

**Claude 會：**
1. 讀取現有的 SKILL.md
2. 根據你的需求修改內容
3. 驗證修改後的結構

### 打包技能

**你說：**
> 幫我打包 .claude/skills/pdf-editor 技能

**Claude 會：**
1. 執行驗證腳本檢查技能結構
2. 打包成 `.skill` 檔案

## 技能結構

```
skill-name/
├── SKILL.md          # 必需 - 技能說明文件
├── scripts/          # 可選 - 可執行腳本
├── references/       # 可選 - 參考文件
└── assets/           # 可選 - 範本與資源
```

## SKILL.md 格式

```yaml
---
name: skill-name
description: 技能說明，描述功能與使用時機
---

# 技能標題

技能內容...
```

## 更新技能

```
/skill-creator update
```

將本機的 skill-creator skill 更新到最新版本。

## 相關檔案

| 檔案 | 說明 |
|------|------|
| `scripts/init_skill.py` | 初始化新技能 |
| `scripts/quick_validate.py` | 驗證技能結構 |
| `scripts/package_skill.py` | 打包成 .skill 檔案 |
| `references/workflows.md` | 工作流程設計模式 |
| `references/output-patterns.md` | 輸出格式範本 |
