# 来源索引

本索引记录第一版知识库用到的公开资料线索。它不是完整书目，后续应继续扩展到逐章读书笔记和案例库。

当前深入资料主要集中在六爻。紫微斗数、奇门遁甲、大六壬/小六壬先进入 [多术数体系路线图](15-multi-system-roadmap.md) 和 `data/systems.json`，后续按体系独立扩展来源、术语、盘式和案例，不与六爻规则混写。

## A 类：经典与公共文本

| 标题 | 链接 | 用途 |
|---|---|---|
| 卜筮正宗 - 中国哲学书电子化计划 | https://ctext.org/wiki.pl?chapter=889452&if=gb | 经典系统框架、用神原忌仇、飞伏、旬空月破等纲领 |
| 增删卜易 - 维基文库 | https://zh.wikisource.org/wiki/%E5%A2%9E%E5%88%AA%E5%8D%9C%E6%98%93 | 分类占断和卦例学习线索；页面自身提示未完全校对，使用时需核验 |
| 黄金策 - 维基文库 | https://zh.wikisource.org/wiki/%E9%BB%84%E9%87%91%E7%AD%96 | 火珠林法经典资料，适合总纲和分类断法 |
| 黄金策 - 中国哲学书电子化计划 | https://ctext.org/wiki.pl?chapter=767055&if=gb&remap=gb | 对照阅读黄金策文本 |
| 易隐 PDF - Wikimedia Commons | https://upload.wikimedia.org/wikipedia/commons/2/27/NLC416-12jh005346-45345_%E6%98%93%E9%9A%B1.pdf | 古籍脉络与纳甲筮法扩展 |

## B 类：现代教程与百科

| 标题 | 链接 | 用途 |
|---|---|---|
| 纳甲说 - 中国孔子网 | https://www.chinakongzi.org/baike/MINGCI/zhexue/201708/t20170825_142777.htm | 纳甲说源流与京房易背景 |
| 六爻神卦 - 维基百科 | https://zh.wikipedia.org/wiki/%E5%85%AD%E7%88%BB%E7%A5%9E%E5%8D%A6 | 六爻作为民间卜卦方式的概览 |
| 六爻纳甲怎么装卦 - 天机要 | https://wiki.tianjiyao.com/yijing/najia-system.html | 纳甲、六亲、六神、世应、伏神的现代入门框架 |
| 六爻占卜体系 - OldBird | https://oldbird.run/yijing/liuyaozanbutixi/ | 起卦装卦七步、旺衰、世用、动变模型 |
| 六爻装卦纳卦 - 三六风水网 | https://www.36fengshui.com/ly/lyzg.asp | 装地支、装世应、装六亲、装六神的流程参考 |
| 六爻讲义：京房纳甲 - 知乎专栏 | https://zhuanlan.zhihu.com/p/709241395 | 纳支口诀和八卦纳支记忆 |
| bopo/najia - 纳甲六爻排盘源码 | https://github.com/bopo/najia | 开源排盘库，用于对照卦码、纳甲表、世应、伏神和测试颗粒度 |
| 六爻排盘教程 - Cosmic Tao | https://www.cosmictao.com/zh/library/liuyao-tutorial | 三钱法、八宫、六亲、六神、世应和伏神流程说明 |
| Liuyao Najia World & Response Guide - FateMaster | https://www.fatemaster.ai/guides/liuyao-shiying | 八宫世应定位表，用于校验游魂、归魂和世应位置 |

## C 类：视频与讨论材料

| 标题 | 链接 | 用途 |
|---|---|---|
| B站六爻纳甲入门到实战全套课程 | https://www.bilibili.com/video/BV1pL1KBiEKj/ | 课程目录显示八卦、地支、起卦纳甲、世应、飞伏、专题占法等学习路径 |
| B站小白六爻课程 | https://www.bilibili.com/video/BV1Xw411M7UV/ | 课程目录显示阴阳五行、天干地支、六亲用神、六神、起卦、纳甲、世应、旬空月破等顺序 |
| Reddit EasternOccult 六亲飞宫讨论 | https://www.reddit.com/r/EasternOccult/comments/1iv5c18/ | 高阶民间技法讨论，只作经验观察，不作为基础规则 |

## 下一步采集计划

- 对《卜筮正宗》建立逐章主题索引。第一版索引见 [古籍阅读索引](06-classics-reading-index.md) 和 `data/classics_index.json`。
- 对《增删卜易》建立卦例索引：题目、用神、动变、结果、争议点。
- 对《黄金策》建立分类断法索引。第一版专题映射见 [古籍阅读索引](06-classics-reading-index.md)。
- 对紫微斗数建立星曜、宫位、四化、大限流年来源索引。
- 对奇门遁甲建立九宫、八门、九星、八神、盘式差异来源索引。
- 对大六壬/小六壬分别建立四课三传、课体和小六壬六宫来源索引。
- 搜集至少 100 个有反馈的现代案例，按专题归档。
- 建立「规则来源」字段：每条规则都能指向古籍、现代解释或案例统计。第一版规则卡见 [规则卡索引](07-rule-cards.md) 和 `data/rules.json`。

## 已核验摘录说明

2026-06-20 使用 Agent Reach 可用后端核验：

- Jina Reader 可读取《卜筮正宗》CText 页面，目录含凡例、启蒙节要、纳甲装卦歌、安世应诀、十八论、十八问答等。
- Jina Reader 可读取天机要纳甲装卦教程，确认其把装卦拆为定卦宫、纳地支、配六亲、安六神、定世应并查伏神。
- Jina Reader 可读取 OldBird 六爻体系页，确认其把知识拆为基础符号、起卦装卦、能量模型、实战解盘、高阶扩展。
- B站搜索可返回六爻用神、原神忌神、纳甲装卦、世应等课程线索；因终端编码限制，标题以源站链接和 bvid 为准。

2026-06-21 使用 Agent Reach 可用后端和 Node fetch 追加核验：

- GitHub raw 可读取 `bopo/najia` README、`const.py`、`utils.py` 和测试文件，确认卦码自下而上、纳甲表、世应、卦宫、六亲、伏神字段。
- Jina Reader 可读取 Cosmic Tao 六爻教程，确认三钱法 6/7/8/9、八宫、六亲、世应、六神和伏神流程。
- Jina Reader 可读取 FateMaster 世应表，确认八纯、一至五世、游魂、归魂的世应位置。

## 采集边界记录

2026-06-20 至 2026-06-21 的采集边界：

- 公开网页、古籍页面、B站课程目录和 GitHub 公开源码已进入本版来源池。
- 社媒、论坛、播客和需要登录态的平台暂不作为规则来源，只作为后续线索池。
- 任何 C 类材料都需要经过古籍、现代教程或案例反馈交叉校验，才能影响规则卡。

下一轮扩展到紫微斗数、奇门遁甲、大六壬/小六壬时，应先建立独立来源索引，再进入术语、盘式和案例层。
