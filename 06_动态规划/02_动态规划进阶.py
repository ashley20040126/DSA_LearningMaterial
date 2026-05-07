# ============================================================
# 数据结构与算法 - 第十二章：动态规划（进阶）
# ============================================================
# 区间 DP、树形 DP、状态压缩 DP、数位 DP 等高级 DP 技巧。
# 以及经典的股票买卖、状态机 DP 等。
# ============================================================

from typing import List
from functools import lru_cache


# ------------------------------------------------------------
# 1. 区间 DP（在区间上做决策）
# ------------------------------------------------------------

def matrix_chain_multiplication(dims: List[int]) -> int:
    """
    【题型】矩阵链乘法（最少乘法次数）
    dims[i]*dims[i+1] 表示第 i 个矩阵的维度。
    dp[i][j] = 计算矩阵 i..j 乘积的最少乘法次数
    转移：dp[i][j] = min(dp[i][k] + dp[k+1][j] + dims[i]*dims[k+1]*dims[j+1])
    区间 DP 通用模板：枚举区间长度 l，枚举左端点 i，右端点 j=i+l-1，枚举分割点 k。
    """
    n = len(dims) - 1  # 矩阵数量
    dp = [[0] * n for _ in range(n)]

    # l 为区间长度（从2开始）
    for l in range(2, n + 1):
        for i in range(n - l + 1):
            j = i + l - 1
            dp[i][j] = float('inf')
            for k in range(i, j):
                cost = dp[i][k] + dp[k + 1][j] + dims[i] * dims[k + 1] * dims[j + 1]
                dp[i][j] = min(dp[i][j], cost)

    return dp[0][n - 1]


def burst_balloons(nums: List[int]) -> int:
    """
    【题型】戳气球（经典区间 DP）
    【思路】逆向思维：考虑"最后一个戳破的气球"，而不是"第一个"。
           dp[i][j] = 在 i..j 范围内（不含边界）能获得的最大硬币数。
           设 k 是这段范围内最后一个被戳破的气球：
           dp[i][j] = max(dp[i][k] + dp[k][j] + nums[i]*nums[k]*nums[j])
    """
    # 在两端添加哑气球（值为1），简化边界处理
    nums = [1] + nums + [1]
    n = len(nums)
    dp = [[0] * n for _ in range(n)]

    # 区间长度从2开始（至少包含一个气球：开区间 (i, j)）
    for l in range(2, n):
        for i in range(n - l):
            j = i + l
            for k in range(i + 1, j):  # k 是最后一个被戳的
                dp[i][j] = max(dp[i][j],
                               dp[i][k] + dp[k][j] + nums[i] * nums[k] * nums[j])

    return dp[0][n - 1]


def stone_game_minimum_cost(stones: List[int]) -> int:
    """
    【题型】石子合并（最小费用）
    相邻两堆石子合并，费用为两堆之和，求合并所有石子的最小费用。
    dp[i][j] = 合并 stones[i..j] 的最小费用
    转移：dp[i][j] = min(dp[i][k] + dp[k+1][j]) + sum(stones[i..j])
    """
    n = len(stones)
    # 前缀和快速求区间和
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + stones[i]

    dp = [[0] * n for _ in range(n)]

    for l in range(2, n + 1):
        for i in range(n - l + 1):
            j = i + l - 1
            dp[i][j] = float('inf')
            interval_sum = prefix[j + 1] - prefix[i]
            for k in range(i, j):
                dp[i][j] = min(dp[i][j], dp[i][k] + dp[k + 1][j] + interval_sum)

    return dp[0][n - 1]


def palindrome_partitioning_min(s: str) -> int:
    """
    【题型】最长回文子序列
    dp[i][j] = s[i..j] 的最长回文子序列长度
    转移：
      s[i]==s[j]：dp[i][j] = dp[i+1][j-1] + 2
      s[i]!=s[j]：dp[i][j] = max(dp[i+1][j], dp[i][j-1])
    """
    n = len(s)
    dp = [[0] * n for _ in range(n)]
    for i in range(n):
        dp[i][i] = 1

    for l in range(2, n + 1):
        for i in range(n - l + 1):
            j = i + l - 1
            if s[i] == s[j]:
                dp[i][j] = (dp[i + 1][j - 1] if l > 2 else 0) + 2
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])

    return dp[0][n - 1]


# ------------------------------------------------------------
# 2. 股票买卖系列（状态机 DP）
# ------------------------------------------------------------

def stock_max_profit_1(prices: List[int]) -> int:
    """
    【题型】股票买卖 I（只能交易一次）
    只需记录到目前为止的最低价格，当前价格 - 最低价格即为利润。
    """
    min_price = float('inf')
    max_profit = 0
    for price in prices:
        min_price = min(min_price, price)
        max_profit = max(max_profit, price - min_price)
    return max_profit


def stock_max_profit_2(prices: List[int]) -> int:
    """
    【题型】股票买卖 II（可交易无限次，但同时只能持有一股）
    【思路】贪心：只要明天比今天贵，今天就买入明天卖出（累积所有正差值）。
    """
    return sum(max(prices[i] - prices[i - 1], 0) for i in range(1, len(prices)))


