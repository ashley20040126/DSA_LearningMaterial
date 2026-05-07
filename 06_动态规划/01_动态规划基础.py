# ============================================================
# 数据结构与算法 - 第十一章：动态规划（基础）
# ============================================================
# 动态规划（DP）：将大问题分解为重叠子问题，保存子问题结果避免重复计算。
#
# 解题框架：
# 1. 定义状态：dp[i] 或 dp[i][j] 表示什么含义
# 2. 状态转移方程：dp[i] = f(dp[i-1], dp[i-2], ...)
# 3. 初始条件：最小子问题的答案
# 4. 计算顺序：确保计算 dp[i] 时，依赖的子问题已计算
# 5. 空间优化：很多 DP 只需保留最近几层
#
# 分类：线性DP、区间DP、背包DP、树形DP、状态压缩DP
# ============================================================

from typing import List
from functools import lru_cache


# ------------------------------------------------------------
# 1. 入门：斐波那契数列（DP 思想的引入）
# ------------------------------------------------------------

def fib_recursive(n: int) -> int:
    """朴素递归：时间 O(2^n)，大量重复计算"""
    if n <= 1:
        return n
    return fib_recursive(n - 1) + fib_recursive(n - 2)


def fib_memo(n: int) -> int:
    """记忆化递归（自顶向下）：用哈希表缓存结果，O(n)"""
    memo = {}

    def dp(n):
        if n <= 1:
            return n
        if n in memo:
            return memo[n]
        memo[n] = dp(n - 1) + dp(n - 2)
        return memo[n]

    return dp(n)


def fib_dp(n: int) -> int:
    """
    动态规划（自底向上）：从小到大填表，O(n) 时间，O(n) 空间。
    状态：dp[i] = 第 i 个斐波那契数
    转移：dp[i] = dp[i-1] + dp[i-2]
    """
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]


def fib_optimized(n: int) -> int:
    """空间优化：只保留前两个状态，O(1) 空间"""
    if n <= 1:
        return n
    prev2, prev1 = 0, 1
    for _ in range(2, n + 1):
        prev2, prev1 = prev1, prev2 + prev1
    return prev1


# ------------------------------------------------------------
# 2. 线性 DP
# ------------------------------------------------------------

def climbing_stairs(n: int) -> int:
    """
    【题型】爬楼梯（每次 1 或 2 步）
    dp[i] = 到达第 i 阶的方法数 = dp[i-1] + dp[i-2]
    """
    if n <= 2:
        return n
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b


def rob(nums: List[int]) -> int:
    """
    【题型】打家劫舍（相邻房屋不能同时抢）
    dp[i] = 偷前 i 个房屋的最大金额
    转移：dp[i] = max(dp[i-1], dp[i-2] + nums[i])
          （不偷 i 号 vs 偷 i 号 + i-2 号之前的最大值）
    """
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]
    prev2, prev1 = nums[0], max(nums[0], nums[1])
    for i in range(2, len(nums)):
        prev2, prev1 = prev1, max(prev1, prev2 + nums[i])
    return prev1


def rob_circle(nums: List[int]) -> int:
    """
    【题型】打家劫舍 II（环形，首尾不能同时抢）
    【思路】拆成两个线性问题：
           情况1：抢 nums[0..n-2]（不抢最后一个）
           情况2：抢 nums[1..n-1]（不抢第一个）
           取两者最大值。
    """
    def rob_linear(arr):
        if not arr:
            return 0
        if len(arr) == 1:
            return arr[0]
        prev2, prev1 = arr[0], max(arr[0], arr[1])
        for i in range(2, len(arr)):
            prev2, prev1 = prev1, max(prev1, prev2 + arr[i])
        return prev1

    if len(nums) == 1:
        return nums[0]
    return max(rob_linear(nums[:-1]), rob_linear(nums[1:]))


def max_subarray(nums: List[int]) -> int:
    """
    【题型】最大子数组和（Kadane 算法）
    dp[i] = 以 nums[i] 结尾的最大子数组和
    转移：dp[i] = max(nums[i], dp[i-1] + nums[i])
          （要么重新开始，要么扩展之前的子数组）
    """
    max_sum = nums[0]
    cur_sum = nums[0]
    for i in range(1, len(nums)):
        cur_sum = max(nums[i], cur_sum + nums[i])
        max_sum = max(max_sum, cur_sum)
    return max_sum


def max_subarray_with_index(nums: List[int]):
    """最大子数组和（同时返回起止下标）"""
    max_sum = cur_sum = nums[0]
    start = end = temp_start = 0
    for i in range(1, len(nums)):
        if cur_sum + nums[i] < nums[i]:
            cur_sum = nums[i]
            temp_start = i
        else:
            cur_sum += nums[i]
        if cur_sum > max_sum:
            max_sum = cur_sum
            start = temp_start
            end = i
    return max_sum, start, end


