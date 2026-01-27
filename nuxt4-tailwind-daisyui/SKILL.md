---
name: nuxt4-tailwind-daisyui
description: 建立 Nuxt 4 + TailwindCSS + DaisyUI 專案的初始化技能。當使用者需要：(1) 建立新的 Nuxt 4 專案、(2) 設定 TailwindCSS 與 DaisyUI 環境、(3) 初始化含有現代 CSS 框架的 Nuxt 專案時使用。
---

# Nuxt 4 + TailwindCSS + DaisyUI 專案初始化

此技能用於快速建立包含 TailwindCSS 與 DaisyUI 的 Nuxt 4 專案。

## 工作流程

### 1. 建立 Nuxt 4 專案

```bash
npm create nuxt <project-name>
cd <project-name>
```

### 2. 安裝依賴套件

```bash
npm install tailwindcss@latest @tailwindcss/vite@latest daisyui@latest
```

### 3. 設定檔案

執行 `scripts/setup.sh` 或手動建立以下檔案：

#### nuxt.config.ts

將現有設定替換為：

```typescript
import tailwindcss from "@tailwindcss/vite";

export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  vite: {
    plugins: [tailwindcss()],
  },
  css: ["./app/tailwind.css"],
})
```

#### app/tailwind.css

建立此檔案：

```css
@import "tailwindcss";
@plugin "daisyui";
```

#### app/app.vue

更新為：

```vue
<template>
  <div>
    <NuxtPage />
  </div>
</template>
```

#### app/pages/index.vue

建立測試頁面（可參考 `assets/index.vue`）：

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

## 資源

- `scripts/setup.sh` - 自動化設定腳本
- `assets/nuxt.config.ts` - nuxt.config.ts 範本
- `assets/tailwind.css` - tailwind.css 範本
- `assets/app.vue` - app.vue 範本
- `assets/index.vue` - 測試頁面範本

---

## 更新技能

### `/nuxt4-tailwind-daisyui update`
更新本機的 nuxt4-tailwind-daisyui skill 到最新版本。

```bash
npx openskills update
```
