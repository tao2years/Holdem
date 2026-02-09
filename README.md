# Holdem 德州扑克 GTO 知识库与 Solver 实现

本仓库用于系统记录德州扑克相关的 GTO 理论、基础与进阶知识，并逐步手动实现 Poker Solver 的核心算法与工程化代码。整体内容采用"总-分-总"的组织方式，强调逻辑结构与可检索性，兼顾学习与工程实践。

## 用户偏好记录

- 语言：中文
- 文档结构：内容描述倾向"总-分-总"，强调整体逻辑与分层表达

## 仓库目标（总）

- 建立完整、可迭代的德州扑克 GTO 知识体系
- 从理论到实践，逐步搭建可运行的 Poker Solver
- 支持自我学习、复盘与知识沉淀，形成可复用的资料库
- 提供从零构建不可被剥削的德扑体系的完整训练手册

## 内容规划（分）

### 1. 理论与基础

- ✅ 德州扑克规则与术语
- ✅ GTO 基本概念与博弈论基础
- ✅ 赔率、期望值、范围与平衡
- ✅ 底池计算、42 原则等实用工具

### 2. 进阶知识

- ✅ 位置策略、范围构建与对抗策略
- ✅ 翻牌前范围表（各位置详细范围）
- ✅ 翻后策略（翻牌、转牌、河牌）
- ✅ 下注尺度与频率策略
- ✅ 读牌与底池动态分析
- ✅ 实战案例与训练任务

### 3. Solver 实现（工程）

- ✅ 核心模型与抽象
- ✅ CFR 算法实现（Vanilla CFR）
- ✅ Kuhn Poker 最小实现
- ✅ 训练流程与评估工具
- 🔄 算法变体（CFR+、MCCFR，计划中）
- 🔄 Leduc Poker 实现（计划中）
- 🔄 德州抽象（计划中）

### 4. 实验与验证

- ✅ Kuhn Poker 基础验证
- ✅ 实验记录模板
- 🔄 算法对比实验（计划中）
- 🔄 性能优化实验（计划中）

## 目录结构（分）

```
Holdem/
├─ docs/                  # 文档入口与知识体系
│  ├─ 00_overview/         # 总览与路线图
│  │  ├─ index.md          # 总览入口
│  │  ├─ gto_handbook.md   # GTO 训练手册总览
│  │  └─ roadmap.md        # 项目路线图
│  ├─ 01_basics/           # 基础知识
│  │  ├─ index.md          # 基础模块入口
│  │  ├─ terminology.md   # 术语与规则
│  │  ├─ pot_math.md       # 底池计算
│  │  ├─ odds_ev.md        # 赔率与期望值
│  │  └─ ranges_tables.md  # 范围表与训练工具
│  ├─ 02_gto_theory/       # GTO 理论
│  │  ├─ index.md          # 理论模块入口
│  │  ├─ core_concepts.md  # GTO 核心概念
│  │  ├─ range_frequency.md # 范围与频率
│  │  ├─ rule_42.md        # 42 原则
│  │  └─ gto_training_manual.md # GTO 训练手册
│  ├─ 03_advanced/         # 进阶策略
│  │  ├─ index.md          # 进阶模块入口
│  │  ├─ preflop_ranges.md # 翻牌前范围
│  │  ├─ postflop_strategy.md # 翻后策略
│  │  ├─ bet_sizing.md     # 下注尺度
│  │  ├─ hand_reading_pot_dynamics.md # 读牌与底池动态
│  │  ├─ case_studies.md   # 实战案例
│  │  ├─ strategy_models.md # 策略模型
│  │  └─ training_checklists.md # 训练清单
│  ├─ 04_solver/           # Solver 设计与实现说明
│  │  ├─ index.md          # Solver 模块入口
│  │  ├─ architecture.md   # 架构概述
│  │  ├─ cfr_intro.md      # CFR 算法详解
│  │  └─ kuhn_example.md   # Kuhn 示例
│  ├─ 05_experiments/      # 实验记录与验证
│  │  ├─ index.md          # 实验模块入口
│  │  ├─ experiment_template.md # 实验模板
│  │  └─ kuhn_baseline.md  # Kuhn 基础验证
│  └─ 99_notes/            # 随手笔记与碎片化想法
│     └─ notes.md          # 碎片笔记
├─ solver/                # Solver 源码
│  ├─ core/                # 核心算法与数据结构
│  │  ├─ cfr.py            # CFR 算法实现
│  │  └─ README.md         # 核心模块说明
│  ├─ game/                # 牌型/规则/动作定义
│  │  ├─ kuhn.py           # Kuhn Poker 实现
│  │  └─ README.md         # 游戏模块说明
│  ├─ tree/                # 状态树/行动树（待实现）
│  ├─ training/            # 训练与迭代逻辑
│  │  ├─ train_kuhn.py     # Kuhn 训练脚本
│  │  └─ README.md         # 训练模块说明
│  ├─ eval/                # 评估与对比
│  │  ├─ report.py         # 评估报告生成
│  │  └─ README.md         # 评估模块说明
│  ├─ cli/                 # 命令行工具
│  │  ├─ run_kuhn.py       # Kuhn 训练入口
│  │  └─ README.md         # CLI 模块说明
│  └─ README.md            # Solver 总览
├─ data/                  # 小型样例、配置、训练结果
│  └─ README.md            # 数据目录说明
└─ README.md
```

