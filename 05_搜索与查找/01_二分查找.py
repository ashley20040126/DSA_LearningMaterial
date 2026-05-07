# ============================================================
# 数据结构与算法 - 第十章：二分查找
# ============================================================
# 二分查找：在有序（或具有单调性）的搜索空间中，每次排除一半。
# 时间复杂度 O(log n)。
#
# 框架：
#   left, right = 0, n-1  (或 n)
#   while left <= right:  (或 left < right)
#       mid = left + (right - left) // 2  (避免溢出)
#       if 条件:
#           right = mid - 1  (或 mid)
#       else:
#           left = mid + 1
#
# 关键：搞清楚搜索区间是 [left, right] 还是 [left, right)
# ============================================================

from typing import List


# ------------------------------------------------------------
# 1. 基础二分查找
# ------------------------------------------------------------

def binary_search(nums: List[int], target: int) -> int:
    """
    在有序数组中查找 target，返回下标；不存在返回 -1。
    搜索区间：[left, right]（闭区间）
    """
    left, right = 0, len(nums) - 1

    while left <= right:  # 区间不为空时继续
        mid = left + (right - left) // 2  # 等价于 (left+right)//2，但避免溢出

        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1   # target 在右半部分，缩小到 [mid+1, right]
        else:
            right = mid - 1  # target 在左半部分，缩小到 [left, mid-1]

    return -1


# ------------------------------------------------------------
# 2. 二分查找变体（找左右边界）
# ------------------------------------------------------------

def lower_bound(nums: List[int], target: int) -> int:
    """
    左边界：找第一个 >= target 的位置（相当于 C++ lower_bound）。
    若不存在，返回 len(nums)。
    应用：找 target 第一次出现的位置。
    """
    left, right = 0, len(nums)  # 注意 right = len(nums)（半开区间）

    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] < target:
            left = mid + 1  # 排除左半部分（包括 mid）
        else:
            right = mid     # mid 可能是答案，保留

    return left  # left 即为第一个 >= target 的位置


def upper_bound(nums: List[int], target: int) -> int:
    """
    右边界：找第一个 > target 的位置（相当于 C++ upper_bound）。
    若不存在，返回 len(nums)。
    应用：target 最后出现的位置 = upper_bound - 1。
    """
    left, right = 0, len(nums)

    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] <= target:
            left = mid + 1
        else:
            right = mid

    return left


def find_first_last(nums: List[int], target: int) -> List[int]:
    """
    【题型】在有序数组中找 target 第一次和最后一次出现的位置。
    利用 lower_bound 和 upper_bound 实现。
    """
    first = lower_bound(nums, target)
    if first == len(nums) or nums[first] != target:
        return [-1, -1]  # target 不存在

    last = upper_bound(nums, target) - 1
    return [first, last]


# ------------------------------------------------------------
# 3. 旋转数组相关（二分查找的重要变体）
# ------------------------------------------------------------

def search_rotated(nums: List[int], target: int) -> int:
    """
    【题型】搜索旋转排序数组（无重复元素）
    【思路】旋转后，至少有一半是有序的。判断 mid 在哪半，再判断 target 在有序半中。
    关键：先判断哪半有序，再判断 target 在不在有序半中。
    """
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid

        if nums[left] <= nums[mid]:
            # 左半部分有序 [left, mid]
            if nums[left] <= target < nums[mid]:
                right = mid - 1  # target 在有序的左半
            else:
                left = mid + 1   # target 在右半（含旋转点）
        else:
            # 右半部分有序 [mid, right]
            if nums[mid] < target <= nums[right]:
                left = mid + 1   # target 在有序的右半
            else:
                right = mid - 1  # target 在左半（含旋转点）

    return -1


