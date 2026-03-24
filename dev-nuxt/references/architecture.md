# 四層式架構參考

## 目錄

- [架構總覽](#架構總覽)
- [1. Service 層](#1-service-層) — $fetch 封裝，僅處理客戶端互動
- [2. Composable 層](#2-composable-層) — 檔案拆分、型別位置、主邏輯、表單、barrel export、回應格式
- [3. Utils 層](#3-utils-層)
- [4. 頁面層](#4-頁面層)
- [5. 路由與權限](#5-路由與權限) — middleware、error.vue、導航選單
- [命名規範](#命名規範)

---

## 架構總覽

```
頁面層 (Pages)  →  業務邏輯層 (Composables)  →  服務層 (Services)  →  工具層 (Utils)
  路由/佈局         狀態管理/業務邏輯            客戶端 CRUD 操作      純函式工具
```

依賴規則：上層可依賴下層，下層不可依賴上層。

---

## 1. Service 層

**路徑**：`app/service/{module}Service.ts`

**職責**：封裝客戶端互動的 `$fetch` 呼叫（表單送出、刪除、更新等）。頁面初始資料不經過 service 層，由 composable 直接使用 `useFetch`。

```
useFetch / useAsyncData → SSR 初始資料（composable 內直接呼叫）
service 層（$fetch）    → 客戶端 CRUD 操作（事件驅動，不需 SSR）
```

```typescript
// app/service/orderService.ts

// ===== 型別定義（API 相關）=====
export interface Order {
  id: number
  name: string
}

export interface CreateOrderRequest {
  name: string
}

// ===== Service 物件 =====
export const orderService = {
  createOrder: (data: CreateOrderRequest) =>
    $fetch<Order>('/api/orders', { method: 'POST', body: data }),

  updateOrder: (id: number, data: Partial<CreateOrderRequest>) =>
    $fetch<Order>(`/api/orders/${id}`, { method: 'PUT', body: data }),

  deleteOrder: (id: number) =>
    $fetch(`/api/orders/${id}`, { method: 'DELETE' }),
}
```

**規則**：
- 命名：`{module}Service.ts`，匯出 `{module}Service` 物件
- 使用 Nuxt 內建的 `$fetch`（基於 ofetch，支援型別推導）
- API 相關型別定義放在同檔案頂部
- 不在 service 層做錯誤處理（由 composable 層決定如何處理）
- 不放 GET 查詢方法——初始資料由 composable 的 `useFetch` 處理

---

## 2. Composable 層

**路徑**：`app/composables/{module}/`

### 檔案拆分策略

| 檔案 | 用途 | 何時需要 |
|------|------|----------|
| `use{Module}.ts` | 主邏輯、狀態管理 | 永遠需要 |
| `use{Module}Form.ts` | 表單狀態、驗證、送出 | 有建立/編輯表單時 |
| `use{Module}Table.ts` | 列表篩選、排序、分頁 | 有資料表格時 |
| `use{Module}Event.ts` | 事件/動作處理 | 有事件紀錄功能時 |
| `use{Module}Navigation.ts` | 日期導航、頁面切換 | 有時間區間操作時 |
| `use{Module}Report.ts` | 報表、圖表資料處理 | 有統計報表時 |
| `types.ts` | UI/狀態相關共用型別 | 多個 composable 共用型別時 |
| `index.ts` | Barrel export | 永遠需要 |

### 型別定義位置原則

| 型別類型 | 放置位置 | 範例 |
|----------|----------|------|
| API 請求/回應 | `service/{module}Service.ts` | `CreateOrderRequest`, `Order` |
| UI 狀態/表單 | `composables/{module}/types.ts` | `OrderFormErrors`, `TableFilter` |
| 單一 composable 專用 | 該 composable 檔案內 | 僅一處使用的型別 |

### 主邏輯 Composable

根據資料取得場景選擇不同模式：

#### 模式 A：SSR 頁面資料（優先使用）

適用於頁面初始載入、需要 SEO 的資料。使用 Nuxt 的 `useFetch` / `useAsyncData`，資料會透過 payload 傳遞，避免 SSR+CSR 重複請求。

```typescript
// app/composables/order/useOrder.ts
import { computed } from 'vue'

export const useOrder = () => {
  const { data: orders, status, error, refresh } = useFetch('/api/orders', {
    default: () => [],
  })

  const loading = computed(() => status.value === 'pending')
  const totalCount = computed(() => orders.value.length)

  return { orders, loading, error, totalCount, refresh }
}
```

#### 模式 B：客戶端互動資料

適用於使用者操作觸發的請求（表單送出、刪除等），使用 `$fetch` 或 service 層。

```typescript
// app/composables/order/useOrder.ts
import { computed } from 'vue'
import { orderService } from '~/service/orderService'

export const useOrder = () => {
  const { data: orders, status, error, refresh } = useFetch('/api/orders', {
    default: () => [],
  })

  const loading = computed(() => status.value === 'pending')
  const totalCount = computed(() => orders.value.length)

  // 互動操作用 service 層 + $fetch，完成後 refresh 列表
  const deleteOrder = async (id: number) => {
    await orderService.deleteOrder(id)
    await refresh()
  }

  return { orders, loading, error, totalCount, refresh, deleteOrder }
}
```

**選擇原則：**
- 頁面初始資料 → `useFetch` / `useAsyncData`（SSR payload，避免閃爍）
- 使用者互動 → `$fetch` / service 層（事件驅動，不需 SSR）
- 不要在 `onMounted` 中用 `$fetch` 取初始資料（會導致 SSR+CSR 重複請求）

### 表單 Composable

```typescript
// app/composables/order/useOrderForm.ts
import { ref, reactive } from 'vue'
import { orderService, type CreateOrderRequest } from '~/service/orderService'

export interface OrderFormErrors {
  name?: string
}

export const useOrderForm = () => {
  // reactive 用於表單（方便欄位存取），ref 用於列表（方便整體替換）
  const formData = reactive<CreateOrderRequest>({ name: '' })
  const formErrors = reactive<OrderFormErrors>({})
  const isEditing = ref(false)
  const editingId = ref<number | null>(null)
  const saving = ref(false)

  const validate = (): boolean => {
    Object.keys(formErrors).forEach(k => delete (formErrors as any)[k])
    if (!formData.name.trim()) formErrors.name = '名稱為必填'
    return Object.keys(formErrors).length === 0
  }

  const save = async () => {
    if (!validate()) return { success: false, error: '驗證失敗' }
    saving.value = true
    try {
      if (isEditing.value && editingId.value) {
        const order = await orderService.updateOrder(editingId.value, formData)
        return { success: true, order, action: 'update' as const }
      } else {
        const order = await orderService.createOrder(formData)
        return { success: true, order, action: 'create' as const }
      }
    } catch (e: any) {
      return { success: false, error: e.message || '儲存失敗' }
    } finally {
      saving.value = false
    }
  }

  const resetForm = () => {
    Object.assign(formData, { name: '' })
    Object.keys(formErrors).forEach(k => delete (formErrors as any)[k])
    isEditing.value = false
    editingId.value = null
  }

  return { formData, formErrors, isEditing, editingId, saving, validate, save, resetForm }
}
```

### Barrel Export

```typescript
// app/composables/order/index.ts
export { useOrder } from './useOrder'
export { useOrderForm } from './useOrderForm'
export type { OrderFormErrors } from './useOrderForm'
```

匯入方式：`import { useOrder, useOrderForm } from '~/composables/order'`

### 統一回應格式

所有 save/create/update 方法統一回傳：

```typescript
// 成功
return { success: true, [entity]: result, action: 'create' | 'update' }
// 失敗
return { success: false, error: 'Error message' }
```

---

## 3. Utils 層

**路徑**：`app/utils/{name}Utils.ts`

純函式，無副作用，不依賴 Vue 響應式系統。

```typescript
// app/utils/formatUtils.ts
export const formatCurrency = (amount: number, currency = 'TWD'): string => {
  return new Intl.NumberFormat('zh-TW', { style: 'currency', currency }).format(amount)
}

export const formatDate = (date: string | Date, format = 'YYYY-MM-DD'): string => {
  // 日期格式化邏輯
}
```

```typescript
// app/utils/validationUtils.ts
export const isEmail = (value: string): boolean => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)
export const isPhone = (value: string): boolean => /^09\d{8}$/.test(value)
```

---

## 4. 頁面層

**路徑**：`app/pages/{module}/`

```
app/pages/order/
├── index.vue              # 列表頁
├── create.vue             # 建立/編輯頁
└── components/            # 頁面專屬元件
    ├── OrderTable.vue
    ├── OrderFilters.vue
    └── index.ts           # Barrel export
```

### 頁面結構

```vue
<!-- app/pages/order/index.vue -->
<template>
  <div class="min-h-screen bg-slate-50/30">
    <div class="p-4 lg:p-6 space-y-4">
      <!-- 內容 -->
    </div>
  </div>
</template>

<script setup lang="ts">
import { useOrder } from '~/composables/order'

// definePageMeta 用於頁面行為（layout、middleware、transition）
definePageMeta({ layout: 'default' })

// useHead / useSeoMeta 用於文件標題與 SEO
useSeoMeta({ title: '訂單管理', description: '管理所有訂單' })

// composable 內部使用 useFetch，資料自動 SSR 載入，不需 onMounted
const { orders, loading, error, refresh } = useOrder()
</script>
```

### 頁面元件 Barrel Export

```typescript
// app/pages/order/components/index.ts
export { default as OrderTable } from './OrderTable.vue'
export { default as OrderFilters } from './OrderFilters.vue'
```

---

## 5. 路由與權限

路由與權限設定依專案架構而定。常見模式：

### 路由設定

若專案使用集中式路由配置：

```typescript
// 在路由設定檔中新增
'/order': {
  title: '訂單管理',
  icon: 'clipboard-list',
},
```

若專案使用檔案式路由（Nuxt 預設），則 `app/pages/` 下的檔案自動產生路由，無需額外設定。

### 權限設定

若專案有權限系統，依照現有模式新增：

```typescript
// 新增權限鍵值
ORDER: ['order:view', 'order:create', 'order:edit', 'order:delete']

// 新增權限 computed
const canViewOrder = computed(() => hasPermission('order:view'))
```

若無權限系統，跳過此步驟。

### Middleware（路由守衛）

用於驗證、權限檢查等路由層級邏輯。放在 `app/middleware/` 下。

```typescript
// app/middleware/auth.ts
export default defineNuxtRouteMiddleware((to) => {
  const { loggedIn } = useUserSession()
  if (!loggedIn.value) {
    return navigateTo('/login')
  }
})
```

在頁面中使用：

```typescript
definePageMeta({
  middleware: ['auth'],
})
```

### 全域錯誤頁面

`app/error.vue` 處理整頁錯誤（404、500 等）：

```vue
<!-- app/error.vue -->
<template>
  <div class="min-h-screen flex items-center justify-center">
    <div class="text-center">
      <h1 class="text-6xl font-bold">{{ error?.statusCode }}</h1>
      <p class="mt-4 text-lg">{{ error?.message }}</p>
      <button class="btn btn-primary mt-6" @click="handleError">
        回首頁
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{ error: { statusCode: number; message: string } }>()

const handleError = () => clearError({ redirect: '/' })
</script>
```

區域錯誤用 `<NuxtErrorBoundary>` 處理，不影響整頁。

### 導航選單

依專案的 layout 結構，在側邊欄或頂部導航新增連結。

---

## 命名規範

| 類型 | 規範 | 範例 |
|------|------|------|
| Composable 目錄 | kebab-case | `dashboard-tickets/` |
| Composable 檔案 | camelCase + use 前綴 | `useOrderForm.ts` |
| Service 檔案 | camelCase + Service 後綴 | `orderService.ts` |
| 頁面元件 | PascalCase | `OrderModal.vue` |
| 工具函式 | camelCase + Utils 後綴 | `formatUtils.ts` |
| 設定檔 | camelCase + Config 後綴 | `routeConfig.ts` |
