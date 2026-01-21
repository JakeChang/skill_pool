# Skill Pool

Claude Code 技能與命令集合。

## 安裝

**安裝到當前專案：**

```bash
git clone --depth 1 https://github.com/JakeChang/skill_pool.git /tmp/skill_pool && cp -r /tmp/skill_pool/.claude ./ && rm -rf /tmp/skill_pool
```

**安裝到全域（所有專案皆可使用）：**

```bash
git clone --depth 1 https://github.com/JakeChang/skill_pool.git /tmp/skill_pool && cp -r /tmp/skill_pool/.claude ~/ && rm -rf /tmp/skill_pool
```

## 命令

| 命令 | 說明 |
|------|------|
| `/commit` | 產生標準化的 git commit 訊息 |

## 技能

### skill-creator

建立 Claude Code 技能的輔助工具。

**觸發方式：**
```
幫我建立一個處理 PDF 的技能
```

**功能：**
- 初始化技能目錄結構
- 引導撰寫 SKILL.md
- 驗證與打包技能

### nuxt4-tailwind-daisyui

快速建立 Nuxt 4 + TailwindCSS + DaisyUI 專案。

**觸發方式：**
```
幫我建立一個 Nuxt 4 專案，要有 TailwindCSS 和 DaisyUI
```

**功能：**
- 建立 Nuxt 4 專案
- 安裝並設定 TailwindCSS + DaisyUI
- 產生測試頁面

## 目錄結構

```
.claude/
├── commands/
│   └── commit.md           # /commit 命令
└── skills/
    ├── skill-creator/      # 技能建立工具
    └── nuxt4-tailwind-daisyui/  # Nuxt 專案初始化
```

## 授權

MIT
