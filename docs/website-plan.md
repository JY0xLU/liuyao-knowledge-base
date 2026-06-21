# 网站化方案

本地知识库已经把内容拆成 Markdown 文档和 JSON 数据。网站化时不需要重写内容，只需要把这些文件作为内容源。

## 1. 产品定位

网站第一版已经做成「术数知识库工作台」，不是营销页。当前以六爻作为完整样板线，紫微斗数、奇门遁甲和大六壬/小六壬已进入第一版术语和结构资料层。

核心用户：

- 初学者：需要按学习路径掌握术语和流程。
- 进阶学习者：需要快速查术语、规则、古籍来源。
- 案例复盘者：需要记录卦例、标注用神、动变、反馈。
- 后续扩展维护者：需要清楚区分六爻、紫微、奇门、六壬的资料层和规则边界。

## 2. 首屏结构

首屏直接进入工作台：

- 左侧：学习路径导航。
- 中间：当前教材或搜索结果。
- 右侧：术语卡、来源卡、案例快捷记录。
- 顶部：全局搜索框、主题筛选、来源等级筛选。

不做大幅营销 hero，不做单纯介绍页。

## 3. 页面清单

| 页面 | 功能 |
|---|---|
| 学习路径 | 展示 `docs/00-learning-map.md` 的章节导航和进度 |
| 体系总览 | 读取 `data/systems.json`，展示六爻、紫微斗数、奇门遁甲、大六壬/小六壬的状态、核心对象、资料路线和风险边界 |
| 教材阅读 | 渲染 `docs/*.md`，支持标题目录和引用跳转 |
| 术语检索 | 读取 `data/terms.json`，按 term、alias、category 搜索 |
| 紫微资料 | 读取 `data/ziwei_terms.json` 和 `data/ziwei_structures.json`，展示紫微术语、十二宫、十四主星、四化和命盘字段 |
| 奇门资料 | 读取 `data/qimen_terms.json` 和 `data/qimen_structures.json`，展示奇门术语、九宫、八门、九星、八神和值符值使字段 |
| 六壬资料 | 读取 `data/liuren_terms.json`、`data/liuren_structures.json`、`data/liuren_case_schema.json` 和 `data/liuren_case_samples.json`，展示大六壬/小六壬术语、四课三传、十二天将、小六壬六宫、案例字段、案例 Schema 和结构样本 |
| 来源库 | 读取 `data/sources.json`，按 A/B/C 类、类型、关键词筛选 |
| 规则卡 | 读取 `data/rules.json`，按 layer、source_refs、confidence 筛选 |
| 古籍路线 | 读取 `data/classics_index.json`，展示每部经典的阅读任务 |
| 外部项目 | 读取 `data/external_projects.json`，展示类似项目、源码参考、可借鉴点和风险 |
| 案例库 | 新建、编辑、搜索案例，使用 `docs/05-case-template.md` 字段 |
| 装卦辅助 | 手工输入六爻，自动生成本卦、变卦、动爻、卦宫、纳甲、六亲、六神、世应、伏神、旬空和月日状态 |
| 验证评分 | 读取 `data/accuracy_cases.json`，展示事件验证、实际结果和评分维度 |

## 4. 前端建议

当前栈：

- 静态 HTML、CSS 和原生 JavaScript。
- 构建脚本把 Markdown 与 JSON 汇总为 `web/assets/kb-data.json` 和 `web/assets/kb-data.js`。
- 前端使用内置数据包做离线检索，部署后优先调用 `/api/search`。
- Netlify Functions 只承担搜索和 Schema 这类薄 API。

暂不引入 React、Next、数据库、登录或复杂权限。等真实案例量、多人协作和在线保存需求明确后，再决定是否升级到 React/Next + SQLite/Postgres。

界面原则：

- 信息密度高，适合查资料。
- 不使用玄学感过强的装饰，避免廉价感。
- 用标签区分「经典来源」「现代教程」「视频/讨论」。
- 每条规则旁边能显示来源等级和来源链接。

## 5. 后端建议

第一版可零后端：

- 构建时读取 Markdown 和 JSON。
- 浏览器端完成搜索。
- 案例先保存为本地导入/导出 JSON。

当前版本已经在零数据库基础上补了 Netlify Functions：

- `GET /api/search?q=...`：读取构建期数据模块，返回文档、规则、术语、紫微术语、紫微结构、奇门术语、奇门结构、六壬术语、六壬结构、六壬案例 Schema、来源、古籍、读书笔记和案例槽位的统一检索结果。
- `GET /api/search?q=四化&kind=ziwei_terms`：检索紫微术语。
- `GET /api/search?q=命宫&kind=ziwei_structures`：检索紫微盘式结构。
- `GET /api/search?q=八门&kind=qimen_terms`：检索奇门术语。
- `GET /api/search?q=坎一宫&kind=qimen_structures`：检索奇门盘式结构。
- `GET /api/search?q=三传&kind=liuren_terms`：检索六壬术语。
- `GET /api/search?q=初传&kind=liuren_structures`：检索六壬课式结构。
- `GET /api/search?q=four_lessons&kind=liuren_case_schema`：检索六壬案例 Schema。
- `GET /api/search?q=结构样本&kind=liuren_case_samples`：检索六壬案例结构样本。
- `GET /api/search?q=najia&kind=external_projects`：检索类似项目与源码参考。
- `GET /api/case-schema`：返回案例录入 Schema，方便后续在线案例保存接口复用。
- `GET /api/liuren-case-schema`：返回大六壬 / 小六壬案例录入 Schema。
- 前端搜索会优先尝试 `/api/search`；本地 `file://` 或普通静态服务不可用时，自动回退到内置数据包检索。

