# 研究与部署日志

本日志记录资料调研、网站化、验证和部署状态。它不是学习正文，只说明当前版本做到了哪里、证据来自哪里、下一步还缺什么。

## 1. 当前版本结论

当前版本以「六爻」作为第一条完整样板线，同时把奇门遁甲、大小六壬、紫微斗数拆成独立体系入口。紫微斗数已经进入第一版资料层，包含术语、十二宫、十四主星、四化和命盘字段结构；奇门遁甲也已进入第一版资料层，包含术语、九宫、八门、九星、八神和值符值使字段结构；大六壬/小六壬也已进入第一版资料层，包含子体系分层、四课、三传、十二天将、小六壬六宫、案例字段结构、独立案例 Schema 和结构样本。这样可以先把资料分层、规则追踪、案例复盘、网站化和部署链路跑通，再逐个扩展其他体系，避免把不同规则混成一套无法校验的断法。

已经完成的基础形态：

- 本地知识库：Markdown 教材、来源索引、古籍阅读路线、规则卡、术语表、古籍读书笔记、案例槽位、案例 Schema。
- 多体系骨架：已加入 `data/systems.json` 和 [多术数体系路线图](15-multi-system-roadmap.md)，把奇门遁甲、大小六壬、紫微斗数、六爻拆成独立资料层，避免规则混写。
- 紫微资料层：已加入 `data/ziwei_terms.json`、`data/ziwei_structures.json` 和 [紫微斗数第一版资料层](16-ziwei-foundation.md)，当前只记录结构字段，不写断语规则。
- 六壬资料层：已加入 `data/liuren_terms.json`、`data/liuren_structures.json`、`data/liuren_case_schema.json`、`data/liuren_case_samples.json` 和 [大六壬 / 小六壬第一版资料层](18-liuren-foundation.md)，当前只记录结构字段、案例契约和结构样本，不写断语规则。
- 搜索工具：`scripts/search.py` 支持全文检索，`scripts/query.py` 支持按术语、规则、来源、古籍、读书笔记、案例槽位做结构化查询。
- 静态网站：`web/index.html` 可读取内置数据包，展示学习路径、全库搜索、规则卡、术语表、古籍索引、读书笔记、案例索引、外部项目、来源库和案例录入。
- 装卦辅助：`web/liuyao-engine.js` 已支持手工输入六爻，生成本卦、变卦、动爻、卦宫、纳甲干支、地支五行、六神、六亲、自动世应、伏神提示、旬空和月建/日辰基础状态。
- 准确度验证：已加入 `data/accuracy_cases.json`、验证评分页面和评分 rubric；当前含 1 条方法演示和 3 条回测校准样本，回测样本不计入真实命中率。
- GitHub 项目化：已创建并推送 public 仓库 `JY0xLU/liuyao-knowledge-base`，已加入 `.github/workflows/check.yml`，远程 Actions 已通过一次检查。
- 后端接口：Netlify Functions 提供 `/api/search` 和 `/api/case-schema`，前端可优先用后端检索并在本地环境回退到内置数据包。
- 部署配置：`netlify.toml`、`package.json`、`.gitignore`、`scripts/predeploy_check.py` 已加入。

仍未完成的完整目标：

- 还没有把经典逐章整理到逐条原文释义和真实卦例复盘级别。
- 还没有把紫微斗数、奇门遁甲、大六壬/小六壬展开到六爻同等深度；紫微、奇门和六壬当前仍是第一版资料层。
- 还没有建立大规模反馈卦例库；当前只有《增删卜易》案例抽取槽位。
- 还没有从公历自动换算月建、日辰、旬空，也还没有完整飞神伏神生克、旺衰和应期模型。
- 还没有在线保存案例的后端。
- 线上站点当前是只读知识库和检索 API，尚未接入用户案例持久化。

## 2. 资料采集与工具状态

2026-06-21 的资料采集以公开网页、古籍页面、B站课程目录、GitHub 公开源码和公开赛果页面为主。需要登录态或专用后端的平台暂不作为规则来源，只作为后续采集候选。

当前规则只从可复查来源进入 A/B/C 分层；视频、论坛、社媒和个人经验材料最多作为 C 类线索，不能直接升级为规则。

## 3. 已纳入来源边界

本版来源按 A/B/C 分层：

- A 类：CText、维基文库、Wikimedia Commons 等经典或公共文本。
- B 类：现代教程、百科、流程文章。
- C 类：视频课程、讨论帖、个人经验材料。

采信方式：

1. A 类用于定义术语、规则主干和古籍阅读路线。
2. B 类用于补齐现代流程、学习顺序和术语解释。
3. C 类用于观察课程结构和案例线索，不直接升级为规则。

