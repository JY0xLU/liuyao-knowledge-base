# 增删卜易案例抽取索引

本索引用来把《增删卜易》从“可阅读古籍”转成“可复盘案例库”。当前版本先建立案例槽位和抽取字段，不伪造原文案例和结果。

## 1. 抽取原则

1. 每条案例必须保留原问题，不用现代话替换问题核心。
2. 必须记录主用神、辅助用神、月建、日辰、动爻、变爻、空破墓绝。
3. 必须记录古籍判断和实际反馈；没有反馈的条目只算练习。
4. 每条案例至少连接一条 `data/rules.json` 中的规则。
5. 规则冲突时保留 `conflict_note`，不要为了整洁强行统一。

## 2. 当前案例槽位

`data/case_index.json` 当前建立 24 条案例抽取槽位，覆盖：

- 求财、货款、投资、交易
- 求职、升迁、考试、文书
- 感情、复合、关系反复
- 病情、医药、检查
- 失物、被盗、隐情、伏藏
- 出行、行人、消息、通知
- 官司、合同、家宅、子女
- 旬空、月破、进退神、反吟伏吟等规则专题

每个槽位都包含：

- `topic`
- `case_type`
- `question_pattern`
- `main_god`
- `secondary_gods`
- `must_record`
- `linked_rule_ids`
- `status`

## 3. 抽取字段模板

后续把槽位升级为真实案例时，建议按以下结构写入：

```json
{
  "id": "zengshan-case-0001",
  "source_ref": "wikisource-zengshan-buyi",
  "source_location": "卷/门类/原章节定位",
  "topic": "wealth",
  "question_original": "原问题",
  "question_modern": "现代语义解释",
  "cast_time": "未知或原文日期",
  "hexagram": {
    "primary": "",
    "changed": "",
    "moving_lines": []
  },
  "use_gods": {
    "main": "妻财",
    "secondary": ["子孙", "兄弟"]
  },
  "evidence": {
    "month_day": "",
    "void": "",
    "break": "",
    "movement": "",
    "world_response": ""
  },
  "judgment": {
    "ancient_summary": "",
    "modern_reconstruction": "",
    "rule_refs": []
  },
  "feedback": {
    "actual_result": "",
    "hit_or_miss": "hit | partial | miss | unknown",
    "miss_reason": ""
  }
}
```

## 4. 专题抽取优先级

### 第一批：反馈最容易验证

| 专题 | 目标 |
|---|---|
| 失物 | 结果明确，适合验证伏神、玄武、内外卦 |
| 消息 | 时间反馈清晰，适合验证父母、朱雀、旬空 |
| 货款 | 是否到账可验证，适合验证财爻、兄弟、父母 |
| 面试 | 是否录用可验证，适合验证官鬼、父母、世应 |

### 第二批：规则冲突多

| 专题 | 目标 |
|---|---|
| 感情复合 | 验证世应、合冲、反吟伏吟 |
| 病情医药 | 验证官鬼、子孙、父母，但只作文化记录 |
| 官司争议 | 验证官鬼、父母、世应双方 |
| 家宅房屋 | 验证父母、墓库、财爻交易 |

### 第三批：规则专题

| 专题 | 目标 |
|---|---|
| 旬空 | 统计出空、填实、逢冲、动化实 |
| 月破 | 统计用神月破和忌神月破差异 |
| 进退神 | 统计趋势增强/减弱是否被反馈验证 |
| 反吟伏吟 | 统计反复、迟滞、内耗是否真实出现 |

## 5. 本轮外部检索记录

2026-06-20 的公开资料采集：

- `bili search "增删卜易 卦例 六爻" --type video -n 8` 返回《增删卜易》全套及多条编号卦例视频线索，包含 `BV1ky8kz7EqG`、`BV1zB4reGEWL`、`BV1qE421F72V`、`BV1bQseeYETc`、`BV14s4nehEek`、`BV1uw4m1k7wR` 等。
- 本轮只记录 bvid 和“存在案例视频线索”这一事实，不把视频标题或讲解内容升级为规则。

## 6. 下一步

1. 把《增删卜易》公共文本按门类切成章节索引。
2. 每个专题先抽 5 条案例，填入 `case_index.json` 的真实案例字段。
3. 对每条案例补 `hit_or_miss`。
4. 每满 20 条案例，复盘一次规则置信度。