def find_minimum_rotated(nums: List[int]) -> int:
    """
    【题型】旋转数组中的最小值（无重复）
    【思路】最小值在旋转点处。比较 mid 和 right：
           若 nums[mid] > nums[right]，最小值在右半；否则在左半（含 mid）。
    """
    left, right = 0, len(nums) - 1

    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] > nums[right]:
            left = mid + 1   # mid 不可能是最小值
        else:
            right = mid      # mid 可能是最小值，保留

    return nums[left]


# ------------------------------------------------------------
# 4. 答案二分（在值域上二分）
# ------------------------------------------------------------

def koko_eating_bananas(piles: List[int], h: int) -> int:
    """
    【题型】爱吃香蕉的珂珂（LeetCode 875）
    【描述】珂珂以速度 k 吃香蕉（每小时吃 k 根），h 小时内吃完所有堆。求最小 k。
    【思路】对答案二分：k 的范围是 [1, max(piles)]。
           判断函数：以速度 k 吃完所有堆需要的时间 ≤ h 吗？
    """
    import math

    def can_finish(speed: int) -> bool:
        # 以速度 speed 吃完所有堆需要的小时数
        hours = sum(math.ceil(pile / speed) for pile in piles)
        return hours <= h

    left, right = 1, max(piles)
    # 找最小的能满足条件的 k（左边界）
    while left < right:
        mid = left + (right - left) // 2
        if can_finish(mid):
            right = mid     # mid 可能是答案，缩小到左半
        else:
            left = mid + 1  # mid 不够快，排除

    return left


def minimum_days_to_bloom(bloomDay: List[int], m: int, k: int) -> int:
    """
    【题型】制作 m 束花，每束需要 k 朵连续的花，求最少等待天数。
    【思路】对天数 d 二分，判断等 d 天后能否制作 m 束花。
    """
    def can_make(d: int) -> bool:
        flowers = bunches = 0
        for day in bloomDay:
            if day <= d:
                flowers += 1
                if flowers == k:
                    bunches += 1
                    flowers = 0
            else:
                flowers = 0  # 连续中断
        return bunches >= m

    if len(bloomDay) < m * k:
        return -1

    left, right = min(bloomDay), max(bloomDay)
    while left < right:
        mid = left + (right - left) // 2
        if can_make(mid):
            right = mid
        else:
            left = mid + 1

    return left


def split_array_largest_sum(nums: List[int], k: int) -> int:
    """
    【题型】分割数组的最大值（将数组分 k 段，最小化各段和的最大值）
    【思路】对"最大段和"二分：范围是 [max(nums), sum(nums)]。
           判断函数：在最大段和 ≤ mid 的限制下，最少需要几段？若 ≤ k 则可行。
    """
    def can_split(max_sum: int) -> bool:
        # 贪心：尽量让每段尽可能长（在不超过 max_sum 的前提下）
        segments = 1
        current = 0
        for num in nums:
            if current + num > max_sum:
                segments += 1
                current = num
            else:
                current += num
        return segments <= k

    left, right = max(nums), sum(nums)
    while left < right:
        mid = left + (right - left) // 2
        if can_split(mid):
            right = mid
        else:
            left = mid + 1

    return left


# ------------------------------------------------------------
# 5. 二维矩阵上的二分
# ------------------------------------------------------------

