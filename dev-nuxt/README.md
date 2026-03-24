# dev-nuxt

Nuxt 模組化開發技能，涵蓋需求規劃、計劃書撰寫、模組開發與瀏覽器測試。

適用於任何 Nuxt 4 專案，遵循四層式架構（Pages → Composables → Services → Utils）。

## 安裝

```bash
npx openskills install JakeChang/skill_pool/dev-nuxt
npx openskills sync
```

## 指令

| 指令 | 用途 | 產出 |
|------|------|------|
| `/dev-nuxt plan` | 分析需求、定義功能範圍 | `docs/requirements/{module}.md` |
| `/dev-nuxt spec` | 規劃技術方案、列出檔案清單 | `docs/specs/{module}.md` |
| `/dev-nuxt dev` | 依四層架構開發模組 | 模組程式碼 |
| `/dev-nuxt review` | 檢查程式碼是否符合架構規範 | 審查報告 |
| `/dev-nuxt test` | 透過 Chrome 瀏覽器實際操作測試 | 測試報告 |

## 搭配使用

建議搭配 [nuxt4-tailwind-daisyui](../nuxt4-tailwind-daisyui/) 一起使用：

1. 先用 `nuxt4-tailwind-daisyui` 建立專案
2. 再用 `dev-nuxt` 的指令進行開發

## 授權

MIT
