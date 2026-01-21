#!/bin/bash
# Nuxt 4 + TailwindCSS + DaisyUI 專案設定腳本
# 用法: ./setup.sh <project-name>

set -e

PROJECT_NAME=${1:-"nuxt4-daisyui-app"}

echo "🚀 建立 Nuxt 4 專案: $PROJECT_NAME"

# 建立 Nuxt 專案
npm create nuxt "$PROJECT_NAME" -- --no-install
cd "$PROJECT_NAME"

# 安裝依賴
echo "📦 安裝依賴套件..."
npm install
npm install tailwindcss@latest @tailwindcss/vite@latest daisyui@latest

# 建立 nuxt.config.ts
echo "⚙️ 設定 nuxt.config.ts..."
cat > nuxt.config.ts << 'EOF'
import tailwindcss from "@tailwindcss/vite";

export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  vite: {
    plugins: [tailwindcss()],
  },
  css: ["./app/tailwind.css"],
})
EOF

# 建立 tailwind.css
echo "🎨 建立 tailwind.css..."
cat > app/tailwind.css << 'EOF'
@import "tailwindcss";
@plugin "daisyui";
EOF

# 更新 app.vue
echo "📝 更新 app.vue..."
cat > app/app.vue << 'EOF'
<template>
  <div>
    <NuxtPage />
  </div>
</template>
EOF

# 建立 pages 目錄和首頁
echo "📄 建立測試頁面..."
mkdir -p app/pages
cat > app/pages/index.vue << 'EOF'
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
EOF

echo ""
echo "✅ 專案設定完成！"
echo ""
echo "執行以下指令啟動開發伺服器："
echo "  cd $PROJECT_NAME"
echo "  npm run dev"
