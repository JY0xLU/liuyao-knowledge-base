# 研究与部署日志

本日志记录资料调研、网站化、验证和部署状态。它不是学习正文，只说明当前版本做到了哪里、证据来自哪里、下一步还缺什么。

## 1. 当前版本结论

当前版本选择先做「六爻」方向，而不是同时铺开紫微斗数和六爻。原因是六爻知识可以较快拆成起卦、装卦、用神、旺衰、动变、专题和案例反馈几个结构层，适合做成本地知识库和静态检索工作台。

已经完成的基础形态：

- 本地知识库：Markdown 教材、来源索引、古籍阅读路线、规则卡、术语表、古籍读书笔记、案例槽位、案例 Schema。
- 搜索工具：`scripts/search.py` 支持全文检索，`scripts/query.py` 支持按术语、规则、来源、古籍、读书笔记、案例槽位做结构化查询。
- 静态网站：`web/index.html` 可读取内置数据包，展示学习路径、全库搜索、规则卡、术语表、古籍索引、读书笔记、案例索引、外部项目、来源库和案例录入。
- 装卦辅助：`web/liuyao-engine.js` 已支持手工输入六爻，生成本卦、变卦、动爻、卦宫、纳甲干支、地支五行、六神、六亲、自动世应、伏神提示、旬空和月建/日辰基础状态。
- 准确度验证：已加入 `data/accuracy_cases.json`、验证评分页面和评分 rubric；当前含 1 条方法演示和 3 条回测校准样本，回测样本不计入真实命中率。
- GitHub 项目化：已创建并推送 public 仓库 `JY0xLU/liuyao-knowledge-base`，已加入 `.github/workflows/check.yml`，远程 Actions 已通过一次检查。
- 后端接口：Netlify Functions 提供 `/api/search` 和 `/api/case-schema`，前端可优先用后端检索并在本地环境回退到内置数据包。
- 部署配置：`netlify.toml`、`package.json`、`.gitignore`、`scripts/predeploy_check.py` 已加入。

仍未完成的完整目标：

- 还没有把经典逐章整理到逐条原文释义和真实卦例复盘级别。
- 还没有建立大规模反馈卦例库；当前只有《增删卜易》案例抽取槽位。
- 还没有从公历自动换算月建、日辰、旬空，也还没有完整飞神伏神生克、旺衰和应期模型。
- 还没有在线保存案例的后端。
- 线上站点当前是只读知识库和检索 API，尚未接入用户案例持久化。

## 2. Agent Reach 状态

2026-06-21 当前机器上 Agent Reach 体检结果要点：

| 通道 | 状态 | 用途 |
|---|---|---|
| web / Jina Reader | 可用 | 读取公开网页和古籍页面 |
| B站 / bili-cli | 可用 | 搜索课程线索、视频目录线索 |
| RSS | 可用 | 后续订阅资料源 |
| 小宇宙 | 可用 | 后续播客转录 |
| Exa | 不可用 | 需要 mcporter + Exa MCP |
| GitHub CLI | 可用但非全局 | 本项目已下载 portable `gh` 到 `.tools/` 并完成仓库创建、推送和 Actions 验证；普通 PATH 里仍不保证有 `gh` |
| Reddit | 不可用 | 需要登录态后端 |
| 小红书 | 不可用 | 需要 OpenCLI 或专用后端 |

本轮已补 GitHub portable 工具；X、Reddit、小红书等需要登录态的通道仍按现有可用性处理。

## 3. 已纳入来源边界

本版来源按 A/B/C 分层：

- A 类：CText、维基文库、Wikimedia Commons 等经典或公共文本。
- B 类：现代教程、百科、流程文章。
- C 类：视频课程、讨论帖、个人经验材料。

采信方式：

1. A 类用于定义术语、规则主干和古籍阅读路线。
2. B 类用于补齐现代流程、学习顺序和术语解释。
3. C 类用于观察课程结构和案例线索，不直接升级为规则。

当前 `data/sources.json` 已收录 19 条来源，其中 A 类 5 条；新增的体育结果来源只用于赛果事实锁定，不用于提升六爻规则等级。

2026-06-21 新增的装卦引擎校验来源：

- `bopo/najia` README 和源码：确认卦码自下而上、纳甲表、六神、六亲、伏神字段，以及 README 中关于地天泰世应和归魂卦 bug 的修复说明。
- `bopo/najia` 测试：确认离为火 `101101` 的纳甲结果为 `己卯、己丑、己亥、己酉、己未、己巳`。
- Cosmic Tao 六爻教程：确认三钱法、八宫、六亲、世应、六神、伏神等现代流程说明。
- FateMaster 世应表：确认八纯、一至五世、游魂、归魂的世应位置。

2026-06-21 新增的回测校准赛果来源：

- Kansas City Chiefs 官方赛报：Super Bowl LVIII，Chiefs 25-22 49ers，加时。
- UEFA 官方赛报：EURO 2024 决赛，Spain 2-1 England，Oyarzabal 后段进球。
- Olympics.com 官方赛报：Paris 2024 男篮决赛，USA 98-87 France，Stephen Curry 末段关键投篮。

