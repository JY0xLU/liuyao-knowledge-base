# 六爻知识库

这是一个本地优先的六爻学习与检索知识库。当前版本先做「六爻」方向，把公开资料、传统典籍线索、现代教程框架和断卦模板整理成可搜索、可复盘的资料库。

> 定位：传统术数与文化研究资料库。这里的内容不能作为医疗、法律、金融、考试、婚恋等现实决策的唯一依据。

## 快速开始

在本目录运行：

```powershell
python .\scripts\search.py 用神
python .\scripts\search.py "月建 日辰"
python .\scripts\search.py --json "伏神"
python .\scripts\query.py rules 旬空
python .\scripts\query.py classics 卜筮正宗
python .\scripts\query.py notes 旬空
python .\scripts\query.py cases 失物
```

常用入口：

- [静态网站工作台](web/index.html)
- [学习地图](docs/00-learning-map.md)
- [基础理论](docs/01-foundations.md)
- [起卦与装卦](docs/02-casting-and-installing.md)
- [断卦框架](docs/03-judgment-framework.md)
- [专题断法](docs/04-topic-playbooks.md)
- [案例记录模板](docs/05-case-template.md)
- [古籍阅读索引](docs/06-classics-reading-index.md)
- [规则卡索引](docs/07-rule-cards.md)
- [研究与部署日志](docs/08-research-and-deployment-log.md)
- [卜筮正宗十八论与十八问答读书笔记](docs/09-bushi-zhengzong-notes.md)
- [增删卜易案例抽取索引](docs/10-zengshan-case-index.md)
- [外部项目与源码参考](docs/11-external-project-benchmark.md)
- [纳甲引擎说明](docs/12-najia-engine-notes.md)
- [准确度验证与评分](docs/13-accuracy-evaluation.md)
- [GitHub 项目化与版本迭代](docs/14-github-versioning.md)
- [版本记录](CHANGELOG.md)
- [来源索引](docs/sources.md)
- [术语表 JSON](data/terms.json)
- [来源 JSON](data/sources.json)
- [规则卡 JSON](data/rules.json)
- [古籍索引 JSON](data/classics_index.json)
- [古籍笔记 JSON](data/classic_notes.json)
- [案例索引 JSON](data/case_index.json)
- [外部项目 JSON](data/external_projects.json)
- [案例 Schema](data/case_schema.json)

## 当前交付范围

已覆盖：

- 六爻体系的学习边界和知识地图
- 起卦、动爻、变卦、本卦、互参逻辑
- 纳甲、六亲、六神、世应、伏神等装卦层
- 用神、原神、忌神、仇神、进退神、旬空、月破、日破等判断层
- 求财、感情、事业、疾病、失物、考试、出行等专题的取象规则
- 本地全文搜索脚本和结构化术语/来源数据
- 古籍阅读索引、结构化规则卡、案例数据模型和数据校验脚本
- 《卜筮正宗》十八论/十八问答结构化读书笔记
- 《增删卜易》案例抽取索引和 24 条案例槽位
- GitHub/平台类似项目参考库和可借鉴设计记录
- 自动六爻装卦辅助：本卦、变卦、动爻、卦宫、纳甲干支、地支五行、六神、六亲、自动世应、伏神提示、旬空、月建/日辰基础状态
- 事件/比赛准确度验证与评分数据模型；含 1 条方法演示和 3 条回测校准样本，回测样本不计入真实命中率
- GitHub 项目化与版本迭代说明
- 静态网站工作台、Netlify 配置和部署前检查脚本

未完成但已预留：

- 典籍逐章读书笔记
- 大量卦例拆解
- 公历自动换算月建/日辰、飞神伏神生克、旺衰和应期的完整自动判断
- 后端在线案例库
- GitHub release 与长期版本迭代；远程仓库已创建、推送并配置 CI，release 尚未创建

## 推荐学习顺序

1. 先读 [学习地图](docs/00-learning-map.md)，建立总览。
2. 再读 [基础理论](docs/01-foundations.md)，补齐阴阳、五行、干支、八卦、六十四卦。
3. 按 [起卦与装卦](docs/02-casting-and-installing.md) 手工排 20 个卦，只练流程，不急着断。
4. 用 [断卦框架](docs/03-judgment-framework.md) 拆 30 个公开案例，只写证据链。
5. 按 [专题断法](docs/04-topic-playbooks.md) 做题型化练习。
6. 每次练习都用 [案例模板](docs/05-case-template.md) 留痕，方便复盘。
7. 进阶阶段按 [古籍阅读索引](docs/06-classics-reading-index.md) 抽规则，用 [规则卡索引](docs/07-rule-cards.md) 校正规则来源。
8. 用 [研究与部署日志](docs/08-research-and-deployment-log.md) 查看当前调研边界、验证结果和下一轮扩展优先级。

