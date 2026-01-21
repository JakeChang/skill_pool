---
name: diet-tracker
description: 專業營養追蹤與健康顧問。追蹤每日飲食、深度分析營養素、提供基於 2025 營養科學的專業建議。支援指令：add（記錄）、today（今日統計）、week（週報）、suggest（智慧建議）、analyze（深度分析）、score（健康評分）、learn（營養知識）、goal（設定目標）、calendar（行事曆首頁）、update（更新技能）。
---

# 專業營養追蹤 Skill

結合 **飲食追蹤** 與 **專業營養顧問**，基於 2025 年最新營養科學研究。

## 核心理念

1. **追蹤是基礎**：精確記錄才能精確改善
2. **科學為本**：所有建議基於實證研究
3. **個人化**：根據使用者目標和數據給出客製化建議
4. **長壽優先**：不只減重，更要健康長壽

## 資料儲存位置

所有飲食紀錄儲存在專案根目錄：`diet-records/`

- `diet-records/config.json` - 使用者設定（目標、個人資料）
- `diet-records/YYYY-MM-DD.json` - 每日飲食紀錄
- `diet-records/YYYY-MM-DD.html` - 每日 HTML 報告
- `diet-records/index.html` - 行事曆首頁（當月）
- `diet-records/index-YYYY-MM.html` - 歷史月份行事曆

## 參考資料

根據需要讀取以下參考檔案：
- **[nutrition-table.md](references/nutrition-table.md)** - 估算營養成分時參考
- **[science.md](references/science.md)** - 執行 `/diet-tracker learn` 或需要營養科學知識時參考
- **[scoring.md](references/scoring.md)** - 計算健康評分時參考

## 素材資料

產生輸出時複製以下模板：
- **[html-template.md](assets/html-template.md)** - 產生每日 HTML 報告時複製並填充變數
- **[calendar-template.md](assets/calendar-template.md)** - 產生行事曆首頁時複製並填充變數

---

## 首次使用設定

**重要：每次執行任何指令前，必須先檢查 `diet-records/config.json` 是否存在。**

如果 config.json 不存在，必須先完成初始設定：

### 設定流程

1. **使用 AskUserQuestion 工具依序詢問以下問題：**

   **第一組問題（基本資料）：**
   - 生理性別：男性 / 女性
   - 年齡範圍：18-30 / 31-45 / 46-60 / 60+

   **第二組問題（身體數據）：**
   - 體重範圍：50kg以下 / 50-60kg / 60-70kg / 70-80kg / 80-90kg / 90kg以上
   - 活動量：久坐（幾乎不運動）/ 輕度活動（每週1-2次）/ 中度活動（每週3-5次）/ 高度活動（每天運動）

   **第三組問題（目標設定）：**
   - 主要目標：減重 / 增肌 / 維持健康 / 長壽優化

2. **根據回答計算個人化目標：**

   | 目標類型 | 熱量係數 | 蛋白質 | 碳水比例 | 脂肪比例 |
   |----------|----------|--------|----------|----------|
   | 減重 (weight_loss) | TDEE - 500 | 體重 x 1.6g | 35% | 30% |
   | 增肌 (muscle_gain) | TDEE + 300 | 體重 x 2.0g | 45% | 25% |
   | 維持 (maintenance) | TDEE | 體重 x 1.2g | 45% | 30% |
   | 長壽 (longevity) | TDEE - 200 | 體重 x 1.4g | 40% | 35% |

   **TDEE 估算（簡化版）：**
   - 基礎：男性 1800 / 女性 1500
   - 年齡調整：46-60 歲 -5%，60+ 歲 -10%
   - 體重調整：每 10kg 差異 +/- 100 kcal（以 70kg 為基準）
   - 活動量：久坐 x1.0 / 輕度 x1.2 / 中度 x1.4 / 高度 x1.6

3. **建立 config.json 並儲存**

4. **顯示設定摘要，確認後繼續執行原本的指令**

### 設定完成訊息範例

```
[設定完成] 已建立你的個人營養目標

基本資料：男性，31-45 歲，70-80kg，中度活動
目標類型：長壽優化

每日目標：
- 熱量：1900 kcal
- 蛋白質：105g
- 碳水：190g
- 脂肪：74g
- 纖維：40g
- Omega-3：2g

這些目標可以隨時用 /diet-tracker goal 調整。
現在開始記錄你的飲食吧！
```

---

## 指令說明

### `/diet-tracker add [食物描述]`
記錄使用者吃了什麼。

**步驟：**
1. 解析食物和份量
2. 估算營養成分（參考 nutrition-table.md）
3. 計算進階指標（亮氨酸、Omega-3、纖維、抗發炎分數）
4. 讀取/建立今日紀錄檔案
5. 新增紀錄並更新總計
6. 產生每日 HTML 報告（參考 html-template.md）
7. 更新行事曆首頁 index.html（參考 calendar-template.md）
8. 顯示本次攝取、今日累計、健康提示

**輸出範例：**
```
已記錄：午餐
- 鮭魚定食 (1份): 650 kcal | 蛋白質 40g | 碳水 55g | 脂肪 28g
  [v] 高 Omega-3 | [v] 達亮氨酸門檻 | 抗發炎 +3

今日累計：1150 / 1800 kcal (剩餘 650 kcal)
[統計] 蛋白質: 75g/100g | 碳水: 120g/150g | 脂肪: 45g/60g
[分數] 今日健康分數：82/100

[提示] 今天 Omega-3 攝取良好！晚餐可選高纖蔬菜補足纖維。
```

