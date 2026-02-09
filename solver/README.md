# Solver 说明

本目录用于实现德州扑克 Solver 的核心算法与工程化代码，内容遵循“总-分-总”结构。

## 本节目的

- 提供最小可运行示例
- 作为后续扩展的工程入口

## 当前实现

- `game/kuhn.py`：Kuhn Poker 简化博弈定义
- `core/cfr.py`：CFR 训练器（最小可用）
- `training/train_kuhn.py`：训练入口
- `cli/run_kuhn.py`：命令行运行脚本

## 运行方式

在仓库根目录执行：

```
python -m solver.cli.run_kuhn --iterations 50000
```

## 总结

当前仅提供最小可运行示例，用于验证算法与工程骨架，后续将扩展到多街与抽象策略。
# Solver 目录说明

该目录用于实现与验证 Solver 核心算法。当前提供 Kuhn Poker 的最小可运行示例，便于验证 CFR 训练流程。

## 快速运行

```bash
python -m solver.cli.run_kuhn --iterations 20000
```

## 说明

- `core/`：核心算法
- `game/`：游戏规则与状态
- `cli/`：命令行入口