## 资料采信原则

本库把来源分为三类：

- A 类：古籍、公共电子文本、可核验的经典资料。
- B 类：现代教程、百科、结构化解释文章。
- C 类：视频课程、论坛讨论、个人经验帖。

使用时先看 A 类定术语，再用 B 类补流程，最后用 C 类看案例和常见误区。C 类材料不直接升级为规则，除非能被 A/B 类资料或大量案例支持。

## 静态网站与部署

线上版本：

- [https://liuyao-knowledge-base.netlify.app](https://liuyao-knowledge-base.netlify.app)
- Netlify project: `liuyao-knowledge-base`
- Site ID: `e4b6e282-daac-49d6-b251-15acf3c896c8`
- Latest deploy: 以 Netlify 项目页为准，避免部署 ID 自引用后变成旧值。

GitHub 仓库：

- [https://github.com/JY0xLU/liuyao-knowledge-base](https://github.com/JY0xLU/liuyao-knowledge-base)

当前已提供静态网站工作台，入口为 `web/index.html`。页面内置 `web/assets/kb-data.js`，可以直接双击或用浏览器打开；若要模拟部署环境，可在本目录运行：

```powershell
python -m http.server 8765
```

然后访问 `http://127.0.0.1:8765/web/`。

本目录已经包含 Netlify 静态部署配置：

- `netlify.toml`：发布目录为 `web`，部署时运行 `npm run build:netlify` 生成 `web/assets` 与函数共享数据包。
- `netlify/functions/search.mts`：部署后提供 `GET /api/search?q=...` 后端检索接口。
- `netlify/functions/case-schema.mts`：部署后提供 `GET /api/case-schema` 案例 Schema 接口。
- `package.json`：提供 `build`、`check`、`serve` 脚本，方便本地和 CI 复用。
- `.gitignore`：排除 `.netlify/`、`node_modules/`、Python 缓存等本地状态。

部署前先运行：

```powershell
python .\scripts\check.py
npm run check
```

如使用 Netlify CLI 手动部署：

```powershell
npx netlify status
npm run check
npx netlify deploy --prod
```

如果要接入 Netlify 项目，可把本库直接作为内容源：

- Markdown 文档作为教材页
- `data/terms.json` 作为术语检索 API
- `data/sources.json` 作为参考资料库
- `data/rules.json` 作为规则卡 API
- `data/classics_index.json` 作为古籍阅读路线 API
- `data/classic_notes.json` 作为十八论/十八问答读书笔记 API
- `data/case_index.json` 作为《增删卜易》案例抽取索引 API
- `data/accuracy_cases.json` 作为事件/比赛验证评分 API
- `data/case_schema.json` 作为案例录入和校验契约
- `web/liuyao-engine.js` 作为前端纳甲装卦辅助引擎
- `web/assets/kb-data.json` 作为静态工作台数据包
- `web/assets/kb-data.js` 作为 `file://` 直接打开时的数据包
- `scripts/search.py` 的打分逻辑改写为后端检索服务
- 前端提供「学习路径、术语检索、案例录入、装卦辅助、来源追踪」五个核心页面

## 本地校验

新增或修改结构化数据后运行：

```powershell
python .\scripts\validate.py
python .\web\scripts\build-data.py
python .\web\scripts\smoke-test.py
node .\scripts\test-functions.mjs
node .\scripts\test-liuyao-engine.mjs
python .\scripts\predeploy_check.py
```

也可以直接运行聚合检查：

```powershell
python .\scripts\check.py
```

注意：`build-data.py` 必须先于 `smoke-test.py` 运行；`scripts/check.py` 会重建数据包并检查生成资产是否已同步。Netlify 部署时也会运行 `npm run build:netlify`，避免线上使用旧数据包。

结构化查询示例：

```powershell
python .\scripts\query.py terms 用神
python .\scripts\query.py rules 月破 --layer strength
python .\scripts\query.py sources 卜筮 --class A
python .\scripts\query.py classics 十八论
python .\scripts\query.py notes 回头克 --group 十八问答
python .\scripts\query.py cases 失物
```