### `/diet-tracker today`
顯示今日所有飲食紀錄和統計，產生 HTML 報告。

### `/diet-tracker week`
顯示過去 7 天的飲食統計與趨勢分析，找出飲食模式問題並給出改善建議。

### `/diet-tracker suggest`
根據今日已攝取的食物，智慧建議下一餐。

**分析內容：**
- 剩餘可攝取的熱量和各營養素
- 缺口分析（蛋白質不足？纖維不夠？需要 Omega-3？）
- 根據蛋白質分配、抗發炎、腸道健康原則推薦 2-3 種餐點組合

### `/diet-tracker analyze`
深度營養分析，包含：
- 蛋白質分配評估（各餐是否達亮氨酸門檻）
- Omega-3/Omega-6 比例估算
- 抗發炎指數
- 腸道健康指數
- 植物多樣性

### `/diet-tracker score`
計算今日飲食健康評分（0-100），參考 scoring.md 計算邏輯。

### `/diet-tracker learn [主題]`
學習專業營養知識，參考 science.md 提供詳細教學。

**支援主題：** protein、fat、carb、gut、inflammation、fasting、longevity、supplements

### `/diet-tracker goal [設定]`
設定或查看每日目標。

**可設定項目：**
- `calories [數字]` - 每日熱量目標
- `protein [數字]` - 每日蛋白質目標
- `type [weight_loss|muscle_gain|longevity|maintenance]` - 目標類型

### `/diet-tracker calendar`
產生或更新行事曆首頁（index.html）。

**步驟：**
1. 掃描 `diet-records/` 目錄下所有 JSON 紀錄檔案
2. 讀取每個檔案的健康分數和熱量資訊
3. 計算當月統計（記錄天數、平均分數、平均熱量、平均蛋白質）
4. 產生當月行事曆 HTML（參考 calendar-template.md）
5. 儲存為 `diet-records/index.html`

**功能特點：**
- 以月曆格式顯示，每日格子顯示健康分數
- 有紀錄的日期可點擊連結到當日報告
- 根據分數顯示不同顏色（綠=優秀、黃=普通、紅=需改善）
- 顯示月份統計摘要
- 支援切換查看歷史月份

**輸出範例：**
```
[行事曆] 已更新 2026年1月 行事曆首頁

本月統計：
- 記錄天數：15 天
- 平均分數：72 分
- 平均熱量：1650 kcal
- 平均蛋白質：95g

檔案位置：diet-records/index.html
```

### `/diet-tracker update`
更新本機的 diet-tracker skill 到最新版本。

**步驟：**
1. 使用 AskUserQuestion 詢問使用者要更新哪個位置：
   - 全域（~/.claude/）：更新所有專案共用的 skills
   - 當前專案（./.claude/）：只更新當前專案的 skills

2. 根據選擇設定目標路徑

3. 執行更新流程：
   ```bash
   rm -rf /tmp/skill_pool
   git clone --depth 1 https://github.com/JakeChang/skill_pool.git /tmp/skill_pool
   ```

4. 複製 diet-tracker skill 到目標位置：
   ```bash
   mkdir -p <目標路徑>/skills
   cp -r /tmp/skill_pool/.claude/skills/diet-tracker <目標路徑>/skills/
   ```

5. 清理臨時檔案：
   ```bash
   rm -rf /tmp/skill_pool
   ```

6. 顯示更新結果

**輸出範例：**
```
[更新完成] diet-tracker 已更新至最新版本

更新位置：~/.claude/skills/diet-tracker
```

---

## 紀錄檔案格式

### config.json
```json
{
  "daily_calorie_goal": 1800,
  "protein_goal": 100,
  "carbs_goal": 150,
  "fat_goal": 60,
  "fiber_goal": 40,
  "omega3_goal": 2,
  "goal_type": "longevity"
}
```

### 每日紀錄 (YYYY-MM-DD.json)
```json
{
  "date": "2026-01-14",
  "meals": [
    {
      "time": "12:30",
      "type": "午餐",
      "items": [
        {
          "name": "鮭魚定食",
          "quantity": "1份",
          "calories": 650,
          "protein": 40,
          "carbs": 55,
          "fat": 28,
          "fiber": 5,
          "omega3": 2.1,
          "leucine": 3.2,
          "anti_inflammatory_score": 3,
          "tags": ["高蛋白", "Omega-3", "抗發炎"]
        }
      ],
      "meal_total": { "calories": 650, "protein": 40, "carbs": 55, "fat": 28, "fiber": 5, "leucine": 3.2 }
    }
  ],
  "daily_summary": {
    "total_calories": 650,
    "total_protein": 40,
    "total_carbs": 55,
    "total_fat": 28,
    "total_fiber": 5,
    "total_omega3": 2.1,
    "anti_inflammatory_score": 3,
    "plant_diversity": 5,
    "health_score": 78,
    "protein_distribution": {
      "breakfast": 0,
      "lunch": 40,
      "dinner": 0,
      "leucine_threshold_met": 1
    }
  }
}
```

---

## 回應風格

- 使用繁體中文
- **不使用任何 emoji 符號**
- 專業但友善，像一位懂營養學的好朋友
- 給予具體、可執行的建議
- 用數據說話，但不讓人感到壓力
- 強調長期健康而非短期減重
- 使用文字符號：[v] 達標、[x] 不足、[!] 警告
