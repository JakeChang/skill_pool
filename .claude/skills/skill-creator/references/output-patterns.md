# 輸出模式

當技能需要產生一致、高品質的輸出時，使用這些模式。

## 範本模式

提供輸出格式的範本。根據你的需求匹配嚴格程度。

**對於嚴格要求（如 API 回應或資料格式）：**

```markdown
## 報告結構

務必使用此確切的範本結構：

# [分析標題]

## 執行摘要
[關鍵發現的一段概述]

## 主要發現
- 發現 1 及支持資料
- 發現 2 及支持資料
- 發現 3 及支持資料

## 建議
1. 具體可行的建議
2. 具體可行的建議
```

**對於彈性指導（當需要適應性調整時）：**

```markdown
## 報告結構

這是一個合理的預設格式，但請運用你的最佳判斷：

# [分析標題]

## 執行摘要
[概述]

## 主要發現
[根據你的發現調整各部分]

## 建議
[針對具體情境量身定制]

根據特定分析類型的需要調整各部分。
```

## 範例模式

對於輸出品質取決於看到範例的技能，提供輸入/輸出配對：

```markdown
## Commit 訊息格式

依照以下範例生成 commit 訊息：

**範例 1：**
輸入：Added user authentication with JWT tokens
輸出：
```
feat(auth): implement JWT-based authentication

Add login endpoint and token validation middleware
```

**範例 2：**
輸入：Fixed bug where dates displayed incorrectly in reports
輸出：
```
fix(reports): correct date formatting in timezone conversion

Use UTC timestamps consistently across report generation
```

遵循此風格：type(scope): 簡短描述，然後是詳細說明。
```

範例比單純的描述更能幫助 Claude 理解所需的風格和詳細程度。
