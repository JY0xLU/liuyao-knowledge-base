# GitHub 项目化与版本迭代

本项目可以上传到 GitHub 作为专业知识库与排盘工具持续迭代。上传前必须确认仓库名、可见性和 license。

## 1. 建议仓库信息

| 字段 | 建议 |
|---|---|
| 仓库名 | `liuyao-knowledge-base` |
| 描述 | 本地优先的传统术数学习、检索、排盘和验证评分工作台 |
| 可见性 | public |
| License | 已补 `LICENSE`：代码 MIT；原创整理内容 CC BY-NC-SA 4.0；第三方来源保留原授权 |
| 默认分支 | `main` |

## 2. 版本线

| 版本 | 范围 |
|---|---|
| v0.1 | 本地知识库、搜索、来源、规则卡、Netlify 静态站 |
| v0.2 | 纳甲排盘：卦宫、纳甲、六亲、六神、世应、伏神 |
| v0.3 | 旬空、月建、日辰基础状态、验证评分模型、GitHub Actions 检查 |
| v0.4 | 多体系入口、体系路线图、真实事件回测校准、GitHub Actions 检查 |
| v1.0 | 稳定文档、案例库、排盘回归集和公开发布说明 |

## 3. 上传前检查

必须通过：

```powershell
python .\scripts\check.py
```

还要人工确认：

- `README.md` 不含本地绝对路径。
- `web/assets/kb-data.json` 不含个人隐私。
- 本地缓存、部署缓存和 `node_modules/` 不会被提交。
- 来源说明不会把 C 类材料误写成 A 类规则。
- Netlify 站点 ID 和 deploy ID 是否适合公开展示。

## 4. 建议 GitHub Actions

已添加 `.github/workflows/check.yml`：

```yaml
name: check
on: [push, pull_request]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - uses: actions/setup-node@v4
        with:
          node-version: "22"
      - run: python scripts/check.py
```

## 5. 发布边界

公开项目说明应强调：

- 这是传统术数文化研究和工具项目。
- 排盘、规则和评分是可复盘研究，不是现实决策建议。
- 医疗、法律、金融、考试、婚恋等问题不能依赖本项目作唯一依据。

## 6. 当前上传状态

2026-06-21 已完成：

- 本地仓库已初始化，默认分支为 `main`。
- GitHub 远程仓库已创建并推送：`https://github.com/JY0xLU/liuyao-knowledge-base`。
- 仓库可见性为 public。
- GitHub Actions `check` 工作流已通过一次远程运行。
- 项目已配置 GitHub Actions `check`，每次推送后应确认远程检查通过。

下一步：

1. 建立 release 标签和 release notes。
2. 每轮新增规则、样本或排盘能力后，先跑 `python .\scripts\check.py`，再提交和推送。
3. 准确度验证只在事前锁定样本达到统计量后发布命中率结论。
