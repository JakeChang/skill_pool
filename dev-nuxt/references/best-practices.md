# Nuxt 最佳實踐

Nuxt 開發關鍵規則，依優先順序排列。

## 目錄

- [1. 資料取得與 SSR](#1-資料取得與-ssr最高優先) — useFetch、$fetch、key 管理、payload 最小化
- [2. Hydration 一致性](#2-hydration-一致性) — 瀏覽器 API、確定性渲染、第三方庫
- [3. 架構邊界](#3-架構邊界) — 機密 server-only、request-safe 狀態、敏感 I/O
- [4. 錯誤處理](#4-錯誤處理) — 全域/區域 error boundary、Nuxt 錯誤工具
- [5. 頁面 Meta 與 Layout](#5-頁面-meta-與-layout) — definePageMeta vs useHead
- [6. 效能](#6-效能) — NuxtLink、route rules、lazy loading
- [7. Server Routes 與 Runtime Config](#7-server-routes-與-runtime-config) — 輸入驗證、runtimeConfig
- [8. Plugins](#8-plugins) — composable 優先、async parallel
- [9. 抽象層選擇](#9-抽象層選擇) — 框架原生 API 優先

---

## 1. 資料取得與 SSR（最高優先）

### 初始資料用 `useFetch` / `useAsyncData`

頁面初始渲染需要的資料，必須使用 Nuxt 的資料取得 composable，讓資料透過 payload 傳遞。

```typescript
// 正確：SSR payload 傳遞，無重複請求
const { data, status, error } = useFetch('/api/orders')

// 錯誤：SSR + CSR 各請求一次
onMounted(async () => {
  const data = await $fetch('/api/orders')
})
```

### `$fetch` 用於互動操作

使用者點擊、表單送出等事件驅動的請求，用 `$fetch` 或 service 層。

### 保持 key 明確且一致

跨元件共用 `useAsyncData` 時，使用明確穩定的 key，避免自動生成 key 導致衝突。

```typescript
// 明確 key
const { data } = useAsyncData('order-list', () => $fetch('/api/orders'))
```

### 最小化 payload

用 `pick` / `transform` 只傳遞模板需要的欄位，減少 SSR payload 大小。

```typescript
const { data } = useFetch('/api/orders', {
  pick: ['id', 'name', 'status'],
})
```

---

## 2. Hydration 一致性

### 不在 SSR 路徑中使用瀏覽器 API

`window`、`document`、`localStorage` 等只能在客戶端使用。

```typescript
// 正確
onMounted(() => {
  const width = window.innerWidth
})

// 正確：使用 Nuxt 的 SSR 安全替代品
const cookie = useCookie('token')

// 錯誤：SSR 時會崩潰
const width = window.innerWidth  // 在 setup 中直接使用
```

### 第一次渲染必須確定性

不要在模板中直接使用 `new Date()`、`Math.random()` 等非確定性值。

```typescript
// 正確：用 useState 共享初始值
const now = useState('now', () => new Date().toISOString())

// 錯誤：SSR 與 CSR 的值不同，觸發 hydration mismatch
const now = new Date().toLocaleString()
```

### 第三方 DOM 操作庫在 mount 後初始化

```typescript
// 正確
onMounted(() => {
  initChart(chartRef.value)
})

// 錯誤：在 setup 中直接初始化
initChart(document.getElementById('chart'))
```

---

## 3. 架構邊界

### 機密資訊只能在 server 端

API key、token 等敏感資訊只能在 `server/` 目錄下使用。

```typescript
// 正確：server/api/orders.ts
const config = useRuntimeConfig()
const apiKey = config.secretApiKey  // 不在 public 中

// 錯誤：在 composable 中使用密鑰
const apiKey = useRuntimeConfig().public.apiKey  // 暴露給客戶端
```

### 使用 request-safe 的狀態管理

SSR 環境下每個請求獨立，不能用模組層級的可變全域變數。

```typescript
// 正確：每次請求獨立
const useCounter = () => useState('counter', () => 0)

// 錯誤：所有請求共用同一個變數（SSR 會跨請求洩漏）
let counter = 0
export const useCounter = () => counter
```

### 敏感 I/O 放在 server 入口

資料庫查詢、第三方 API 呼叫統一放在 `server/api/` 下。

---

## 4. 錯誤處理

### 同時處理全域與區域錯誤

- 全域：`app/error.vue`（整頁錯誤）
- 區域：`<NuxtErrorBoundary>`（元件級錯誤，不影響整頁）

```vue
<template>
  <NuxtErrorBoundary>
    <OrderTable :orders="orders" />
    <template #error="{ error, clearError }">
      <div class="alert alert-error">
        {{ error.message }}
        <button @click="clearError">重試</button>
      </div>
    </template>
  </NuxtErrorBoundary>
</template>
```

### 使用 Nuxt 錯誤工具

用 `clearError`、`showError` 而非自行重設狀態，避免不一致。

---

## 5. 頁面 Meta 與 Layout

### `definePageMeta` vs `useHead` 分工

| API | 用途 | 範例 |
|-----|------|------|
| `definePageMeta` | 頁面行為 | layout、middleware、transition、keepalive |
| `useHead` | 文件 head | link、script、style |
| `useSeoMeta` | SEO metadata | title、description、og:image |

```typescript
// 頁面行為
definePageMeta({
  layout: 'dashboard',
  middleware: ['auth'],
})

// SEO
useSeoMeta({
  title: '訂單管理',
  description: '管理所有訂單',
})
```

### Layout 用於共享結構

重複的 header、sidebar、footer 放在 `layouts/` 中，不要在每個頁面複製。

---

## 6. 效能

### 內部連結用 `NuxtLink`

```vue
<!-- 正確：自動 prefetch -->
<NuxtLink to="/orders">訂單管理</NuxtLink>

<!-- 錯誤：失去 prefetch 與 SPA 導航 -->
<a href="/orders">訂單管理</a>
```

### 依內容特性設定 route rules

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  routeRules: {
    '/': { prerender: true },           // 靜態首頁
    '/dashboard/**': { ssr: false },    // 純客戶端
    '/blog/**': { swr: 3600 },         // 每小時重新驗證
  },
})
```

### 延遲載入非關鍵元件

```vue
<!-- 自動 lazy loading -->
<LazyOrderChart v-if="showChart" />

<!-- 可見時才 hydrate -->
<LazyHeavyWidget hydrate-on-visible />
```

---

## 7. Server Routes 與 Runtime Config

### 在 handler 邊界驗證輸入

```typescript
// server/api/orders.post.ts
export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  if (!body.name?.trim()) {
    throw createError({ statusCode: 400, message: '名稱為必填' })
  }
  // ...處理邏輯
})
```

### `runtimeConfig.public` 最小化

只暴露客戶端真正需要的設定，其餘放在 `runtimeConfig`（server-only）。

---

## 8. Plugins

### 優先用 composable，非必要不建 plugin

Plugin 參與每次啟動/hydration，增加全域成本。只有真正需要 app 層級注入時才用。

### 獨立的 async plugin 設定 parallel

```typescript
// plugins/analytics.ts
export default defineNuxtPlugin({
  parallel: true,  // 不依賴其他 plugin，可並行
  async setup() {
    // ...
  },
})
```

---

## 9. 抽象層選擇

### 優先使用框架原生 API

遇到問題時，先找 Nuxt 是否已提供解決方案，再考慮通用 Vue 或原生 HTML。

| 需求 | 框架方案 | 避免 |
|------|----------|------|
| Cookie | `useCookie` | `document.cookie` |
| 路由連結 | `NuxtLink` | `<a>` + `router.push` |
| 初始資料 | `useFetch` | `onMounted` + `$fetch` |
| 頁面 title | `useSeoMeta` | `document.title = ...` |
| 狀態共享 | `useState` | 模組層級變數 |

### 不要只看視覺結果

手寫 HTML 可能看起來正確，但如果繞過了框架原生元件，可能失去 SSR、prefetch、型別安全等優勢。