def length_of_lis(nums: List[int]) -> int:
    """
    【题型】最长递增子序列（LIS）
    dp[i] = 以 nums[i] 结尾的最长递增子序列长度
    转移：dp[i] = max(dp[j] + 1) for j < i if nums[j] < nums[i]
    【复杂度】O(n²)，可优化到 O(n log n)（见下方）
    """
    if not nums:
        return 0
    n = len(nums)
    dp = [1] * n  # 每个元素自身构成长度为1的子序列

    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)

    return max(dp)


def length_of_lis_nlogn(nums: List[int]) -> int:
    """
    LIS O(n log n) 解法（耐心排序 / 二分优化）。
    维护 tails 数组：tails[i] 是长度为 i+1 的递增子序列的最小末尾值。
    tails 始终有序，可用二分查找。
    """
    tails = []
    for num in nums:
        # 找 tails 中第一个 >= num 的位置（lower_bound）
        lo, hi = 0, len(tails)
        while lo < hi:
            mid = (lo + hi) // 2
            if tails[mid] < num:
                lo = mid + 1
            else:
                hi = mid
        if lo == len(tails):
            tails.append(num)   # 延长 LIS
        else:
            tails[lo] = num     # 替换（维护最小末尾值）
    return len(tails)


# ------------------------------------------------------------
# 3. 二维 DP（路径问题）
# ------------------------------------------------------------

def unique_paths(m: int, n: int) -> int:
    """
    【题型】不同路径（从左上到右下，只能向右或向下）
    dp[i][j] = 到达 (i,j) 的不同路径数
    转移：dp[i][j] = dp[i-1][j] + dp[i][j-1]
    """
    dp = [[1] * n for _ in range(m)]
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
    return dp[m - 1][n - 1]


def min_path_sum(grid: List[List[int]]) -> int:
    """
    【题型】最小路径和（从左上到右下，求路径上数字总和的最小值）
    dp[i][j] = 到达 (i,j) 的最小路径和
    """
    m, n = len(grid), len(grid[0])
    # 原地修改，省去额外空间
    for i in range(m):
        for j in range(n):
            if i == 0 and j == 0:
                continue
            elif i == 0:
                grid[i][j] += grid[i][j - 1]
            elif j == 0:
                grid[i][j] += grid[i - 1][j]
            else:
                grid[i][j] += min(grid[i - 1][j], grid[i][j - 1])
    return grid[m - 1][n - 1]


def triangle_min_path(triangle: List[List[int]]) -> int:
    """
    【题型】三角形最小路径和（从顶部到底部）
    dp[j] = 当前层第 j 个元素到底部的最小路径和
    从底部往上更新（滚动数组）。
    """
    dp = triangle[-1][:]  # 以最后一行初始化

    # 从倒数第二行开始向上
    for i in range(len(triangle) - 2, -1, -1):
        for j in range(len(triangle[i])):
            dp[j] = triangle[i][j] + min(dp[j], dp[j + 1])

    return dp[0]


# ------------------------------------------------------------
# 4. 字符串 DP
# ------------------------------------------------------------

def longest_common_subsequence(text1: str, text2: str) -> int:
    """
    【题型】最长公共子序列（LCS）
    dp[i][j] = text1[0..i-1] 和 text2[0..j-1] 的 LCS 长度
    转移：
      字符相等：dp[i][j] = dp[i-1][j-1] + 1
      字符不等：dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    """
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[m][n]


def edit_distance(word1: str, word2: str) -> int:
    """
    【题型】编辑距离（Levenshtein 距离）：将 word1 变为 word2 的最少操作数（增/删/替换）
    dp[i][j] = word1[0..i-1] 变为 word2[0..j-1] 的最少操作数
    转移：
      字符相等：dp[i][j] = dp[i-1][j-1]（无需操作）
      字符不等：dp[i][j] = 1 + min(
                    dp[i-1][j],   # 删除 word1[i-1]
                    dp[i][j-1],   # 插入 word2[j-1]
                    dp[i-1][j-1]  # 替换 word1[i-1]
                )
    """
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # 初始化：word1 的前 i 个字符变为空字符串需要 i 次删除
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

    return dp[m][n]


def is_palindrome_partition(s: str) -> int:
    """
    【题型】分割回文串 II（最少分割次数使每段都是回文）
    dp[i] = s[0..i] 的最少分割次数
    先用 is_pal[i][j] 预处理所有回文子串。
    """
    n = len(s)
    # 预处理：is_pal[i][j] = s[i..j] 是否是回文
    is_pal = [[False] * n for _ in range(n)]
    for right in range(n):
        for left in range(right + 1):
            if s[left] == s[right] and (right - left <= 2 or is_pal[left + 1][right - 1]):
                is_pal[left][right] = True

    dp = list(range(n))  # dp[i] = i+1（每个字符单独为一段）
    for i in range(1, n):
        if is_pal[0][i]:
            dp[i] = 0  # s[0..i] 整体是回文，无需分割
            continue
        for j in range(1, i + 1):
            if is_pal[j][i]:
                dp[i] = min(dp[i], dp[j - 1] + 1)

    return dp[n - 1]


# ------------------------------------------------------------
# 5. 背包问题
# ------------------------------------------------------------

