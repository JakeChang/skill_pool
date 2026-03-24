# CLI/TUI 三層式架構參考

## 目錄

- [架構總覽](#架構總覽)
- [1. CLI Entry 層](#1-cli-entry-層) — 指令路由、meow 設定
- [2. Core 層](#2-core-層) — config、process、log buffer、EventEmitter
- [3. Utils 層](#3-utils-層) — terminal 格式化、純函式工具
- [4. 選用模式](#4-選用模式) — process 管理、log buffer（按需使用）
- [專案初始化](#專案初始化) — package.json、tsconfig.json
- [命名規範](#命名規範)

---

## 架構總覽

```
src/
├── index.tsx              # CLI 入口：指令路由
├── app.tsx                # TUI 主渲染器（如需要）
├── core/                  # 業務邏輯
│   ├── types.ts           # 所有 TypeScript 型別
│   ├── config-manager.ts  # 設定檔管理
│   ├── process-manager.ts # process 管理（如需要）
│   └── log-buffer.ts      # 日誌緩衝（如需要）
└── utils/
    ├── colors.ts          # terminal 格式化
    └── terminal-link.ts   # 終端機超連結
```

依賴規則：`index.tsx` → `app.tsx` → `core/*` → `utils/*`，下層不依賴上層。

---

## 1. CLI Entry 層

**路徑**：`src/index.tsx`

使用 meow 解析指令與 flags，路由到對應處理函式。不放業務邏輯。

```typescript
#!/usr/bin/env node
import meow from 'meow'
import { ConfigManager } from './core/config-manager.js'

const cli = meow(`
  Usage
    $ my-tool <command>

  Commands
    init          初始化設定
    add <path>    新增項目
    remove <id>   移除項目
    list          列出所有項目
    config        編輯設定檔

  Options
    --port, -p    指定 port
    --verbose     顯示詳細日誌

  Examples
    $ my-tool init
    $ my-tool add ./my-project --port 3000
`, {
  importMeta: import.meta,
  flags: {
    port: { type: 'number', shortFlag: 'p' },
    verbose: { type: 'boolean', default: false },
  },
})

const [command, ...args] = cli.input
const configManager = new ConfigManager()

switch (command) {
  case 'init':
    await configManager.init()
    console.log('✓ 設定檔已建立')
    break

  case 'add':
    if (!args[0]) {
      console.error('錯誤：請提供專案路徑')
      process.exit(2)
    }
    await configManager.addProject(args[0], cli.flags)
    break

  case 'remove':
    if (!args[0]) {
      console.error('錯誤：請提供專案 ID')
      process.exit(2)
    }
    await configManager.removeProject(args[0])
    break

  case 'list':
    const projects = await configManager.getProjects()
    // 格式化輸出
    break

  case 'config':
    // 開啟 $EDITOR
    break

  default:
    // 無指令時啟動 TUI（如有），否則顯示 help
    if (command) {
      console.error(`未知指令：${command}`)
      cli.showHelp()
      process.exit(2)
    }
    // 啟動 TUI
    const { AppRenderer } = await import('./app.js')
    const app = new AppRenderer(configManager)
    await app.start()
}
```

**規則**：
- 第一行必須有 shebang：`#!/usr/bin/env node`
- exit code：0 成功、1 一般錯誤、2 參數/用法錯誤
- 錯誤訊息包含建議動作（「請提供...」而非只說「缺少參數」）
- 動態 import TUI 模組，減少非 TUI 指令的啟動時間

---

## 2. Core 層

**路徑**：`src/core/`

每個 CLI 工具的 core 模組依需求不同。常見組合：

| 工具類型 | 必要模組 | 選用模組 |
|----------|----------|----------|
| 設定管理工具 | types.ts、config-manager.ts | — |
| 資料處理工具 | types.ts、data-processor.ts | formatter.ts |
| Dev server 管理器 | types.ts、config-manager.ts | process-manager.ts、log-buffer.ts |
| 檔案產生器 | types.ts、template-engine.ts | — |

以下以「設定管理 + process 管理」為例說明各模組模式。

### types.ts — 集中型別定義

```typescript
// src/core/types.ts

export interface Config {
  version: number
  defaults: DefaultConfig
  projects: ProjectConfig[]
}

export interface DefaultConfig {
  logBufferSize: number
  shutdownTimeout: number
}

export interface ProjectConfig {
  id: string
  name: string
  path: string
  port: number
  command: string
  env?: Record<string, string>
  autoStart?: boolean
}

export type ProjectStatus = 'stopped' | 'starting' | 'running' | 'error'

export interface ProjectState {
  pid: number | null
  status: ProjectStatus
  uptime: number
  lastError: string | null
}
```

### config-manager.ts — 設定檔管理

```typescript
// src/core/config-manager.ts
import { readFile, writeFile, mkdir } from 'node:fs/promises'
import { existsSync } from 'node:fs'
import { homedir } from 'node:os'
import { join } from 'node:path'
import type { Config, ProjectConfig } from './types.js'

const CONFIG_DIR = join(homedir(), '.my-tool')
const CONFIG_FILE = join(CONFIG_DIR, 'config.json')

const DEFAULT_CONFIG: Config = {
  version: 1,
  defaults: {
    logBufferSize: 1000,
    shutdownTimeout: 5000,
  },
  projects: [],
}

export class ConfigManager {
  private config: Config | null = null

  async load(): Promise<Config> {
    if (this.config) return this.config

    if (!existsSync(CONFIG_FILE)) {
      return DEFAULT_CONFIG
    }

    const raw = await readFile(CONFIG_FILE, 'utf-8')
    this.config = JSON.parse(raw) as Config
    return this.config
  }

  async save(config: Config): Promise<void> {
    await mkdir(CONFIG_DIR, { recursive: true })
    await writeFile(CONFIG_FILE, JSON.stringify(config, null, 2))
    this.config = config
  }

  async init(): Promise<void> {
    await this.save(DEFAULT_CONFIG)
  }

  async addProject(path: string, options?: { port?: number }): Promise<void> {
    const config = await this.load()
    // 產生 ID、偵測名稱、分配 port
    const project: ProjectConfig = {
      id: generateId(path),
      name: detectProjectName(path),
      path,
      port: options?.port ?? await findFreePort(3000),
      command: 'npm run dev',
    }
    config.projects.push(project)
    await this.save(config)
  }

  async removeProject(id: string): Promise<void> {
    const config = await this.load()
    config.projects = config.projects.filter(p => p.id !== id)
    await this.save(config)
  }

  async getProjects(): Promise<ProjectConfig[]> {
    const config = await this.load()
    return config.projects
  }
}
```

**規則**：
- 設定檔放在 `~/.{tool-name}/` 下
- 預設值集中定義，不散落在各處
- config 物件帶 `version` 欄位，方便未來 migration

---

## 4. 選用模式

以下模組根據需求加入，並非每個 CLI 工具都需要。

### process-manager.ts — Process 管理（選用）

**何時需要**：CLI 工具需要啟動/管理子 process 時（如 dev server 管理器、task runner）。

```typescript
// src/core/process-manager.ts
import { spawn, type ChildProcess } from 'node:child_process'
import { EventEmitter } from 'node:events'
import treeKill from 'tree-kill'
import type { ProjectConfig, ProjectState } from './types.js'

export class ProcessManager extends EventEmitter {
  private processes = new Map<string, ChildProcess>()
  private states = new Map<string, ProjectState>()

  start(project: ProjectConfig): void {
    if (this.processes.has(project.id)) return

    this.updateState(project.id, { status: 'starting', pid: null })

    const child = spawn(project.command, {
      cwd: project.path,
      shell: true,
      stdio: ['ignore', 'pipe', 'pipe'],
      env: { ...process.env, PORT: String(project.port), ...project.env },
    })

    this.processes.set(project.id, child)
    this.updateState(project.id, { status: 'running', pid: child.pid ?? null })

    child.stdout?.on('data', (data: Buffer) => {
      this.emit('log', project.id, data.toString())
    })

    child.stderr?.on('data', (data: Buffer) => {
      this.emit('log', project.id, data.toString())
    })

    child.on('exit', (code) => {
      this.processes.delete(project.id)
      this.updateState(project.id, {
        status: code === 0 ? 'stopped' : 'error',
        pid: null,
        lastError: code !== 0 ? `exit code: ${code}` : null,
      })
      this.emit('exited', project.id, code)
    })

    this.emit('started', project.id)
  }

  async stop(id: string, timeout = 5000): Promise<void> {
    const child = this.processes.get(id)
    if (!child?.pid) return

    return new Promise<void>((resolve) => {
      const timer = setTimeout(() => {
        // timeout 後強制 kill
        treeKill(child.pid!, 'SIGKILL')
        resolve()
      }, timeout)

      child.on('exit', () => {
        clearTimeout(timer)
        resolve()
      })

      treeKill(child.pid!, 'SIGTERM')
    })
  }

  async stopAll(timeout = 5000): Promise<void> {
    await Promise.all(
      [...this.processes.keys()].map(id => this.stop(id, timeout))
    )
  }

  private updateState(id: string, partial: Partial<ProjectState>): void {
    const current = this.states.get(id) ?? {
      pid: null, status: 'stopped' as const, uptime: 0, lastError: null,
    }
    const next = { ...current, ...partial }
    this.states.set(id, next)
    this.emit('stateChange', id, next)
  }

  getState(id: string): ProjectState | undefined {
    return this.states.get(id)
  }
}
```

**規則**：
- 使用 `tree-kill` 確保子 process tree 完整清除
- 必須有 shutdown timeout 防止 zombie process
- 繼承 `EventEmitter`，透過事件通知 UI 層
- stdout/stderr 統一為 `log` 事件

### log-buffer.ts — 環形日誌緩衝（選用）

**何時需要**：需要保留子 process 或串流輸出的最近 N 行時（如 TUI 日誌檢視器）。

```typescript
// src/core/log-buffer.ts

export class LogBuffer {
  private buffer: string[] = []
  private maxSize: number

  constructor(maxSize = 1000) {
    this.maxSize = maxSize
  }

  push(line: string): void {
    this.buffer.push(line)
    if (this.buffer.length > this.maxSize) {
      this.buffer.shift()
    }
  }

  getLines(count?: number): string[] {
    if (!count) return [...this.buffer]
    return this.buffer.slice(-count)
  }

  clear(): void {
    this.buffer = []
  }

  get length(): number {
    return this.buffer.length
  }
}
```

**規則**：
- 固定上限，避免長時間運行記憶體無限增長
- 超過上限時丟棄最舊的資料

---

## 3. Utils 層

**路徑**：`src/utils/`

純函式，不依賴 core 或 CLI entry。

### colors.ts — Terminal 格式化

```typescript
// src/utils/colors.ts

// ANSI escape codes
const ESC = '\x1b['
const RESET = `${ESC}0m`

export const bold = (s: string) => `${ESC}1m${s}${RESET}`
export const dim = (s: string) => `${ESC}2m${s}${RESET}`
export const green = (s: string) => `${ESC}32m${s}${RESET}`
export const red = (s: string) => `${ESC}31m${s}${RESET}`
export const yellow = (s: string) => `${ESC}33m${s}${RESET}`
export const cyan = (s: string) => `${ESC}36m${s}${RESET}`
export const gray = (s: string) => `${ESC}90m${s}${RESET}`

// CJK 全形字元寬度計算
export function getStringWidth(str: string): number {
  let width = 0
  for (const char of str) {
    const code = char.codePointAt(0)!
    if (
      (code >= 0x1100 && code <= 0x115F) ||   // Hangul Jamo
      (code >= 0x2E80 && code <= 0x303E) ||   // CJK Radicals
      (code >= 0x3040 && code <= 0x33BF) ||   // Japanese
      (code >= 0x3400 && code <= 0x4DBF) ||   // CJK Unified Ext A
      (code >= 0x4E00 && code <= 0x9FFF) ||   // CJK Unified
      (code >= 0xF900 && code <= 0xFAFF) ||   // CJK Compat
      (code >= 0xFE30 && code <= 0xFE6F) ||   // CJK Compat Forms
      (code >= 0xFF01 && code <= 0xFF60) ||   // Fullwidth Forms
      (code >= 0x20000 && code <= 0x2FFFF)    // CJK Unified Ext B-F
    ) {
      width += 2
    } else {
      width += 1
    }
  }
  return width
}

// 填充字串到指定寬度（考慮全形）
export function padEnd(str: string, width: number): string {
  const currentWidth = getStringWidth(str)
  if (currentWidth >= width) return str
  return str + ' '.repeat(width - currentWidth)
}

// 截斷字串到指定寬度（考慮全形）
export function truncate(str: string, maxWidth: number, suffix = '…'): string {
  if (getStringWidth(str) <= maxWidth) return str
  let width = 0
  let result = ''
  for (const char of str) {
    const charWidth = getStringWidth(char)
    if (width + charWidth + getStringWidth(suffix) > maxWidth) break
    result += char
    width += charWidth
  }
  return result + suffix
}
```

### terminal-link.ts — OSC 8 超連結

```typescript
// src/utils/terminal-link.ts

export function terminalLink(text: string, url: string): string {
  return `\x1b]8;;${url}\x07${text}\x1b]8;;\x07`
}
```

---

TUI 渲染模式（ANSI 直接渲染、Ink 框架選擇、鍵盤輸入）請見 [references/tui-patterns.md](tui-patterns.md)。

---

## 專案初始化

### package.json

```json
{
  "name": "my-tool",
  "version": "0.0.1",
  "type": "module",
  "bin": {
    "my-tool": "./dist/index.js"
  },
  "scripts": {
    "build": "tsc",
    "dev": "tsx src/index.tsx",
    "start": "node dist/index.js"
  },
  "dependencies": {
    "meow": "^13.0.0"
  },
  "devDependencies": {
    "@types/node": "^22.0.0",
    "tsx": "^4.19.0",
    "typescript": "^5.7.0"
  }
}
```

按需加入：
- `tree-kill`：需要 process 管理時
- `ink` + `react`：選擇 Ink 框架而非 ANSI 直接渲染時

### tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

如使用 JSX（Ink 或自訂）：加入 `"jsx": "react-jsx"`。

---

## 命名規範

| 類型 | 規範 | 範例 |
|------|------|------|
| 檔案名稱 | kebab-case | `config-manager.ts` |
| Class | PascalCase | `ConfigManager` |
| 函式/變數 | camelCase | `getStringWidth` |
| 型別/介面 | PascalCase | `ProjectConfig` |
| 常數 | UPPER_SNAKE 或 camelCase | `CONFIG_DIR`、`DEFAULT_CONFIG` |
| CLI 指令 | kebab-case | `my-tool add` |
| flags | camelCase（meow 自動轉換） | `--port`、`--verbose` |