def stock_max_profit_3(prices: List[int]) -> int:
    """
    【题型】股票买卖 III（最多交易两次）
    状态：buy1, profit1, buy2, profit2
    - buy1：第一次买入后的最大收益（负数表示花费）
    - profit1：第一次卖出后的最大收益
    - buy2：第二次买入后的最大收益
    - profit2：第二次卖出后的最大收益
    """
    buy1 = buy2 = float('-inf')
    profit1 = profit2 = 0

    for price in prices:
        # 状态转移：按"依赖关系"从后往前更新，避免同一天交易
        profit2 = max(profit2, buy2 + price)   # 第二次卖出
        buy2 = max(buy2, profit1 - price)       # 第二次买入（花费在第一次卖出利润基础上）
        profit1 = max(profit1, buy1 + price)    # 第一次卖出
        buy1 = max(buy1, -price)               # 第一次买入

    return profit2


def stock_max_profit_k(k: int, prices: List[int]) -> int:
    """
    【题型】股票买卖 IV（最多交易 k 次）
    通用 DP：dp[i][j][0/1] = 第 i 天，已完成 j 次交易，不/持有股票时的最大利润。
    空间优化为 O(k)。
    """
    n = len(prices)
    if not prices or k == 0:
        return 0

    # 若 k >= n//2，等价于无限次交易
    if k >= n // 2:
        return stock_max_profit_2(prices)

    # buy[j]：已完成 j 次交易且持有股票时的最大利润
    # sell[j]：已完成 j 次交易且不持有股票时的最大利润
    buy = [float('-inf')] * (k + 1)
    sell = [0] * (k + 1)

    for price in prices:
        for j in range(k, 0, -1):
            sell[j] = max(sell[j], buy[j] + price)
            buy[j] = max(buy[j], sell[j - 1] - price)

    return sell[k]


def stock_with_cooldown(prices: List[int]) -> int:
    """
    【题型】含冷冻期的股票买卖（卖出后需冷冻1天）
    三个状态：
    - hold：持有股票
    - sold：刚卖出（明天冷冻）
    - rest：冷冻/空仓
    """
    hold = float('-inf')
    sold = 0
    rest = 0

    for price in prices:
        prev_hold, prev_sold, prev_rest = hold, sold, rest
        hold = max(prev_hold, prev_rest - price)   # 维持持有 或 从 rest 状态买入
        sold = prev_hold + price                     # 从持有状态卖出
        rest = max(prev_rest, prev_sold)             # 维持 rest 或 从 sold 冷冻结束

    return max(sold, rest)


def stock_with_fee(prices: List[int], fee: int) -> int:
    """
    【题型】含手续费的股票买卖（每次卖出时扣手续费）
    """
    hold = float('-inf')  # 持有股票时的最大利润
    cash = 0              # 不持有股票时的最大利润

    for price in prices:
        hold = max(hold, cash - price)
        cash = max(cash, hold + price - fee)

    return cash


# ------------------------------------------------------------
# 3. 数字 DP
# ------------------------------------------------------------

def count_numbers_with_unique_digits(n: int) -> int:
    """
    【题型】统计各位数字都不同的数字个数（0 到 10^n - 1）
    dp[i] = i 位数字中各位不同的数字个数
    排列组合：第一位9种选择（1-9），后续位从剩余数字中选。
    """
    if n == 0:
        return 1
    result = 10  # n >= 1 时：0..9 共10个1位数
    unique_digits = 9
    available_digits = 9

    for i in range(2, min(n + 1, 11)):  # 最多10位（不重复数字只有10个）
        unique_digits *= available_digits
        result += unique_digits
        available_digits -= 1

    return result


# ------------------------------------------------------------
# 4. 状态压缩 DP（位运算表示子集状态）
# ------------------------------------------------------------

def traveling_salesman(dist: List[List[int]]) -> int:
    """
    旅行商问题（TSP）：从城市0出发，访问所有城市恰好一次后回到0，求最短路径。
    【思路】状态压缩 DP：用二进制位表示已访问的城市集合。
    dp[S][i] = 访问了城市集合 S，当前在城市 i 时的最短路径长度。
    【复杂度】时间 O(2^n * n²)，空间 O(2^n * n)
    适用于 n ≤ 20
    """
    n = len(dist)
    INF = float('inf')
    # dp[S][i]：已访问集合为 S，停在城市 i 时的最短路径
    dp = [[INF] * n for _ in range(1 << n)]
    dp[1][0] = 0  # 只访问了城市0（集合为 ...0001），停在城市0，路径长度为0

    for S in range(1, 1 << n):
        for u in range(n):
            if dp[S][u] == INF:
                continue
            if not (S >> u & 1):
                continue  # u 不在集合 S 中，跳过
            for v in range(n):
                if S >> v & 1:
                    continue  # v 已访问
                new_S = S | (1 << v)
                dp[new_S][v] = min(dp[new_S][v], dp[S][u] + dist[u][v])

    # 返回访问所有城市后回到城市0的最短路径
    full = (1 << n) - 1
    return min(dp[full][i] + dist[i][0] for i in range(1, n))


