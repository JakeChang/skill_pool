# Skill Pool

Claude Code 技能集合。

## 安裝

**安裝到當前專案：**

```bash
git clone --depth 1 https://github.com/JakeChang/skill_pool.git /tmp/skill_pool && cp -r /tmp/skill_pool/.claude ./ && rm -rf /tmp/skill_pool
```

**安裝到全域（所有專案皆可使用）：**

```bash
git clone --depth 1 https://github.com/JakeChang/skill_pool.git /tmp/skill_pool && cp -r /tmp/skill_pool/.claude ~/ && rm -rf /tmp/skill_pool
```

## 技能列表

### 開發工具

| 技能 | 說明 | 文件 |
|------|------|------|
| commit | 建立標準化的 git commit | [README](.claude/skills/commit/README.md) |
| skill-creator | 建立 Claude Code 技能的輔助工具 | [README](.claude/skills/skill-creator/README.md) |
| swagger-tracker | Swagger/OpenAPI 文件追蹤與版本比較 | [README](.claude/skills/swagger-tracker/README.md) |

### 專案模板

| 技能 | 說明 | 文件 |
|------|------|------|
| nuxt4-tailwind-daisyui | 快速建立 Nuxt 4 + TailwindCSS + DaisyUI 專案 | [README](.claude/skills/nuxt4-tailwind-daisyui/README.md) |

### 生活應用

| 技能 | 說明 | 文件 |
|------|------|------|
| diet-tracker | 專業營養追蹤與健康顧問 | [README](.claude/skills/diet-tracker/README.md) |

## 目錄結構

```
.claude/
└── skills/
    ├── commit/                  # Git commit 工具
    ├── skill-creator/           # 技能建立工具
    ├── swagger-tracker/         # Swagger API 文件追蹤
    ├── nuxt4-tailwind-daisyui/  # Nuxt 專案初始化
    └── diet-tracker/            # 營養追蹤顧問
```

## 授權

MIT