def knapsack_01(weights: List[int], values: List[int], capacity: int) -> int:
    """
    【题型】0/1 背包（每件物品最多选一次）
    dp[j] = 容量为 j 时的最大价值
    状态转移：dp[j] = max(dp[j], dp[j-w] + v)
    【关键】逆序遍历容量，防止同一物品被重复选取。
    """
    dp = [0] * (capacity + 1)

    for w, v in zip(weights, values):
        # 逆序遍历：防止当前物品被重复使用
        for j in range(capacity, w - 1, -1):
            dp[j] = max(dp[j], dp[j - w] + v)

    return dp[capacity]


def knapsack_complete(weights: List[int], values: List[int], capacity: int) -> int:
    """
    【题型】完全背包（每件物品可选无限次）
    dp[j] = 容量为 j 时的最大价值
    【关键】正序遍历容量，允许同一物品被重复选取。
    """
    dp = [0] * (capacity + 1)

    for w, v in zip(weights, values):
        # 正序遍历：允许当前物品被重复使用
        for j in range(w, capacity + 1):
            dp[j] = max(dp[j], dp[j - w] + v)

    return dp[capacity]


def coin_change(coins: List[int], amount: int) -> int:
    """
    【题型】零钱兑换（凑出 amount 的最少硬币数，完全背包）
    dp[j] = 凑出金额 j 的最少硬币数
    转移：dp[j] = min(dp[j], dp[j-coin] + 1)
    """
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0

    for coin in coins:
        for j in range(coin, amount + 1):
            if dp[j - coin] != float('inf'):
                dp[j] = min(dp[j], dp[j - coin] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1


def coin_change_ways(coins: List[int], amount: int) -> int:
    """
    【题型】零钱兑换 II（凑出 amount 的组合数）
    dp[j] = 凑出金额 j 的方案数
    【注意】组合数（不考虑顺序）→ 外层遍历硬币，内层遍历金额
    """
    dp = [0] * (amount + 1)
    dp[0] = 1  # 凑出 0 有 1 种方法（不选任何硬币）

    for coin in coins:
        for j in range(coin, amount + 1):
            dp[j] += dp[j - coin]

    return dp[amount]


def partition_equal_subset_sum(nums: List[int]) -> bool:
    """
    【题型】分割等和子集（能否将数组分为两个和相等的子集）
    【转化】等价于 0/1 背包：能否从数组中选一些数使其和等于 total//2。
    dp[j] = 是否能从前面的数中选出和恰好为 j 的子集
    """
    total = sum(nums)
    if total % 2:
        return False
    target = total // 2

    dp = [False] * (target + 1)
    dp[0] = True

    for num in nums:
        # 逆序：0/1 背包
        for j in range(target, num - 1, -1):
            dp[j] = dp[j] or dp[j - num]

    return dp[target]


# ------------------------------------------------------------
# 主程序演示
# ------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 50)
    print("1. 斐波那契（对比各实现）")
    for n in [5, 10, 20]:
        print(f"  fib({n}) = {fib_dp(n)}")

    print("\n2. 线性 DP")
    print(f"  爬10阶楼梯: {climbing_stairs(10)}")
    print(f"  打家劫舍[2,7,9,3,1]: {rob([2,7,9,3,1])}")
    print(f"  打家劫舍II[2,3,2]: {rob_circle([2,3,2])}")
    print(f"  最大子数组[-2,1,-3,4,-1,2,1,-5,4]: {max_subarray([-2,1,-3,4,-1,2,1,-5,4])}")
    print(f"  LIS[10,9,2,5,3,7,101,18]: {length_of_lis([10,9,2,5,3,7,101,18])}")
    print(f"  LIS O(nlogn): {length_of_lis_nlogn([10,9,2,5,3,7,101,18])}")

    print("\n3. 二维 DP")
    print(f"  不同路径3x7: {unique_paths(3, 7)}")
    grid = [[1,3,1],[1,5,1],[4,2,1]]
    print(f"  最小路径和: {min_path_sum(grid)}")
    triangle = [[2],[3,4],[6,5,7],[4,1,8,3]]
    print(f"  三角形最小路径: {triangle_min_path(triangle)}")

    print("\n4. 字符串 DP")
    print(f"  LCS('abcde','ace'): {longest_common_subsequence('abcde','ace')}")
    print(f"  编辑距离('horse','ros'): {edit_distance('horse','ros')}")

    print("\n5. 背包问题")
    weights = [1, 3, 4]; values = [15, 20, 30]; capacity = 4
    print(f"  0/1背包: {knapsack_01(weights, values, capacity)}")
    print(f"  完全背包: {knapsack_complete(weights, values, capacity)}")
    print(f"  零钱兑换coins=[1,2,5],amount=11: {coin_change([1,2,5], 11)}")
    print(f"  零钱组合数amount=5: {coin_change_ways([1,2,5], 5)}")
    print(f"  等和子集[1,5,11,5]: {partition_equal_subset_sum([1,5,11,5])}")
