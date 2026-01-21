# Nuxt 4 + TailwindCSS + DaisyUI 使用指南

在 Claude Code 中快速建立 Nuxt 4 專案並整合 TailwindCSS 與 DaisyUI。

## 安裝

**安裝到當前專案：**

```bash
git clone --depth 1 https://github.com/JakeChang/skill_pool.git /tmp/skill_pool && mkdir -p .claude/skills && cp -r /tmp/skill_pool/.claude/skills/nuxt4-tailwind-daisyui .claude/skills/ && rm -rf /tmp/skill_pool
```

**安裝到全域：**

```bash
git clone --depth 1 https://github.com/JakeChang/skill_pool.git /tmp/skill_pool && mkdir -p ~/.claude/skills && cp -r /tmp/skill_pool/.claude/skills/nuxt4-tailwind-daisyui ~/.claude/skills/ && rm -rf /tmp/skill_pool
```

## 如何觸發此技能

在 Claude Code 對話中，說明你想要建立 Nuxt 專案：

```
幫我建立一個 Nuxt 4 專案
```

```
建立一個有 TailwindCSS 和 DaisyUI 的 Nuxt 專案叫 my-app
```

```
初始化一個 Nuxt 4 + DaisyUI 的前端專案
```

## 使用範例

### 建立新專案

**你說：**
> 幫我建立一個叫 my-website 的 Nuxt 4 專案，要有 TailwindCSS 和 DaisyUI

**Claude 會：**
1. 執行 `npm create nuxt my-website` 建立專案
2. 安裝 TailwindCSS 和 DaisyUI 依賴
3. 設定 `nuxt.config.ts`
4. 建立 `app/tailwind.css`
5. 更新 `app/app.vue`
6. 建立測試頁面 `app/pages/index.vue`
7. 啟動開發伺服器

### 在現有專案加入 TailwindCSS + DaisyUI

**你說：**
> 幫我在這個 Nuxt 專案加入 TailwindCSS 和 DaisyUI

**Claude 會：**
1. 安裝必要的依賴套件
2. 更新 `nuxt.config.ts` 設定
3. 建立 CSS 檔案

## 專案結構

建立完成後的專案結構：

```
my-website/
├── app/
│   ├── app.vue           # 主應用元件
│   ├── tailwind.css      # TailwindCSS + DaisyUI 設定
│   └── pages/
│       └── index.vue     # 首頁（含 DaisyUI 元件範例）
├── nuxt.config.ts        # Nuxt 設定檔
└── package.json
```

## 技術棧

| 套件 | 用途 |
|------|------|
| Nuxt 4 | Vue 3 全端框架 |
| TailwindCSS | Utility-first CSS 框架 |
| @tailwindcss/vite | Vite 整合插件 |
| DaisyUI | TailwindCSS 元件庫 |

## 常用指令

```bash
# 啟動開發伺服器
npm run dev

# 建置生產版本
npm run build

# 預覽生產版本
npm run preview
```

## 相關檔案

| 檔案 | 說明 |
|------|------|
| `scripts/setup.sh` | 自動化設定腳本 |
| `assets/nuxt.config.ts` | nuxt.config.ts 範本 |
| `assets/tailwind.css` | tailwind.css 範本 |
| `assets/app.vue` | app.vue 範本 |
| `assets/index.vue` | 測試頁面範本 |