当前 `data/sources.json` 已收录多类来源，其中 A 类来源包含六爻经典文本和维基文库《紫微斗數全書》；体育结果来源只用于赛果事实锁定，不用于提升六爻规则等级。紫微、奇门和六壬来源只用于结构和检索入口，不直接升级为断语规则。

2026-06-21 新增的装卦引擎校验来源：

- `bopo/najia` README 和源码：确认卦码自下而上、纳甲表、六神、六亲、伏神字段，以及 README 中关于地天泰世应和归魂卦 bug 的修复说明。
- `bopo/najia` 测试：确认离为火 `101101` 的纳甲结果为 `己卯、己丑、己亥、己酉、己未、己巳`。
- Cosmic Tao 六爻教程：确认三钱法、八宫、六亲、世应、六神、伏神等现代流程说明。
- FateMaster 世应表：确认八纯、一至五世、游魂、归魂的世应位置。

2026-06-21 新增的回测校准赛果来源：

- Kansas City Chiefs 官方赛报：Super Bowl LVIII，Chiefs 25-22 49ers，加时。
- UEFA 官方赛报：EURO 2024 决赛，Spain 2-1 England，Oyarzabal 后段进球。
- Olympics.com 官方赛报：Paris 2024 男篮决赛，USA 98-87 France，Stephen Curry 末段关键投篮。

2026-06-21 新增的紫微资料层来源：

- 维基文库《紫微斗數全書》：作为 A 类公共古籍文本候选，用于星曜、宫位和结构字段索引；引用前仍需逐段校对。
- 中文维基百科“紫微斗数”和英文 Wikipedia “Zi Wei Dou Shu”：作为 B 类百科导览，用于概念入口和跨语言命名。
- `Renhuai123/ziwei-doushu`：MIT 开源 TypeScript 排盘项目，用于字段、四化系统和测试颗粒度参考。
- `taskyoooo/ziwei-doushu-skill`：作为 C 类产品形态线索，不作为规则来源。

## 4. 网站化验证结果

本地静态工作台已完成以下验证：

| 验证项 | 结果 |
|---|---|
| 数据校验 | `scripts/validate.py` 通过：19 sources、4 systems、16 terms、31 rules、4 classics、36 classic notes、24 case slots、4 accuracy cases、6 external projects |
| 数据构建 | `web/scripts/build-data.py` 通过：18 docs、4 systems、16 terms、31 rules、36 notes、24 case slots、4 accuracy cases、6 external projects |
| 静态冒烟 | `web/scripts/smoke-test.py` 通过，覆盖多体系入口、读书笔记、案例索引、验证评分和外部项目 |
| 函数测试 | `scripts/test-functions.mjs` 通过，覆盖 `/api/search` 核心搜索语义、体系搜索、验证评分搜索、外部项目搜索和案例 Schema 数据 |
| 装卦测试 | `scripts/test-liuyao-engine.mjs` 通过，覆盖本卦、变卦、动爻、卦码、纳甲、卦宫、六神、六亲、自动世应、游魂、归魂、伏神、旬空和月建/日辰基础状态 |
| 部署前检查 | `scripts/predeploy_check.py` 通过，覆盖公开资产路径、体系入口、规则引用、读书笔记和案例槽位 |
| 搜索脚本 | `scripts/search.py 旬空` 可返回文档、术语、规则、来源 |
| 结构化查询 | `scripts/query.py rules 旬空`、`scripts/query.py notes 旬空`、`scripts/query.py cases 失物` 均可返回结构化结果 |
| 浏览器桌面 QA | `http://127.0.0.1:8765/web/` 可加载，搜索「旬空」返回 15 张结果卡 |
| 读书笔记 QA | 读书笔记页可显示 36 张十八论/十八问答笔记卡 |
| 案例索引 QA | 案例索引页可显示 24 张《增删卜易》案例槽位卡 |
| 外部项目 QA | 外部项目页可显示 6 个 GitHub/平台参考项目 |
| 紫微资料 QA | 新增紫微资料页和后端搜索 kind，覆盖 `ziwei_terms` 与 `ziwei_structures` |
| 奇门资料 QA | 新增奇门资料页和后端搜索 kind，覆盖 `qimen_terms` 与 `qimen_structures` |
| 六壬资料 QA | 新增六壬资料页和后端搜索 kind，覆盖 `liuren_terms` 与 `liuren_structures` |
| 六壬案例 Schema QA | 新增 `liuren_case_schema` 数据包、搜索 kind 和 `/api/liuren-case-schema` |
| 六壬案例样本 QA | 新增 `liuren_case_samples` 数据包、搜索 kind、CLI 查询和六壬资料页样本展示 |
| 案例录入 QA | 案例页可填写问题字段，能显示 `case_schema.json` 标识 |
| 移动端 QA | 390px 断点生效，`.app-shell` 变为单列布局 |
| 控制台 | 浏览器 QA 中未记录 error/warn |