## 快速开始（分）

### 阅读路线

**📖 完整阅读路线图**：请先查看 `ROADMAP.md`，选择适合你的学习路径！

`ROADMAP.md` 提供三条主要学习路径：
- **GTO 理论学习路径**：系统掌握 GTO 理论（3-6 个月）
- **实战应用路径**：快速提升实战水平（1-2 个月）
- **Solver 开发路径**：深入理解算法原理（2-4 个月）

### 快速入门（1 天）

1. **新手入门**：从 `docs/00_overview/gto_handbook.md` 开始
2. **选择路径**：查看 `ROADMAP.md` 选择适合的学习路径
3. **开始学习**：按照路线图逐步推进

### 运行 Solver

#### 环境要求

- Python 3.8+
- 无额外依赖（当前实现使用标准库）

#### 运行 Kuhn Poker 训练

```bash
# 训练 50000 轮
python -m solver.cli.run_kuhn --iterations 50000

# 指定输出文件
python -m solver.cli.run_kuhn --iterations 50000 --output data/kuhn_strategy.json

# 显示详细日志
python -m solver.cli.run_kuhn --iterations 50000 --verbose
```

#### 查看结果

训练完成后，策略文件将保存在 `data/` 目录下，可以使用评估工具分析策略质量。

## 文档写作规范（分）

- **结构**：总览 -> 分项 -> 结论（"总-分-总"）
- **固定模块**：每篇文档包含"本节目的"和"总结"
- **逻辑清晰**：强调整体逻辑与分层表达
- **实用导向**：提供可操作的训练方法与案例

## 项目状态（分）

### 已完成

- ✅ 完整的文档框架与目录结构
- ✅ 基础理论文档（术语、计算、GTO 核心概念）
- ✅ 进阶策略文档（翻牌前、翻后、下注尺度、案例）
- ✅ GTO 训练手册（系统化的训练框架）
- ✅ Kuhn Poker Solver 实现
- ✅ CFR 算法实现
- ✅ 训练与评估工具

### 进行中

- 🔄 更多实战案例补充
- 🔄 训练工具完善
- 🔄 文档细节优化

### 计划中

- 📋 Leduc Poker 实现
- 📋 算法变体（CFR+、MCCFR）
- 📋 性能优化（向量化、并行化）
- 📋 策略可视化工具
- 📋 德州抽象实现

## 后续展开路线（分）

1. ✅ 完善 `docs/00_overview/` 的总览与路线图
2. ✅ 建立 `docs/01_basics/` 的术语与规则体系
3. ✅ 将 GTO 理论按"概念 -> 示例 -> 结论"拆分整理
4. ✅ 在 `solver/` 中实现最小可运行版本（Kuhn Poker + CFR）
5. 🔄 逐步引入多街（Leduc Poker）、抽象、性能优化与可视化

详细路线图请参考 `docs/00_overview/roadmap.md`。

## 贡献指南（分）

### 文档贡献

- 遵循"总-分-总"的文档结构
- 使用中文编写
- 提供可操作的训练方法与案例

### 代码贡献

- 遵循现有代码风格
- 提供清晰的注释
- 包含必要的测试

### 反馈与建议

欢迎提出改进建议、报告问题或分享学习心得。

## 参考资料（分）

### 理论资源

- "An Introduction to Counterfactual Regret Minimization" (2019)
- "Libratus: The superhuman AI for no-limit poker" (2017)
- "Solving Imperfect-Information Games" (2019)

### 工具资源

- PioSolver：商业 Solver 工具
- GTO+：GTO 分析软件
- PokerSnowie：AI 训练工具

## 总结（总）

本仓库以"知识体系 + Solver 实现"双线推进，形成可持续迭代的德州扑克 GTO 学习与工程实践平台。通过系统化的文档、可运行的代码、实用的训练工具，帮助玩家从零开始，系统掌握不可被剥削的 GTO 策略。

**当前状态**：基础框架已建立，核心文档已完善，最小 Solver 已实现。后续将逐步扩展功能，完善训练工具，最终构建完整的 GTO 训练生态系统。

---

**开始学习**：从 `docs/00_overview/gto_handbook.md` 开始你的 GTO 训练之旅！
