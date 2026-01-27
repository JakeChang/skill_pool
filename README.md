# Skill Pool

Claude Code 技能集合。

## 安裝

使用 [openskills](https://github.com/numman-ali/openskills) CLI 安裝單一技能：

```bash
npx openskills install JakeChang/skill_pool/<skill-name>
npx openskills sync
```

例如安裝 commit 技能：

```bash
npx openskills install JakeChang/skill_pool/commit
npx openskills sync
```

## 技能列表

### 開發工具

| 技能 | 說明 | 文件 |
|------|------|------|
| commit | 建立標準化的 git commit | [README](commit/README.md) |
| skill-creator | 建立 Claude Code 技能的輔助工具 | [README](skill-creator/README.md) |
| swagger-tracker | Swagger/OpenAPI 文件追蹤與版本比較 | [README](swagger-tracker/README.md) |

### 專案模板

| 技能 | 說明 | 文件 |
|------|------|------|
| nuxt4-tailwind-daisyui | 快速建立 Nuxt 4 + TailwindCSS + DaisyUI 專案 | [README](nuxt4-tailwind-daisyui/README.md) |

### 生活應用

| 技能 | 說明 | 文件 |
|------|------|------|
| diet-tracker | 專業營養追蹤與健康顧問 | [README](diet-tracker/README.md) |
| work-tracker | 個人工作記錄與目標追蹤 | [README](work-tracker/README.md) |
| book-notes | 個人閱讀筆記管理系統 | [README](book-notes/README.md) |
| cartoon-notes | 動畫卡通觀看紀錄管理 | [README](cartoon-notes/README.md) |

## 目錄結構

```
skill_pool/
├── commit/                  # Git commit 工具
├── skill-creator/           # 技能建立工具
├── swagger-tracker/         # Swagger API 文件追蹤
├── nuxt4-tailwind-daisyui/  # Nuxt 專案初始化
├── diet-tracker/            # 營養追蹤顧問
├── work-tracker/            # 工作記錄追蹤
├── book-notes/              # 閱讀筆記管理
└── cartoon-notes/           # 動畫觀看紀錄
```

## 授權

MIT
