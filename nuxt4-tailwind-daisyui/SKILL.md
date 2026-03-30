---
name: nuxt4-tailwind-daisyui
description: 建立 Nuxt 4 + TailwindCSS + DaisyUI 專案的初始化技能。當使用者需要：(1) 建立新的 Nuxt 4 專案、(2) 設定 TailwindCSS 與 DaisyUI 環境、(3) 初始化含有現代 CSS 框架的 Nuxt 專案時使用。
---

# Nuxt 4 + TailwindCSS + DaisyUI 專案初始化

此技能用於快速建立包含 TailwindCSS 4 與 DaisyUI 5 的 Nuxt 4 專案。

## 重要版本資訊

- **Nuxt**: 目前 npm 上最新為 3.x（如 3.16.0），尚無 Nuxt 4 正式套件。需透過 `future.compatibilityVersion: 4` 啟用 Nuxt 4 行為。
- **Tailwind CSS**: v4，使用 `@tailwindcss/vite` 作為 Vite 插件整合
- **DaisyUI**: v5，透過 Tailwind 的 `@plugin` 語法載入

## 重要：nuxi init 的正確用法

`nuxi init` 預設會進入互動模式，**必須**加上以下參數避免卡住：

```bash
npx nuxi@latest init <project-name> --packageManager npm --no-gitInit 2>&1
```

- **不要**指定 `--template` 參數（預設 template 就是正確的，`v4-minimal` 等自訂名稱不存在會 404）
- **必須**加 `--packageManager npm` 避免互動式選擇套件管理器
- **必須**加 `--no-gitInit` 避免互動式選擇是否初始化 git
- **必須**加 `2>&1` 將 stderr 導向 stdout，否則看不到輸出
- 此指令會自動執行 `npm install`，不需要再手動 `npm install`

## 工作流程

### 1. 建立 Nuxt 專案

```bash
npx nuxi@latest init <project-name> --packageManager npm --no-gitInit 2>&1
cd <project-name>
```

### 2. 安裝額外依賴套件

```bash
npm install -D tailwindcss@4 @tailwindcss/vite daisyui@5
```

### 3. 設定檔案

#### nuxt.config.ts

```typescript
import tailwindcss from "@tailwindcss/vite";

export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  future: {
    compatibilityVersion: 4,
  },
  devtools: { enabled: true },
  vite: {
    plugins: [tailwindcss()],
  },
  css: ["~/tailwind.css"],
})
```

關鍵設定說明：
- `future.compatibilityVersion: 4` — 啟用 Nuxt 4 行為模式（路由、目錄結構等）
- `css: ["~/tailwind.css"]` — 使用 Nuxt 的 `~` alias（解析到 app/ 目錄），不要用相對路徑 `./app/tailwind.css`

#### app/tailwind.css

```css
@import "tailwindcss";
@plugin "daisyui";
```

#### tsconfig.json（專案根目錄）

```json
{
  "extends": "./.nuxt/tsconfig.json"
}
```

#### app/app.vue

```vue
<template>
  <div>
    <NuxtPage />
  </div>
</template>
```

#### app/pages/index.vue

建立測試頁面驗證 DaisyUI 是否正常運作：

```vue
<template>
  <div class="p-8">
    <h1 class="text-3xl font-bold mb-4">Nuxt 4 + DaisyUI</h1>
    <button class="btn btn-primary mr-2">Primary</button>
    <button class="btn btn-secondary">Secondary</button>
    <div class="card w-96 bg-base-100 shadow-xl mt-8">
      <div class="card-body">
        <h2 class="card-title">Card Title</h2>
        <p>DaisyUI card component works!</p>
        <div class="card-actions justify-end">
          <button class="btn btn-primary">Buy Now</button>
        </div>
      </div>
    </div>
  </div>
</template>
```

### 4. 啟動開發伺服器

```bash
npm run dev
```

## 常見問題

### 路由不生效 / 頁面空白
確認 `nuxt.config.ts` 有設定 `future.compatibilityVersion: 4`，Nuxt 4 相容模式會改變目錄解析方式。

### CSS 載入失敗
確認 CSS 路徑使用 `~/tailwind.css` 而非 `./app/tailwind.css`，`~` alias 在 Nuxt 4 模式下指向 `app/` 目錄。

## 資源

- `scripts/setup.sh` - 自動化設定腳本
- `assets/` - 各檔案範本
