---
name: dev-cli
description: Node.js CLI/TUI 應用開發技能。當需要：(1) 建立 CLI 工具或 TUI 介面、(2) 規劃 CLI 指令結構、(3) 開發終端機互動功能（鍵盤操作、ANSI 渲染、process 管理）、(4) 檢查 CLI 程式碼品質時使用。適用於 TypeScript + meow 的 CLI 專案，遵循三層式架構（CLI Entry → Core → Utils）。不適用於：純 npm library（無 CLI 入口）、Electron/桌面應用、非 Node.js 的 CLI 工具。
---

# CLI/TUI 應用開發

適用於 Node.js CLI 工具與 TUI（終端機使用者介面）開發，使用 TypeScript + meow 框架。

遵循三層式架構：

```
CLI Entry → Core Modules → Utils
指令路由     業務邏輯/狀態管理   純函式工具
```

依賴規則：上層可依賴下層，下層不可依賴上層。

## 為什麼要模組化

CLI 工具容易把所有邏輯塞進一個檔案。模組化的核心原則：

- **每個檔案控制在 300 行以內**，最多不超過 1000 行
- **單一職責**：CLI 入口只做指令路由，業務邏輯放 core，格式化放 utils
- **可獨立測試**：core 模組不依賴 stdin/stdout，方便單元測試

架構細節請見 [references/architecture.md](references/architecture.md)。
TUI 渲染模式請見 [references/tui-patterns.md](references/tui-patterns.md)。

---

## 指令

### `/dev-cli plan`

分析需求，規劃 CLI 工具的指令結構與功能。

**流程：**

1. 與使用者確認：
   - 這個 CLI 工具要解決什麼問題？
   - 需要哪些子指令？
   - 是否需要 TUI 互動介面？
   - 需要管理什麼狀態（設定檔、process、資料）？
   - 目標使用者是誰（開發者、運維、一般使用者）？

2. 產出需求清單：

```markdown
# {工具名稱} 需求規劃

## 目標
簡述工具目的與解決的問題。

## 指令結構
| 指令 | 說明 | 參數 |
|------|------|------|
| `tool-name` | 預設行為（TUI / help） | |
| `tool-name init` | 初始化設定 | |
| `tool-name add <arg>` | 新增項目 | `<arg>` 必填 |

## flags
| flag | 縮寫 | 說明 | 預設值 |
|------|------|------|--------|

## 互動模式
是否需要 TUI？鍵盤操作清單。

## 狀態管理
設定檔位置、格式、資料結構。

## 不包含
明確列出此次不做的項目。
```

3. 儲存至：`docs/requirements/{tool-name}.md`

---

### `/dev-cli spec`

基於需求，撰寫技術計劃書。

**前置條件：** 已有需求文件。

**流程：**

1. 讀取需求文件
2. 產出計劃書：

```markdown
# {工具名稱} 技術計劃書

## 概要
基於 {需求文件路徑} 的技術實作方案。

## 技術選型
- CLI 框架：meow
- TUI 渲染：ANSI 直接渲染 / Ink
- process 管理：child_process + tree-kill（如需要）

## 檔案清單

### CLI Entry
| 檔案 | 用途 |
|------|------|
| `src/index.tsx` | 指令路由 |
| `src/app.tsx` | TUI 主渲染器（如需要） |

### Core
| 檔案 | 用途 |
|------|------|

### Utils
| 檔案 | 用途 |
|------|------|

## 實作順序
1. 專案初始化（package.json、tsconfig.json）
2. Core 模組（config、業務邏輯）
3. CLI 入口（指令路由）
4. TUI 介面（如需要）
5. 測試

## 設定檔結構
JSON 格式，包含 version 欄位。
```

3. 儲存至：`docs/specs/{tool-name}.md`

---

### `/dev-cli dev`

依照三層架構開發 CLI 工具。

**前置條件：** 已有計劃書或明確的開發目標。

**流程：**

