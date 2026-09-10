# PEVC Research Copilot

一套面向真实一级市场工作的开源 AI 投研工作流：以六个可组合 Codex Skills 覆盖读 BP、项目初筛、产业链研究、公司尽调与 IC Memo，并始终保留来源、口径、反向证据和待验证事项。

## 这套系统解决什么问题

它不是把所有 PE/VC 方法塞进一个超长提示词，而是按当前投资决策路由到最合适的专业 Skill：

```text
收到项目材料
  → BP 事实卡：先把材料读清楚
  → 项目初筛：决定是否值得继续投入时间
  → 产业链地图：理解上下游、利润池、技术路线和主要公司
  → 公司尽调：验证客户、订单、技术、财务质量与红旗
  → IC Memo：形成阶段适配、可追溯的投资决策材料
```

## 六个 Skill

| Skill | 用途 | 不负责什么 |
|---|---|---|
| `pevc-research-router` | 判断当前任务、选择最短可靠流程、维护交接 | 不替代专业 Skill 执行全部分析 |
| `pevc-bp-fact-card` | 提取 BP/CIM/teaser 的事实、口径、冲突与缺口 | 不做基金匹配或投资建议 |
| `pevc-deal-screening` | 用明确的基金标准做初筛并设计最低成本验证 | 不替代完整尽调或最终 IC |
| `pevc-industry-chain-mapper` | 生成真实上下游产业链 JSON 与交互 HTML 地图 | 不把估值、风险、投资建议画成产业链节点 |
| `pevc-company-diligence` | 验证客户、产品、技术、竞争、财务质量和交易风险 | 不替代法律、税务、审计或技术专家意见 |
| `pevc-ic-memo` | 输出筛选、预审、终审或更新版 IC Memo | 不编造交易条款、收益或尽调结论 |

## 与 N.E.I. 的关系

本项目借鉴了 [N.E.I. PEVC Skill Library](https://nei-pevc.com/) 的任务地图、Skill/Workflow 分层、研究纪律和连接器路由思路，但不是 N.E.I. 内容镜像。

- N.E.I. 更像在线方法库和 MCP 推荐层；
- 本项目定位为本地执行、证据交接、产业链交互交付和自动质检层；
- 不包含 N.E.I. Token、私有内容或用户收藏；
- N.E.I. 可作为可选方法来源，真实项目材料仍应留在可信本地环境。

## 安装

在仓库目录运行：

```bash
python3 scripts/install_skills.py
```

开发时希望仓库修改立即生效，可以使用链接模式：

```bash
python3 scripts/install_skills.py --link
```

也可以只复制需要的 `skills/<skill-name>` 到 `${CODEX_HOME:-$HOME/.codex}/skills/`。安装后刷新 Codex 的 Skill 发现。

## 最快使用方式

不确定该用哪个 Skill：

```text
Use $pevc-research-router to inspect the available materials and run the smallest reliable workflow for the current investment gate.
```

直接指定任务：

```text
Use $pevc-bp-fact-card to read these materials and produce a source-traceable fact card without an investment recommendation.

Use $pevc-deal-screening to compare the fact card with our fund criteria and decide whether to advance, hold, or decline.

Use $pevc-industry-chain-mapper to map the DPU value chain and generate the structured JSON plus interactive HTML.

Use $pevc-company-diligence to verify the decisive customer, revenue, technology, and cash-conversion claims.

Use $pevc-ic-memo to prepare a preliminary IC memo and keep unresolved assumptions visible.
```

完整中文教程见 [docs/usage-guide.zh-CN.md](docs/usage-guide.zh-CN.md)。工作流和质量门见 [docs/workflow.md](docs/workflow.md)。

## 项目证据包

多阶段项目使用三个结构化文件：

| 文件 | 作用 |
|---|---|
| `project-manifest.json` | 项目范围、阶段、决策、材料和保密级别 |
| `evidence-bundle.json` | 来源、事实、主张、反向证据、冲突和未决事项 |
| `decision-record.json` | IC 建议、交易条款、收益情景、风险和条件 |

验证示例：

```bash
python3 scripts/validate_project_bundle.py examples/synthetic-project --require-decision
```

验证器会检查跨文件项目编号、来源引用、事实状态、计算公式、投前/投后估值、EV/股权价值和 MOIC/IRR 等关键一致性。

## 质量验证

```bash
python3 scripts/validate_repo.py
```

该检查覆盖 Skill 结构、元数据、JSON、Python 脚本、合成项目证据包和失败案例测试。产业链地图还应单独运行其数据验证器、生成 HTML，并人工检查缩放、拖拽、搜索、节点弹窗、连接线和窄屏显示。

## 仓库结构

```text
skills/      六个可安装 Skill
skills/pevc-research-router/references/schemas/  项目清单、证据包和决策记录的数据契约
scripts/     安装、项目验证和仓库验证工具
examples/    不包含真实交易信息的合成示例
tests/       关键失败条件测试
evals/       面向真实 Agent 行为的正向与反向评测案例
docs/        使用教程、流程、来源与发布说明
```

## 保密和专业边界

不要把数据室文件、未公开 BP、客户名单、访谈记录、财务模型、IC 材料、LP 信息、Token、私有链接或含敏感信息的生成结果提交到本仓库。所有输出都依赖底层证据的质量、授权和时效，不构成法律、税务、审计、估值或受监管投资意见。

当前版本：`v1.0.0`。
