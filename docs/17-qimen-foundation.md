# 奇门遁甲第一版资料层

本页记录奇门遁甲第一版落地范围：术语、盘式字段、九宫、八门、九星、八神、值符值使、阴阳遁、局数和来源索引。它是知识库的结构层，不是自动起局算法，也不是断语规则库。

## 1. 本轮做了什么

| 文件 | 用途 | 入口 |
|---|---|---|
| `data/qimen_terms.json` | 奇门遁甲术语、别名、分类、定义、来源和边界说明 | 全库搜索、奇门资料页、后续案例字段 |
| `data/qimen_structures.json` | 九宫、八门、九星、八神和盘式字段结构 | 起局 Schema 设计、前端结构展示 |
| `data/qimen_case_schema.json` | 奇门案例录入契约，分开记录盘式体系、时间体系、九宫单元和值符值使 | 全库搜索、奇门资料页、`/api/qimen-case-schema` |
| `data/systems.json` | 奇门体系状态和下一步 | 多体系路线图和体系总览 |
| `data/sources.json` | 奇门百科、开源项目和视频搜索线索 | 来源库、规则采信边界 |

本轮只写结构字段，不把奇门断语混入 `data/rules.json`。后续如果增加规则，必须单独标明盘式体系、来源、适用条件、例外和案例证据。

## 2. 第一批术语范围

本轮术语覆盖 25 个入口：

- 体系：奇门遁甲、奇门盘、流派差异。
- 盘式：九宫、天盘、地盘、人盘、神盘、门星神。
- 结构：八门、九星、八神、三奇六仪、遁甲。
- 起局字段：值符、值使、阴遁阳遁、局数。
- 体系边界：转盘奇门、飞盘奇门、时家奇门、日家奇门。
- 案例复盘：用神、格局。

这些术语用于学习检索和案例字段，不代表已经完成自动排盘或断法。

## 3. 来源分级

本轮纳入的奇门来源：

| 等级 | 来源 | 用法 |
|---|---|---|
| B | 中文维基百科“奇门遁甲” | 体系、九宫、八门、九星、八神等概念入口 |
| B | 英文 Wikipedia “Qimen Dunjia” | 英文命名和跨语言概念入口 |
| B | `qfdk/qimen` | MIT 开源转盘奇门在线排盘项目，用于字段和前端盘面参考 |
| B | `arc119226/qimen_dunjia` | MIT 开源起盘模块，用于起局字段和值符值使输出颗粒度参考 |
| B | `banderzhm/ZhouYiLab` | 多体系计算引擎，用于工程分层参考 |
| C | B站奇门遁甲入门搜索结果 | 学习生态观察，不作为规则来源 |

本轮 Jina Reader 读取 Wikipedia 镜像时返回匿名 401；因此百科来源只记录可直接访问的原始页面 URL，后续逐段校对前不能升为 A 类材料。

## 4. 案例 Schema

奇门案例已经进入 `data/qimen_case_schema.json`。当前契约只支持手工录入和开源库输出留痕，不执行自动起局。共享必填字段包括：

- `id`
- `system`
- `method`
- `time_system`
- `topic`
- `question`
- `input_source`
- `chart`
- `judgment`
- `boundary_notes`

`chart.oneOf` 分成 `hour_qimen_chart` 和 `day_qimen_chart`，分别固定 `time_system = shi_jia` 和 `time_system = ri_jia`。共享盘式字段包含 `calendar_basis`、`dun_type`、`ju_number`、`xun_shou`、`fu_shou`、`zhi_fu`、`zhi_shi`、`palaces`、`topic_mapping` 和可选 `chart_json`。

九宫单元使用现有结构 ID：`palace-kan-1`、`palace-kun-2`、`palace-zhen-3`、`palace-xun-4`、`palace-center-5`、`palace-qian-6`、`palace-dui-7`、`palace-gen-8`、`palace-li-9`。八门、九星、八神只记录名称和落宫，不在本层生成吉凶断语。

## 5. 下一步

1. 建立阴阳遁、局数、值符和值使的最小测试样本。
2. 继续抽样审计 `qfdk/qimen` 和 `arc119226/qimen_dunjia` 的具体输出，对照 `chart_json` 保留字段。
3. 继续寻找可逐段校对的公开古籍文本入口，再决定哪些来源可以升为 A 类。
4. 等最小样本稳定后，再评估是否接入自动起局算法。