def count_shortest_paths(n: int, relation: List[List[int]], k: int) -> int:
    """
    【题型】恰好 k 步的方案数（状态压缩/矩阵快速幂的 DP 版本）
    dp[step][i] = 经过 step 步后在城市 i 的方案数
    """
    dp = [0] * n
    dp[0] = 1  # 从城市0出发

    for _ in range(k):
        new_dp = [0] * n
        for src, dst in relation:
            new_dp[dst] += dp[src]
        dp = new_dp

    return dp[n - 1]


# ------------------------------------------------------------
# 5. 树形 DP
# ------------------------------------------------------------

def rob_tree(root) -> int:
    """
    【题型】打家劫舍 III（树形 DP）
    每个节点要么被选（不能选相邻节点），要么不被选。
    对每个节点返回 (不选自己的最大值, 选自己的最大值) 元组。
    """
    def dfs(node):
        if not node:
            return 0, 0
        left_skip, left_rob = dfs(node.left)
        right_skip, right_rob = dfs(node.right)
        # 不选当前节点：子节点可选可不选，取较大值
        skip = max(left_skip, left_rob) + max(right_skip, right_rob)
        # 选当前节点：子节点只能跳过
        rob = node.val + left_skip + right_skip
        return skip, rob

    skip, rob = dfs(root)
    return max(skip, rob)


# ------------------------------------------------------------
# 6. 记忆化搜索（自顶向下 DP，适合复杂状态）
# ------------------------------------------------------------

def word_break(s: str, word_dict: List[str]) -> bool:
    """
    【题型】单词拆分（s 能否被 word_dict 中的单词拼成）
    dp[i] = s[0..i-1] 能否被完整拆分
    转移：dp[i] = True 若存在 j < i 使 dp[j]=True 且 s[j..i-1] 在字典中
    """
    word_set = set(word_dict)
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True

    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break

    return dp[n]


@lru_cache(maxsize=None)
def catalan_number(n: int) -> int:
    """
    卡特兰数（不同的二叉搜索树的数量）
    C(0) = 1, C(n) = sum(C(i) * C(n-1-i) for i in 0..n-1)
    用 @lru_cache 实现自动记忆化（Python 内置）。
    """
    if n <= 1:
        return 1
    return sum(catalan_number(i) * catalan_number(n - 1 - i) for i in range(n))


def num_distinct_subsequences(s: str, t: str) -> int:
    """
    【题型】不同的子序列（s 中 t 的子序列个数）
    dp[i][j] = s[0..i-1] 中含 t[0..j-1] 的子序列数
    转移：
      s[i-1] != t[j-1]：dp[i][j] = dp[i-1][j]
      s[i-1] == t[j-1]：dp[i][j] = dp[i-1][j] + dp[i-1][j-1]
    """
    m, n = len(s), len(t)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = 1  # 空字符串 t 只有一种匹配

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            dp[i][j] = dp[i - 1][j]  # 不使用 s[i-1]
            if s[i - 1] == t[j - 1]:
                dp[i][j] += dp[i - 1][j - 1]  # 使用 s[i-1] 匹配 t[j-1]

    return dp[m][n]


# ------------------------------------------------------------
# 主程序演示
# ------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 50)
    print("1. 区间 DP")
    print(f"  矩阵链乘法 [40,20,30,10,30]: {matrix_chain_multiplication([40,20,30,10,30])}")
    print(f"  戳气球 [3,1,5,8]: {burst_balloons([3,1,5,8])}")
    print(f"  最长回文子序列 'bbbab': {palindrome_partitioning_min('bbbab')}")

    print("\n2. 股票系列")
    prices = [3, 3, 5, 0, 0, 3, 1, 4]
    print(f"  价格: {prices}")
    print(f"  买卖一次: {stock_max_profit_1(prices)}")
    print(f"  买卖多次: {stock_max_profit_2(prices)}")
    print(f"  买卖两次: {stock_max_profit_3(prices)}")
    print(f"  含冷冻期: {stock_with_cooldown(prices)}")
    print(f"  手续费2: {stock_with_fee(prices, 2)}")

    print("\n3. 单词拆分")
    print(f"  'leetcode' in ['leet','code']: {word_break('leetcode',['leet','code'])}")
    print(f"  'applepenapple' in ['apple','pen']: {word_break('applepenapple',['apple','pen'])}")

    print("\n4. 卡特兰数（前6个）")
    print(f"  {[catalan_number(i) for i in range(7)]}")

    print("\n5. 不同子序列")
    print(f"  'rabbbit' 中 'rabbit' 的子序列数: {num_distinct_subsequences('rabbbit','rabbit')}")

    print("\n6. TSP 旅行商")
    dist = [[0,10,15,20],[10,0,35,25],[15,35,0,30],[20,25,30,0]]
    print(f"  4城市最短路径: {traveling_salesman(dist)}")
