# 规则卡索引

规则卡是本知识库的核心数据层。它把六爻断法从长篇教材拆成可检索、可验证、可追踪来源的单条规则。

结构化数据见 [rules.json](../data/rules.json)。

## 1. 规则卡分层

| layer | 含义 |
|---|---|
| question | 问题质量和起卦边界 |
| installation | 装卦、纳甲、六亲、六神、世应 |
| use_god | 取用神和辅助用神 |
| relationship | 世应、双方关系、内外环境 |
| strength | 月日旺衰、空破墓绝 |
| movement | 动爻、变爻、回头生克、进退神 |
| hidden | 飞神、伏神、用神不上卦 |
| timing | 应期 |
| topic | 财、婚、病、官、考试、失物等专题 |
| caution | 判断边界和风险 |

## 2. 第一批核心规则

### 一事一卦

同一卦只处理一个明确问题。问题越混杂，用神越难定，反馈也无法验证。

证据字段：

- `question`
- `topic`
- `time_scope`
- `querent`

### 先装卦后断卦

六爻判断依赖纳甲、六亲、六神、世应、月日等底盘。底盘错，后续判断会系统性失真。

证据字段：

- `hexagram`
- `palace`
- `branches`
- `six_kin`
- `world_response`
- `six_spirits`

### 六亲以卦宫五行为中心

配六亲时以卦宫五行为「我」，不是以世爻五行为「我」。这是初学者最容易犯的装卦错误之一。

证据字段：

- `palace_element`
- `line_element`
- `six_kin`

### 六神只作辅助取象

六神可以补充事件风格，如消息、隐情、伤灾、拖延，但不能越过用神、旺衰、动变直接定成败。

证据字段：

- `six_spirits`
- `main_god`
- `strength`
- `moving_lines`

### 世应和用神分开

世爻代表求测者立场，应爻代表对方或环境；用神代表所问事情。疾病、失物、官司等题目尤其不能把世爻简单等同于用神。

证据字段：

- `world_line`
- `response_line`
- `main_god`
- `topic`

### 月建定大势，日辰定触发

月建更像大环境和季节根气，日辰更像当下触发和近身作用。用神得月日生扶为有力，被冲克为空破受损。

证据字段：

- `month_branch`
- `day_branch`
- `main_god_branch`
- `main_god_element`

### 动爻是事件发动点

静爻有象，动爻有事。动爻对用神、世爻、应爻的生克冲合，是判断变化机制的重点。

证据字段：

- `moving_lines`
- `changed_lines`
- `main_god`
- `world_line`
- `response_line`

### 原神、忌神、仇神看传导

生用神者为原神，克用神者为忌神，克原神或生忌神者为仇神。判断时要看它们是否出现、是否发动、是否得月日。

证据字段：

- `main_god`
- `original_god`
- `avoid_god`
- `enemy_god`
- `strength`
- `moving_lines`

### 用神不上卦查伏神

用神不上卦不等于事情不存在。要查伏神、飞神、月日、生克、出伏条件。

证据字段：

- `main_god_presence`
- `hidden_god`
- `flying_god`
- `month_day`

### 空亡不是永远没有

旬空多表示暂虚、不到位、未落实。出空、填实、逢冲、动化实，都可能让空亡转为可用。

证据字段：

- `void_branches`
- `main_god_branch`
- `day_branch`
- `moving_lines`

### 合冲都要看题目

合不一定吉，可能是成事，也可能是绊住。冲不一定凶，可能是破坏，也可能是冲开阻滞。

证据字段：

- `combine`
- `clash`
- `topic`
- `main_god`
- `world_response`

### 应期从触发点取

应期常从用神临值、冲合、填空、开墓、动变地支等处取，但必须符合问题的时间尺度。

证据字段：

- `time_scope`
- `main_god_branch`
- `moving_line_branch`
- `void_branches`
- `tomb_branch`

## 3. 使用方式

查询规则：

```powershell
python .\scripts\search.py 月破
python .\scripts\search.py 原神 忌神
python .\scripts\search.py --json 旬空
python .\scripts\query.py rules 旬空
python .\scripts\query.py rules 月破 --layer strength
```

校验规则数据：

```powershell
python .\scripts\validate.py
```

## 4. 规则升级标准

一条规则从「笔记」升级为「稳定规则」至少需要：

- 有 A 类或 B 类来源。
- 知道适用条件。
- 写出例外。
- 至少能在若干案例中看到同类证据链。
- 不和更高优先级规则直接冲突；若冲突，必须标注争议。
