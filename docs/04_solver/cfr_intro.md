# CFR 算法详解

本章以"总-分-总"结构深入说明 CFR（Counterfactual Regret Minimization）的核心原理、实现细节与优化方向。

## 本节目的（总）

- 深入理解 CFR 算法的数学原理
- 掌握 CFR 的实现细节与关键技巧
- 了解 CFR 的变体与优化方向

## 核心问题（分）

### 问题背景

在信息不完美博弈中，玩家无法观察到对手的私有信息（如手牌），只能基于公共信息（如历史行动）做出决策。如何找到纳什均衡策略？

### 传统方法的问题

- **枚举法**：状态空间巨大，无法枚举所有可能
- **线性规划**：约束条件过多，计算复杂度高
- **梯度下降**：不适用于离散行动空间

### CFR 的解决思路

通过**反事实后悔值最小化**，在自博弈中逐步逼近均衡策略：
- 不需要显式求解线性规划
- 通过迭代更新策略，自然收敛到均衡
- 适用于大规模信息不完美博弈

## 数学原理（分）

### 基本概念

#### 信息集合（Information Set）

信息集合是玩家无法区分的所有状态的集合。例如，在 Kuhn Poker 中：
- 玩家 1 拿到 J 且历史为 "p" 的状态属于同一信息集合
- 玩家 1 拿到 J 且历史为 "b" 的状态属于另一信息集合

#### 反事实值（Counterfactual Value）

反事实值是在假设玩家以概率 1 选择某个行动时，该信息集合的期望收益。

**公式**：
```
v_I(σ, a) = Σ_{z∈Z_I} π^σ_{-i}(z[I]) π^σ(z[I]a, z) u_i(z)
```

其中：
- `I`：信息集合
- `σ`：策略
- `a`：行动
- `z`：终局状态
- `π^σ_{-i}(z[I])`：对手到达信息集合 I 的概率
- `π^σ(z[I]a, z)`：从 I 选择 a 到达 z 的概率
- `u_i(z)`：玩家 i 在 z 的收益

#### 后悔值（Regret）

后悔值是"如果选择行动 a 而非当前策略，能获得多少额外收益"。

**公式**：
```
R^T_I(a) = Σ_{t=1}^T (v_I(σ^t, a) - v_I(σ^t))
```

其中：
- `R^T_I(a)`：T 轮后行动 a 的累积后悔值
- `v_I(σ^t, a)`：第 t 轮选择 a 的反事实值
- `v_I(σ^t)`：第 t 轮当前策略的反事实值

### CFR 算法流程

#### 1. 初始化

```python
# 为每个信息集合初始化后悔值
regret_sum[info_set][action] = 0.0
strategy_sum[info_set][action] = 0.0
```

#### 2. 训练循环（迭代 T 轮）

对每轮 t：
1. **遍历博弈树**：从根节点递归遍历所有可能的状态
2. **计算策略**：基于当前后悔值计算当前策略
3. **计算反事实值**：递归计算每个行动的反事实值
4. **更新后悔值**：根据反事实值更新后悔值

#### 3. 输出平均策略

```python
# 平均策略 = 累积策略 / 累积到达概率
average_strategy[info_set][action] = strategy_sum[info_set][action] / sum(strategy_sum[info_set].values())
```

### 关键公式

#### 策略更新（Regret Matching）

```python
# 将负后悔值截断为 0
positive_regrets = {a: max(0, regret_sum[a]) for a in actions}

# 归一化得到策略
normalizer = sum(positive_regrets.values())
if normalizer > 0:
    strategy[a] = positive_regrets[a] / normalizer
else:
    strategy[a] = 1.0 / len(actions)  # 均匀策略
```

#### 后悔值更新

```python
# 计算反事实后悔值
regret = counterfactual_value[action] - node_util

# 更新累积后悔值（乘以对手到达概率）
regret_sum[action] += opponent_reach_prob * regret
```

## 实现细节（分）

### 信息集合编码

**Kuhn Poker 示例**：
```python
def get_info_set_key(cards, history):
    """生成信息集合键"""
    player = len(history) % 2
    return f"{cards[player]}{history}"
```

**设计要点**：
- 相同信息集合使用相同键
- 键应包含所有可观察信息
- 键应唯一且可逆

### 递归遍历

```python
def cfr(cards, history, p0, p1):
    """CFR 递归遍历"""
    if is_terminal(history):
        return utility(history, cards)
    
    player = len(history) % 2
    info_set = get_info_set(cards, history)
    strategy = info_set.get_strategy(p0 if player == 0 else p1)
    
    util = {}
    node_util = 0.0
    
    for action in legal_actions(history):
        next_history = history + action
        if player == 0:
            util[action] = cfr(cards, next_history, p0 * strategy[action], p1)
        else:
            util[action] = cfr(cards, next_history, p0, p1 * strategy[action])
        node_util += strategy[action] * util[action]
    
    # 更新后悔值
    for action in legal_actions(history):
        regret = util[action] - node_util
        if player == 0:
            info_set.regret_sum[action] += p1 * regret
        else:
            info_set.regret_sum[action] += p0 * (-regret)
    
    return node_util
```

### 策略累积

```python
def get_strategy(self, realization_weight):
    """计算当前策略并累积"""
    strategy = self.compute_strategy_from_regrets()
    
    # 累积策略（用于计算平均策略）
    for action, prob in strategy.items():
        self.strategy_sum[action] += realization_weight * prob
    
    return strategy
```

## 算法变体（分）

### CFR+（Linear CFR）

**改进**：使用线性后悔值更新，而非累积后悔值。

