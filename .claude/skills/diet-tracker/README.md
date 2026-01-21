# Diet Tracker 使用指南

專業營養追蹤與健康顧問，基於 2025 年最新營養科學研究。

## 安裝

**安裝到當前專案：**

```bash
git clone --depth 1 https://github.com/JakeChang/skill_pool.git /tmp/skill_pool && mkdir -p .claude/skills && cp -r /tmp/skill_pool/.claude/skills/diet-tracker .claude/skills/ && rm -rf /tmp/skill_pool
```

**安裝到全域：**

```bash
git clone --depth 1 https://github.com/JakeChang/skill_pool.git /tmp/skill_pool && mkdir -p ~/.claude/skills && cp -r /tmp/skill_pool/.claude/skills/diet-tracker ~/.claude/skills/ && rm -rf /tmp/skill_pool
```

## 指令一覽

| 指令 | 說明 |
|------|------|
| `/diet add [食物]` | 記錄飲食 |
| `/diet today` | 今日統計 |
| `/diet week` | 週報分析 |
| `/diet suggest` | 智慧建議下一餐 |
| `/diet analyze` | 深度營養分析 |
| `/diet score` | 健康評分 (0-100) |
| `/diet learn [主題]` | 學習營養知識 |
| `/diet goal [設定]` | 設定每日目標 |

## 使用範例

### 記錄飲食

```
/diet add 午餐吃了鮭魚定食
```

輸出：
```
已記錄：午餐
- 鮭魚定食 (1份): 650 kcal | 蛋白質 40g | 碳水 55g | 脂肪 28g
  [v] 高 Omega-3 | [v] 達亮氨酸門檻 | 抗發炎 +3

今日累計：1150 / 1800 kcal (剩餘 650 kcal)
[統計] 蛋白質: 75g/100g | 碳水: 120g/150g | 脂肪: 45g/60g
[分數] 今日健康分數：82/100

[提示] 今天 Omega-3 攝取良好！晚餐可選高纖蔬菜補足纖維。
```

### 查看今日統計

```
/diet today
```

### 取得下一餐建議

```
/diet suggest
```

### 設定目標

```
/diet goal calories 1800
/diet goal protein 100
/diet goal type longevity
```

**目標類型：**
- `weight_loss` - 減重
- `muscle_gain` - 增肌
- `longevity` - 長壽健康
- `maintenance` - 維持現狀

### 學習營養知識

```
/diet learn protein
```

**支援主題：** protein、fat、carb、gut、inflammation、fasting、longevity、supplements

## 資料儲存

所有紀錄儲存在專案根目錄的 `./diet-records/`：

```
diet-records/
├── config.json          # 使用者目標設定
├── 2026-01-21.json      # 每日飲食紀錄
└── 2026-01-21.html      # 每日 HTML 報告
```

## 核心功能

- **精確追蹤**：記錄熱量、蛋白質、碳水、脂肪、纖維、Omega-3
- **進階指標**：亮氨酸門檻、抗發炎分數、腸道健康指數
- **智慧建議**：根據已攝取營養分析缺口，推薦下一餐
- **健康評分**：每日 0-100 分，量化飲食品質
- **週報分析**：找出飲食模式問題，提供改善建議

## 相關檔案

| 檔案 | 說明 |
|------|------|
| `references/nutrition-table.md` | 食物營養成分參考表 |
| `references/science.md` | 營養科學知識庫 |
| `references/scoring.md` | 健康評分計算邏輯 |
| `assets/html-template.md` | HTML 報告模板 |
