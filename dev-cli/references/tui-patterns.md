# TUI 渲染模式

## 目錄

- [渲染方式選擇](#渲染方式選擇)
- [ANSI 直接渲染](#ansi-直接渲染) — 核心模式、cleanup、鍵盤輸入、debounce
- [TUI 規則](#tui-規則)

---

## 渲染方式選擇

| 方式 | 優點 | 缺點 | 適用場景 |
|------|------|------|----------|
| ANSI 直接渲染 | 完全控制、零框架開銷、精確 cursor | 手動管理複雜 | 高效能、簡單佈局 |
| Ink（React） | 元件化、狀態管理、佈局系統 | React 開銷、啟動慢 | 複雜互動 UI |

---

## ANSI 直接渲染

**路徑**：`src/app.tsx`

### 核心模式

```typescript
// src/app.tsx

export class AppRenderer {
  private selectedIndex = 0
  private renderTimer: NodeJS.Timeout | null = null

  async start(): Promise<void> {
    // 1. 進入 raw mode
    process.stdin.setRawMode(true)
    process.stdin.resume()
    process.stdin.setEncoding('utf8')

    // 2. 隱藏 cursor
    process.stdout.write('\x1b[?25l')

    // 3. 註冊事件
    process.stdin.on('data', this.handleInput.bind(this))
    process.on('SIGWINCH', this.scheduleRender.bind(this))

    // 4. 註冊 cleanup（必須）
    const cleanup = async () => {
      process.stdout.write('\x1b[?25h')  // 顯示 cursor
      process.stdin.setRawMode(false)
      // 清理資源（如 child process）
      process.exit(0)
    }
    process.on('SIGINT', cleanup)
    process.on('SIGTERM', cleanup)

    // 5. 初始渲染
    this.render()
  }

  private scheduleRender(): void {
    // debounce 50ms 避免閃爍
    if (this.renderTimer) clearTimeout(this.renderTimer)
    this.renderTimer = setTimeout(() => this.render(), 50)
  }

  private render(): void {
    const { columns, rows } = process.stdout
    const output: string[] = []

    // 清除畫面
    output.push('\x1b[2J\x1b[H')

    // 組裝畫面內容...

    process.stdout.write(output.join(''))
  }

  private handleInput(data: string): void {
    switch (data) {
      case 'q':
        // 退出確認
        break
      case 'j':
      case '\x1b[B':  // 方向鍵下
        this.selectedIndex = Math.min(this.selectedIndex + 1, this.maxIndex)
        this.scheduleRender()
        break
      case 'k':
      case '\x1b[A':  // 方向鍵上
        this.selectedIndex = Math.max(this.selectedIndex - 1, 0)
        this.scheduleRender()
        break
    }
  }
}
```

### 常用 ANSI 序列

| 序列 | 用途 |
|------|------|
| `\x1b[2J\x1b[H` | 清除畫面並移到左上角 |
| `\x1b[?25l` / `\x1b[?25h` | 隱藏 / 顯示 cursor |
| `\x1b[{n}m` | SGR（顏色、粗體等） |
| `\x1b[{row};{col}H` | 移動 cursor 到指定位置 |

---

## TUI 規則

- 進入時隱藏 cursor，退出時**必須還原**
- 進入 raw mode 後，退出時**必須還原**
- 渲染使用 debounce（50ms），避免快速操作造成閃爍
- terminal resize（SIGWINCH）時重新渲染
- SIGINT / SIGTERM 必須 graceful shutdown（清理資源、還原 terminal）
- 鍵盤操作同時支援 vim 風格（j/k）和方向鍵