进阶版再加后端：

- SQLite 存术语、来源、案例。
- FTS5 做全文搜索。
- API：
  - `GET /api/search?q=...`
  - `GET /api/terms`
  - `GET /api/sources`
  - `GET /api/rules`
  - `GET /api/classics`
  - `GET /api/docs/:slug`
  - `POST /api/cases`
  - `GET /api/cases?topic=...`

## 6. 数据模型

### Term

```json
{
  "term": "用神",
  "aliases": ["主用神"],
  "category": "judgment",
  "definition": "...",
  "see_also": ["原神", "忌神"],
  "source_refs": ["ctext-bushi-zhengzong"]
}
```

### Source

```json
{
  "id": "ctext-bushi-zhengzong",
  "title": "卜筮正宗 - 中国哲学书电子化计划",
  "url": "https://ctext.org/wiki.pl?chapter=889452&if=gb",
  "class": "A",
  "type": "classic",
  "notes": "..."
}
```

### Case

```json
{
  "id": "case-2026-06-20-001",
  "question": "本周五面试能否进入下一轮？",
  "topic": "事业",
  "cast_time": "2026-06-20T10:30:00+08:00",
  "main_god": "官鬼",
  "world_line": "...",
  "response_line": "...",
  "judgment": "...",
  "feedback": "..."
}
```

### Rule

```json
{
  "id": "month-environment-day-trigger",
  "title": "月建定大势，日辰定触发",
  "layer": "strength",
  "statement": "...",
  "source_refs": ["ctext-bushi-zhengzong"],
  "confidence": "A"
}
```

## 7. 当前静态工作台

当前仓库已经包含第一版静态工作台：

- 入口：`web/index.html`
- 样式：`web/styles.css`
- 交互：`web/app.js`
- 数据包：`web/assets/kb-data.json` 和 `web/assets/kb-data.js`
- 后端接口：`netlify/functions/search.mts`、`netlify/functions/case-schema.mts` 和 `netlify/functions/liuren-case-schema.mts`
- 数据构建：`web/scripts/build-data.py`
- 冒烟测试：`web/scripts/smoke-test.py`
- 函数测试：`scripts/test-functions.mjs`
- 部署前检查：`scripts/predeploy_check.py`

它不是占位原型，而是可用的本地学习和检索界面。当前支持：

- 文档阅读
- 全库检索
- 部署后 API 检索，离线时本地回退
- 外部项目参考库
- 规则卡浏览
- 术语速查
- 古籍路线浏览
- 来源库浏览
- 紫微资料浏览：术语、十二宫、十四主星、四化、命盘字段
- 奇门资料浏览：术语、九宫、八门、九星、八神、值符值使、盘式字段
- 六壬资料浏览：术语、子体系、四课、三传、十二天将、小六壬六宫、案例字段、案例 Schema 和案例结构样本
- 案例录入和 JSON 导出
- 装卦辅助：本卦、变卦、卦码、纳甲干支、地支五行、卦宫、六亲、六神、世应、伏神、旬空和月日状态
- 验证评分：比赛、人物或公开事件的预测、结果和评分 rubric

## 8. 部署路线

### 静态版

当前第一阶段已采用：

- 静态 `web` 目录。
- 部署到 Netlify、Vercel 或 GitHub Pages。
- 优点：快、稳定、无数据库。
- 缺点：案例不能多人在线保存，除非接第三方存储。

### 全栈版

适合第二阶段：

- Next.js + SQLite/Postgres。
- 部署到 Vercel/Netlify + 托管数据库。
- 增加登录、私有案例、全文检索和批注。

## 9. 下一步实施清单

1. 持续扩展 `data/systems.json`，但不同体系不要混写规则。
2. 为紫微补 `data/ziwei_case_schema.json` 和排盘算法测试用例。
3. 为奇门补 `data/qimen_case_schema.json`、源码抽样和节气/局数/值符值使测试。
4. 为六壬补源码抽样样本和月将/占时/四课三传算法回归测试。
5. 用线上 URL 复跑桌面搜索、案例录入、体系总览、紫微资料、奇门资料、六壬资料和移动端布局 QA。
6. 建立至少 20 条事前锁定的真实前瞻样本后，再公开命中率。
7. 第二阶段再决定是否新建 React/Next 工程；当前静态工作台已经足够承载第一版学习、检索和体系路线图。