def search_matrix(matrix: List[List[int]], target: int) -> bool:
    """
    【题型】搜索 m×n 矩阵（每行升序，每行首元素 > 上行末元素）
    【思路一】将矩阵视为一维有序数组，下标转换：row=mid//n, col=mid%n。
    【复杂度】O(log(m*n))
    """
    if not matrix or not matrix[0]:
        return False
    m, n = len(matrix), len(matrix[0])
    left, right = 0, m * n - 1

    while left <= right:
        mid = left + (right - left) // 2
        val = matrix[mid // n][mid % n]
        if val == target:
            return True
        elif val < target:
            left = mid + 1
        else:
            right = mid - 1

    return False


def search_matrix_ii(matrix: List[List[int]], target: int) -> bool:
    """
    【题型】搜索矩阵 II（每行每列都升序，但行列无整体有序关系）
    【思路】从右上角出发：当前值 > target 则左移（排除一列），< target 则下移（排除一行）。
    【复杂度】O(m+n)
    """
    if not matrix:
        return False
    row, col = 0, len(matrix[0]) - 1  # 从右上角开始

    while row < len(matrix) and col >= 0:
        if matrix[row][col] == target:
            return True
        elif matrix[row][col] > target:
            col -= 1  # 当前列都比 target 大，排除
        else:
            row += 1  # 当前行都比 target 小，排除

    return False


# ------------------------------------------------------------
# 6. 其他二分查找经典题
# ------------------------------------------------------------

def find_peak_element(nums: List[int]) -> int:
    """
    【题型】寻找峰值（相邻元素不相等）
    【思路】若 nums[mid] < nums[mid+1]，右侧必有峰值；否则左侧（含mid）必有峰值。
    """
    left, right = 0, len(nums) - 1
    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] < nums[mid + 1]:
            left = mid + 1   # 峰值在右侧
        else:
            right = mid      # 峰值在左侧（含mid）
    return left


def find_sqrt(x: int) -> int:
    """
    【题型】求整数平方根（下取整）
    """
    if x < 2:
        return x
    left, right = 1, x // 2
    while left <= right:
        mid = left + (right - left) // 2
        if mid * mid == x:
            return mid
        elif mid * mid < x:
            left = mid + 1
        else:
            right = mid - 1
    return right  # right 是最大的满足 right² ≤ x 的值


def single_non_duplicate(nums: List[int]) -> int:
    """
    【题型】有序数组中的单一元素（其余每个元素出现两次）
    【思路】正常情况下，成对元素中第一个在偶数下标，第二个在奇数下标。
           若 mid 为偶数且 nums[mid] == nums[mid+1]，说明单一元素在右侧。
    """
    left, right = 0, len(nums) - 1
    while left < right:
        mid = left + (right - left) // 2
        # 确保 mid 是偶数（便于成对比较）
        if mid % 2 == 1:
            mid -= 1
        if nums[mid] == nums[mid + 1]:
            left = mid + 2  # 这对元素完整，单一元素在右侧
        else:
            right = mid     # 这对元素不完整，单一元素在左侧（含mid）
    return nums[left]


# ------------------------------------------------------------
# 主程序演示
# ------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 50)
    print("1. 基础二分查找")
    nums = [1, 3, 5, 7, 9, 11, 13, 15]
    print(f"  查找7: {binary_search(nums, 7)}")
    print(f"  查找6: {binary_search(nums, 6)}")

    print("\n2. 边界查找")
    nums2 = [1, 2, 2, 2, 3, 4]
    print(f"  [1,2,2,2,3,4] 中2的位置: {find_first_last(nums2, 2)}")

    print("\n3. 旋转数组")
    rotated = [4, 5, 6, 7, 0, 1, 2]
    print(f"  {rotated} 查找0: {search_rotated(rotated, 0)}")
    print(f"  最小值: {find_minimum_rotated(rotated)}")

    print("\n4. 答案二分")
    piles = [3, 6, 7, 11]
    print(f"  珂珂吃香蕉 h=8: {koko_eating_bananas(piles, 8)}")

    nums3 = [7, 2, 5, 10, 8]
    print(f"  分割数组k=2最大值: {split_array_largest_sum(nums3, 2)}")

    print("\n5. 矩阵二分")
    matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]]
    print(f"  搜索3: {search_matrix(matrix, 3)}")
    print(f"  搜索13: {search_matrix(matrix, 13)}")

    print("\n6. 其他")
    print(f"  峰值: {find_peak_element([1,2,3,1])}")
    print(f"  sqrt(8): {find_sqrt(8)}")
    print(f"  单一元素: {single_non_duplicate([1,1,2,3,3,4,4,8,8])}")