1. 讀取計劃書（如有）
2. 依照 [references/architecture.md](references/architecture.md) 的模式，按順序建立：
   - **專案初始化** → **Core 模組** → **CLI 入口** → **TUI（如需要）**
3. 每完成一層，簡要回報進度
4. 開發完成後執行編譯確認型別無誤：
   ```bash
   npm run build
   ```
   不需要執行 `npm run dev` 或啟動工具，編譯通過即可。
5. 列出所有新增/修改的檔案

---

### `/dev-cli review`

檢查 CLI 程式碼品質。

**用法：** `/dev-cli review` 或 `/dev-cli review {module-name}`

**流程：**

1. 執行編譯，確認型別無誤（不需要 `npm run dev`）：
   ```bash
   npm run build
   ```
2. 掃描 `src/` 目錄結構
3. 針對以下規則逐一檢查：

#### 架構檢查

- 依賴方向：core 不應 import CLI entry，utils 不應 import core
- 檔案命名：kebab-case（`config-manager.ts`、`log-buffer.ts`）
- 檔案大小：超過 300 行警告，超過 1000 行必須拆分

#### CLI 品質檢查

- 指令是否有完整的 `--help` 說明
- 錯誤訊息是否清楚（包含建議的修正動作）
- exit code 是否正確（0 成功、1 一般錯誤、2 參數錯誤）
- 是否處理 SIGINT / SIGTERM 的 graceful shutdown

#### TUI 檢查（如有 TUI）

- 是否處理 terminal resize 事件
- 是否在退出時還原 terminal 狀態（cursor、raw mode）
- 是否支援 CJK 全形字元寬度計算
- 渲染是否有 debounce 避免閃爍

#### 程式碼內容檢查

**型別安全**
- `any` 濫用（超過 3 處警告）
- 未使用的 import / 變數

**Process 管理**
- child process 是否在退出時被清理（tree-kill 或 SIGTERM）
- 是否有 shutdown timeout 防止 zombie process
- event listener 是否在不需要時移除

**資源管理**
- 檔案 handle 是否正確關閉
- setInterval / setTimeout 是否在退出時清除
- EventEmitter listener 是否有 memory leak（未 removeListener）

**安全性**
- 使用者輸入是否消毒（避免 command injection）
- `child_process.exec` / `spawn` 的 shell 參數是否安全
- 設定檔路徑是否有 path traversal 風險

4. 產出審查報告：

```markdown
# 審查報告

## 總覽
- 掃描檔案數：N
- 問題數：N（嚴重：N / 警告：N）

## 問題清單

### 嚴重（必須修正）
| # | 檔案:行號 | 類別 | 問題 | 說明 |
|---|-----------|------|------|------|

### 警告（建議修正）
| # | 檔案:行號 | 類別 | 問題 | 說明 |
|---|-----------|------|------|------|
```

---

### `/dev-cli test`

透過 Bash 工具在終端機中直接執行 CLI 指令進行測試。

**前置條件：** 工具已開發完成。

**流程：**

1. 建置專案：`npm run build`
2. 使用 Bash 工具依序執行測試：

#### 指令測試
- 執行每個子指令，用 Bash 確認 stdout 輸出正確
- 執行 `tool-name --help`，確認說明完整
- 執行無效指令 / 無效參數，確認 stderr 錯誤訊息清楚
- 用 `echo $?` 確認 exit code 正確（0/1/2）

#### TUI 測試（如有 TUI，需使用者手動確認）
- TUI 互動無法透過 Bash 自動測試，改為請使用者手動啟動並回報
- 提供測試檢查清單讓使用者逐項確認：畫面渲染、鍵盤操作、退出行為

#### 邊界測試
- 刪除設定檔後執行指令，確認錯誤處理正確
- 對唯讀目錄執行寫入操作，確認權限錯誤訊息
- 執行後用 `kill -SIGINT <pid>` 測試 graceful shutdown

3. 產出測試報告：

```markdown
# {工具名稱} 測試報告

## 測試結果
| 測試項目 | 狀態 | 備註 |
|----------|------|------|

## 發現的問題
（如有）
```