`file://` 直接打开已在文件层由 `web/assets/kb-data.js` 支持；Browser 插件阻止访问 `file://` 页面，因此没有绕过安全策略做浏览器复查。

## 5. Netlify 状态

Netlify 上线结果：

- Team: `jy0xlu`
- Project: `liuyao-knowledge-base`
- Site ID: `e4b6e282-daac-49d6-b251-15acf3c896c8`
- Site URL: https://liuyao-knowledge-base.netlify.app
- Latest deploy: 以 Netlify 项目页为准，避免部署 ID 自引用后变成旧值。
- Deploy state: `ready`

线上 HTTP 验证：

| 验证项 | 结果 |
|---|---|
| 首页 | `https://liuyao-knowledge-base.netlify.app/` 返回 200，HTML 含 `kb-data.js` |
| 体系搜索 API | `/api/search?q=紫微斗数&kind=systems` 返回 200，结果包含 `ziwei` |
| 外部项目 API | `/api/search?q=najia&kind=external_projects` 返回 200，首条为 `github-bopo-najia` |
| 案例索引 API | `/api/search?q=失物&kind=case_index` 返回 200，首条为 `zengshan-case-slot-010-lost-object-home` |
| 案例 Schema API | `/api/case-schema` 返回 200，Schema title 为 `LiuyaoCase` |

部署工具链记录：

- Netlify 部署时运行 `npm run build:netlify` 重建 `web/assets/kb-data.json`、`web/assets/kb-data.js` 和 `netlify/functions/_shared/kb-data.mjs`，避免源数据变更后发布旧资产。
- 发布前使用干净部署副本，只包含源码、文档、数据、前端和函数目录，不携带本地缓存或临时工具目录。

## 6. 外部项目参考状态

2026-06-20 使用 GitHub 公开 API 和 Agent Reach 搜索：

- 已结构化记录 6 个参考项目：`RealKai42/liu-yao-divining`、`Brhiza/mingyu`、`bopo/najia`、`xiongdun8/liuyao`、`kentang2017/ichingshifa`、`abbeymondshein/i-ching-cli`。
- 已写入 `data/external_projects.json` 和 [外部项目与源码参考](11-external-project-benchmark.md)。
- 可借鉴重点：结构化输出、多入口 API/MCP/skill、装卦函数拆分、六神/六亲/世应/旬空测试颗粒度、AI 解读与规则数据分层。
- 风险：部分项目未确认 license；部分项目定位为娱乐或泛命理平台；GitHub API 本轮出现 rate limit，未做深度源码抓取。

## 7. 下一轮扩展优先级

### 第一优先：紫微资料层深化

1. 校对《紫微斗數全書》里十二宫、十四主星和四化相关段落。
2. 建立 `data/ziwei_case_schema.json`，先支持手工命例录入。
3. 对 `Renhuai123/ziwei-doushu` 做源码和测试抽样，确认命盘字段、四化输入输出和流派边界。
4. 收集公开命例或事件复盘，回测样本只用于字段校准，不计入真实准确率。

### 第二优先：经典细化

1. 《卜筮正宗》十八论逐条读书笔记。
2. 每条读书笔记拆成：原章节、核心问题、规则、适用条件、例外、对应规则卡。
3. 把「十八问答」改造成案例问题集。

### 第三优先：反馈案例库

1. 从《增删卜易》抽取至少 100 条卦例。
2. 每条卦例按 `data/case_schema.json` 记录。
3. 按财、婚、病、官、考试、失物、出行等专题聚类。
4. 把规则是否应验记录成可统计字段。

### 第四优先：装卦辅助

1. 从公历时间自动换算月建、日辰、旬空。
2. 继续补飞神伏神的生克关系、旺衰、空破、墓绝、合冲和应期字段。
3. 接入案例表单，自动保存排盘字段。

### 第五优先：上线增强

1. 加入在线案例持久化后端。
2. 建立真实前瞻事件验证集，至少 20 条可评分样本。
3. 创建 release 标签和 release notes。
4. 使用线上 URL 定期复跑桌面和移动端 QA。
5. 把每轮公网验证结果写回 README 和本日志。

## 2026-06-21 奇门遁甲第一版资料层

- 新增 `data/qimen_terms.json`：25 个奇门术语，覆盖奇门盘、九宫、八门、九星、八神、值符值使、阴阳遁、局数、转盘/飞盘和时家/日家边界。
- 新增 `data/qimen_structures.json`：九宫、八门、九星、八神和盘式字段结构。
- 新增 [奇门遁甲第一版资料层](17-qimen-foundation.md)，明确本轮只做结构资料，不实现自动起局，不写确定性断语。
- 接入前端“奇门资料”视图、后端 `qimen_terms` / `qimen_structures` 搜索池、CLI 查询和部署前检查。
- 调研边界：Jina Reader 读取 Wikipedia 镜像返回匿名 401；本轮使用可直接访问的百科 URL 与 GitHub 元数据，B站搜索只作为 C 类学习生态线索。