## 4. 网站化验证结果

本地静态工作台已完成以下验证：

| 验证项 | 结果 |
|---|---|
| 数据校验 | `scripts/validate.py` 通过：19 sources、16 terms、31 rules、4 classics、36 classic notes、24 case slots、4 accuracy cases、6 external projects |
| 数据构建 | `web/scripts/build-data.py` 通过：17 docs、16 terms、31 rules、36 notes、24 case slots、4 accuracy cases、6 external projects |
| 静态冒烟 | `web/scripts/smoke-test.py` 通过，覆盖读书笔记、案例索引、验证评分和外部项目 |
| 函数测试 | `scripts/test-functions.mjs` 通过，覆盖 `/api/search` 核心搜索语义、验证评分搜索、外部项目搜索和案例 Schema 数据 |
| 装卦测试 | `scripts/test-liuyao-engine.mjs` 通过，覆盖本卦、变卦、动爻、卦码、纳甲、卦宫、六神、六亲、自动世应、游魂、归魂、伏神、旬空和月建/日辰基础状态 |
| 部署前检查 | `scripts/predeploy_check.py` 通过，覆盖公开资产路径、规则引用、读书笔记和案例槽位 |
| 搜索脚本 | `scripts/search.py 旬空` 可返回文档、术语、规则、来源 |
| 结构化查询 | `scripts/query.py rules 旬空`、`scripts/query.py notes 旬空`、`scripts/query.py cases 失物` 均可返回结构化结果 |
| 浏览器桌面 QA | `http://127.0.0.1:8765/web/` 可加载，搜索「旬空」返回 15 张结果卡 |
| 读书笔记 QA | 读书笔记页可显示 36 张十八论/十八问答笔记卡 |
| 案例索引 QA | 案例索引页可显示 24 张《增删卜易》案例槽位卡 |
| 外部项目 QA | 外部项目页可显示 6 个 GitHub/平台参考项目 |
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
| 首页 | `https://liuyao-knowledge-base.netlify.app/` 返回 200，HTML 含 `六爻知识库` 和 `kb-data.js` |
| 外部项目 API | `/api/search?q=najia&kind=external_projects` 返回 200，首条为 `github-bopo-najia` |
| 案例索引 API | `/api/search?q=失物&kind=case_index` 返回 200，首条为 `zengshan-case-slot-010-lost-object-home` |
| 案例 Schema API | `/api/case-schema` 返回 200，Schema title 为 `LiuyaoCase` |

部署工具链记录：

- `netlify-cli@26.1.0` 通过 `pnpm dlx` 下载时因 `esbuild@0.28.0` tarball 超时失败。
- Netlify MCP uploader 已能上传干净部署副本；第一次上传误含 `.pnpm-runtime` 缓存导致长时间卡住，已把 `.pnpm-runtime/` 加入 `.gitignore` 并改用临时干净目录上传。
- Netlify 当前在部署时运行 `npm run build:netlify` 重建 `web/assets/kb-data.json`、`web/assets/kb-data.js` 和 `netlify/functions/_shared/kb-data.mjs`，避免源数据变更后发布旧资产。

## 6. 外部项目参考状态

2026-06-20 使用 GitHub 公开 API 和 Agent Reach 搜索：

- 已结构化记录 6 个参考项目：`RealKai42/liu-yao-divining`、`Brhiza/mingyu`、`bopo/najia`、`xiongdun8/liuyao`、`kentang2017/ichingshifa`、`abbeymondshein/i-ching-cli`。
- 已写入 `data/external_projects.json` 和 [外部项目与源码参考](11-external-project-benchmark.md)。
- 可借鉴重点：结构化输出、多入口 API/MCP/skill、装卦函数拆分、六神/六亲/世应/旬空测试颗粒度、AI 解读与规则数据分层。
- 风险：部分项目未确认 license；部分项目定位为娱乐或泛命理平台；GitHub API 本轮出现 rate limit，未做深度源码抓取。

## 7. 下一轮扩展优先级

### 第一优先：经典细化

1. 《卜筮正宗》十八论逐条读书笔记。
2. 每条读书笔记拆成：原章节、核心问题、规则、适用条件、例外、对应规则卡。
3. 把「十八问答」改造成案例问题集。

### 第二优先：反馈案例库

1. 从《增删卜易》抽取至少 100 条卦例。
2. 每条卦例按 `data/case_schema.json` 记录。
3. 按财、婚、病、官、考试、失物、出行等专题聚类。
4. 把规则是否应验记录成可统计字段。

### 第三优先：装卦辅助

1. 从公历时间自动换算月建、日辰、旬空。
2. 继续补飞神伏神的生克关系、旺衰、空破、墓绝、合冲和应期字段。
3. 接入案例表单，自动保存排盘字段。

### 第四优先：上线增强

1. 加入在线案例持久化后端。
2. 建立真实前瞻事件验证集，至少 20 条可评分样本。
3. 创建 release 标签和 release notes。
4. 使用线上 URL 定期复跑桌面和移动端 QA。
5. 把每轮公网验证结果写回 README 和本日志。