**公式**：
```
R^T_I(a) = max(0, R^{T-1}_I(a) + r^T_I(a))
```

**优势**：
- 在某些博弈中收敛更快
- 后悔值不会无限增长

**实现**：
```python
# CFR+ 使用线性更新
regret_sum[action] = max(0, regret_sum[action] + immediate_regret)
```

### MCCFR（Monte Carlo CFR）

**改进**：通过采样减少计算量，适用于大规模博弈。

**方法**：
- **Outcome Sampling**：每次只采样一条路径
- **External Sampling**：每次采样所有玩家的外部信息
- **Chance Sampling**：采样所有机会节点

**优势**：
- 大幅减少计算量
- 适用于无法完全遍历的博弈

**实现**：
```python
def mccfr(cards, history, p0, p1, sampling_strategy):
    """MCCFR 采样遍历"""
    if is_terminal(history):
        return utility(history, cards)
    
    # 根据采样策略选择要遍历的行动
    actions_to_explore = sampling_strategy.select_actions(history)
    
    # 只遍历采样的行动
    for action in actions_to_explore:
        # ... 递归计算 ...
```

### Discounted CFR

**改进**：对早期轮次的后悔值进行折扣，加快收敛。

**公式**：
```
R^T_I(a) = Σ_{t=1}^T α^t * r^t_I(a)
```

其中 `α^t` 是折扣因子（通常 `α^t = t^α`，α > 0）。

## 性能优化（分）

### 向量化计算

使用 NumPy 向量化操作加速计算：

```python
import numpy as np

# 向量化后悔值更新
regrets = np.array([regret_sum[a] for a in actions])
positive_regrets = np.maximum(regrets, 0)
normalizer = np.sum(positive_regrets)
strategy = positive_regrets / normalizer if normalizer > 0 else np.ones(len(actions)) / len(actions)
```

### 并行化

**多线程**：并行遍历不同的发牌组合

```python
from concurrent.futures import ThreadPoolExecutor

def train_parallel(iterations, num_threads):
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        for _ in range(iterations):
            futures = []
            for cards in all_card_combinations():
                future = executor.submit(cfr, cards, "", 1.0, 1.0)
                futures.append(future)
            for future in futures:
                future.result()
```

**多进程**：适用于 CPU 密集型任务

```python
from multiprocessing import Pool

def train_multiprocess(iterations, num_processes):
    with Pool(processes=num_processes) as pool:
        for _ in range(iterations):
            results = pool.starmap(cfr, [(cards, "", 1.0, 1.0) for cards in all_card_combinations()])
```

### 内存优化

**状态压缩**：使用更紧凑的状态表示

```python
# 使用整数编码而非字符串
def encode_history(history):
    """将历史编码为整数"""
    encoding = {"": 0, "p": 1, "b": 2, "pp": 3, "pb": 4, "bf": 5, "bc": 6, "pbf": 7, "pbc": 8}
    return encoding.get(history, -1)
```

**延迟构建**：按需构建信息集合，而非预先构建

```python
# 只在需要时创建信息集合
if info_key not in self.nodes:
    self.nodes[info_key] = InfoSet(actions=actions)
```

## 收敛性分析（分）

### 理论保证

CFR 算法保证：
- **平均策略收敛**：平均策略在 T 轮后收敛到 ε-纳什均衡，其中 ε = O(1/√T)
- **后悔值界限**：累积后悔值的上界为 O(√T)

### 实际收敛表现

**Kuhn Poker 示例**：
- **前 1000 轮**：策略快速变化，后悔值大幅下降
- **1000-10000 轮**：策略逐步稳定，频率波动减小
- **10000+ 轮**：策略基本稳定，变化 < 1%

### 收敛判断

```python
def check_convergence(strategies_history, window=1000, threshold=0.01):
    """判断策略是否收敛"""
    if len(strategies_history) < window * 2:
        return False
    
    recent = strategies_history[-window:]
    previous = strategies_history[-window*2:-window]
    
    # 计算策略差异
    diff = compute_strategy_diff(recent, previous)
    return diff < threshold
```

## 常见问题（分）

### Q: 为什么使用平均策略而非当前策略？

**A**：平均策略的收敛性有理论保证，而当前策略可能波动较大。平均策略通过累积所有轮次的策略，平滑了波动，更接近均衡。

### Q: 后悔值会无限增长吗？

**A**：在 Vanilla CFR 中，后悔值会无限增长，但通过归一化策略更新，不会影响策略质量。CFR+ 通过截断负后悔值，可以限制后悔值的增长。

### Q: 如何选择训练轮次？

**A**：取决于博弈复杂度：
- **简单博弈**（如 Kuhn Poker）：10000-50000 轮
- **中等博弈**（如 Leduc Poker）：100000-500000 轮
- **复杂博弈**（如德州抽象）：百万级轮次

### Q: CFR 适用于所有博弈吗？

**A**：CFR 适用于信息不完美博弈，但要求：
- 博弈树可以完全遍历（或通过采样近似）
- 信息集合可以高效编码
- 状态空间不会导致内存爆炸

## 总结（总）

CFR 算法通过反事实后悔值最小化，在自博弈中逐步逼近纳什均衡策略。核心思想是：
- **后悔值驱动**：通过累积后悔值指导策略更新
- **平均策略收敛**：平均策略保证收敛到均衡
- **可扩展性**：通过变体（CFR+、MCCFR）适用于不同规模博弈

掌握 CFR 的原理与实现，是构建 GTO Solver 的基础。通过理解算法细节、优化性能与验证收敛性，可以逐步扩展到更复杂的博弈，最终实现德州扑克的 GTO 求解。
