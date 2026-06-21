# 大六壬 / 小六壬第一版资料层

本页记录六壬体系的第一版资料层。它只做术语、课式字段和来源边界，不自动起课，也不写确定性断语。

## 1. 分层原则

六壬在本库中拆成两个子层：

| 子层 | 第一版范围 | 暂不做 |
|---|---|---|
| 大六壬 | 月将、占时、天地盘、四课、三传、十二天将、课体和案例字段 | 自动起课、课体判断、应期和断语 |
| 小六壬 | 大安、留连、速喜、赤口、小吉、空亡六宫和取数字段 | 速断口诀、吉凶结论、与大六壬混合评分 |

这样做是为了避免把两个复杂度完全不同的体系混成一套规则。大六壬后续更适合做课式 Schema、起课算法和课体测试；小六壬后续更适合做六宫速查、取数来源和轻量案例校验。

## 2. 已落地数据

- `data/liuren_terms.json`：六壬术语层，覆盖六壬、大六壬、小六壬、月将、占时、天地盘、四课、三传、发用、十二天将、课体和小六壬六宫。
- `data/liuren_structures.json`：六壬结构层，覆盖两个子体系、大六壬课式字段、四课、三传、十二天将、小六壬六宫和案例字段。
- `data/liuren_case_schema.json`：六壬案例 Schema，使用共享字段加大六壬/小六壬两个分支，保留输入来源、课式 JSON、结果、评分、许可和边界说明。
- `data/systems.json`：六壬状态更新为 `active-v0.7-seed`。
- `data/sources.json`：新增大六壬、小六壬百科入口、开源项目和 B站搜索线索。
- `data/external_projects.json`：新增 `kentang2017/kinliuren`、`look-fate/liuren-ts-lib`、`maifusha/xiaoliuren` 三个六壬参考项目。

## 3. 大六壬结构字段

第一版只记录复盘和后续算法所需字段：

- 输入字段：月将、占时、日干、日支。
- 盘层字段：天地盘、天盘、地盘。
- 课式字段：四课、三传、发用、课体。
- 天将字段：贵人、螣蛇、朱雀、六合、勾陈、青龙、天空、白虎、太常、玄武、太阴、天后。
- 案例字段：题型、输入来源、课式 JSON、规则来源、结果、评分、许可说明和边界说明。

这些字段是资料结构，不是判断结论。后续如果接入起课算法，必须先建立月将、占时、四课、三传、十二天将和课体的固定测试样本。

## 4. 小六壬结构字段

小六壬第一版只记录六宫：

| 顺序 | 名称 |
|---|---|
| 1 | 大安 |
| 2 | 留连 |
| 3 | 速喜 |
| 4 | 赤口 |
| 5 | 小吉 |
| 6 | 空亡 |

这里的“空亡”是小六壬六宫名称，不等同于六爻中的旬空。案例、规则和评分必须保留子体系字段，避免跨体系误用。

小六壬案例 Schema 记录起课宫位、阳历/阴历日期、时辰、掐指计数、三宫落点、最终六宫和原始输出 JSON。六宫速断文本暂不进入规则层。

## 5. 案例 Schema

`data/liuren_case_schema.json` 目前分三层：

- 共享字段：`id`、`system`、`subsystem`、`topic`、`question`、`input_source`、`judgment`、`outcome`、`score`、`source_refs`、`license_notes` 和 `boundary_notes`。
- 大六壬分支：`calendar_basis`、`month_general`、`divination_hour`、`day_ganzhi`、`plates`、`four_lessons`、`three_transmissions`、`heavenly_generals`、`lesson_types` 和 `markers`。
- 小六壬分支：`qike_start`、`solar_date`、`lunar_date`、`hour_branch`、`finger_count`、`sangong`、`selected_palace`、`palace_order` 和 `favorable_hours`。

后端新增 `GET /api/liuren-case-schema`，前端六壬资料页也会展示 Schema 摘要。这样后续可以先做手工案例录入和固定样本，再接起课算法。

## 6. 来源边界

本轮调研使用：

- 维基百科“大六壬 / 六壬”页面：用于大六壬、四课、三传和十二天将等结构入口。
- 维基百科“六曜 / 小六壬”重定向入口：用于小六壬六宫名称入口。
- `kentang2017/kinliuren`：MIT 开源 Python 大六壬包，用作字段和测试颗粒度参考。
- `look-fate/liuren-ts-lib`：Apache-2.0 TypeScript 六壬神课库，用作后续 Web/API 算法候选。
- `maifusha/xiaoliuren`：MIT Go 小六壬实现，用作小六壬接口和六宫字段参考。
- `wlhyl/dalurenpython`：未确认 license，只作为字段词汇交叉观察，不复制代码或数据。
- B站搜索结果：只作为课程生态观察，不升级为规则。

## 7. 下一步

1. 把 `kinliuren` 和 `liuren-ts-lib` 的输入输出转成固定测试样本。
2. 为小六壬建立六宫取数来源样本，但不把速断口诀直接写成规则。
3. 基于 `liuren_case_schema.json` 做手工案例导入/导出。
4. 寻找可校对的公开古籍文本入口，再把经典资料逐条挂到术语和规则层。