## 2026-06-21 奇门案例 Schema

- 新增 `data/qimen_case_schema.json`：共享字段包含 `id`、`system`、`method`、`time_system`、`topic`、`question`、`input_source`、`chart`、`judgment`、`outcome`、`score`、`license_notes` 和 `boundary_notes`。
- `chart.oneOf` 分为 `hour_qimen_chart` 与 `day_qimen_chart`，分别固定 `shi_jia` 和 `ri_jia`；共享盘式字段包含 `calendar_basis`、`dun_type`、`ju_number`、`xun_shou`、`fu_shou`、`zhi_fu`、`zhi_shi`、`palaces`、`topic_mapping` 和 `chart_json`。
- 新增 `/api/qimen-case-schema`，并把 `qimen_case_schema` 接入后端搜索池、本地搜索、CLI 查询、奇门资料页、静态数据包和部署前检查。
- Agent Reach doctor 显示 Web/Jina、B站、V2EX、RSS 可用；GitHub 全局检测未找到 `gh`，但仓库内本地 `gh` 可用。GitHub 元数据确认 `qfdk/qimen`、`arc119226/qimen_dunjia`、`banderzhm/ZhouYiLab` 均为 MIT 且 2026-06-19/20 有更新记录，本轮只采用字段形态参考。

## 2026-06-21 大六壬 / 小六壬第一版资料层

- 新增 `data/liuren_terms.json`：覆盖六壬、大六壬、小六壬、月将、占时、天地盘、四课、三传、发用、十二天将、课体和小六壬六宫。
- 新增 `data/liuren_structures.json`：子体系、大六壬课式字段、四课、三传、十二天将、小六壬六宫和案例字段结构。
- 新增 [大六壬 / 小六壬第一版资料层](18-liuren-foundation.md)，明确本轮只做结构资料，不实现自动起课，不写确定性断语。
- 接入前端“六壬资料”视图、后端 `liuren_terms` / `liuren_structures` 搜索池、CLI 查询和部署前检查。
- 调研边界：Node fetch 可直接访问“大六壬 / 六壬”和“六曜 / 小六壬”页面；GitHub 元数据确认 `kentang2017/kinliuren`、`look-fate/liuren-ts-lib` 和 `maifusha/xiaoliuren`；B站搜索只作为 C 类学习生态线索。

## 2026-06-21 六壬案例 Schema

- 新增 `data/liuren_case_schema.json`：共享字段包含 `id`、`system`、`subsystem`、`topic`、`question`、`input_source`、`chart`、`judgment`、`outcome`、`score`、`license_notes` 和 `boundary_notes`。
- 大六壬分支记录 `calendar_basis`、`month_general`、`divination_hour`、`day_ganzhi`、`plates`、`four_lessons`、`three_transmissions`、`heavenly_generals`、`lesson_types` 和 `markers`。
- 小六壬分支记录 `qike_start`、`solar_date`、`lunar_date`、`hour_branch`、`finger_count`、`sangong`、`selected_palace`、`palace_order` 和 `favorable_hours`。
- 新增 `/api/liuren-case-schema`，并把 `liuren_case_schema` 接入后端搜索池、本地搜索、CLI 查询、静态数据包和部署前检查。
- 源码抽样边界：`kinliuren` 和 `maifusha/xiaoliuren` 为 MIT，可作字段和接口参考；`liuren-ts-lib` 为 Apache-2.0，可作 Web/API 字段结构参考；`wlhyl/dalurenpython` 未确认 license，只作词汇观察，不复制代码或数据。

## 2026-06-21 六壬案例样本层

- 新增 `data/liuren_case_samples.json`：包含 `liuren-sample-da-structure-001` 和 `liuren-sample-xiao-structure-001` 两条结构样本。
- 大六壬样本覆盖月将、占时、天地盘、四课、三传、十二天将、课体标签和 markers；小六壬样本覆盖起课入口、日期字段、时辰、掐指计数、三宫递进、最终六宫和六宫顺序。
- 样本全部标记为 `schema_fixture`，`score.mode` 为 `retrospective_calibration_not_accuracy`，`score.total` 为 `0`，不进入真实准确率。
- 接入后端 `liuren_case_samples` 搜索池、本地搜索、CLI 查询、六壬资料页、静态数据包、校验脚本、冒烟测试、函数测试和部署前检查。
- 子代理 QA 确认应保持该层独立于 `case_index` 和 `accuracy_cases`，并要求 `subsystem` 与 `chart.subsystem` 一致、来源 id 可追踪、样本不能携带本机路径或私密字段。
