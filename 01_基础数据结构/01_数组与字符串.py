# ============================================================
# 数据结构与算法 - 第一章：数组与字符串
# ============================================================
# 数组是最基础的数据结构，在内存中连续存储，支持 O(1) 随机访问。
# Python 中的 list 就是动态数组，字符串是不可变序列。
# ============================================================

# ------------------------------------------------------------
# 1. 数组基本操作与时间复杂度分析
# ------------------------------------------------------------

def array_basics():
    """演示数组的基本操作及其时间复杂度"""

    arr = [3, 1, 4, 1, 5, 9, 2, 6]

    # O(1) - 随机访问（通过下标直接定位内存地址）
    print(f"第3个元素: {arr[2]}")

    # O(n) - 在末尾插入（平均情况，涉及动态扩容时为摊销O(1)）
    arr.append(5)

    # O(n) - 在头部插入（需要将所有元素向后移动一位）
    arr.insert(0, 99)

    # O(n) - 删除指定位置元素（需要将后续元素前移）
    arr.pop(0)

    # O(n) - 线性查找（最坏情况需遍历所有元素）
    target = 9
    for i, val in enumerate(arr):
        if val == target:
            print(f"找到 {target}，位置: {i}")
            break

    print(f"最终数组: {arr}")


# ------------------------------------------------------------
# 2. 双指针技巧 —— 解决数组中的对撞/同向问题
# ------------------------------------------------------------

def two_pointers_remove_duplicates(nums: list) -> int:
    """
    【题型】有序数组去重（原地修改）
    【思路】慢指针 slow 指向待填入位置，快指针 fast 向前探索。
           当 fast 指向的值与 slow 不同时，才将其写入 slow+1。
    【复杂度】时间 O(n)，空间 O(1)
    """
    if not nums:
        return 0

    slow = 0  # slow 指向当前不重复序列的末尾
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]:
            slow += 1
            nums[slow] = nums[fast]  # 将新的不重复值写到慢指针位置

    return slow + 1  # 不重复元素个数


def two_pointers_two_sum(nums: list, target: int):
    """
    【题型】有序数组中找两数之和等于 target
    【思路】左右指针从两端向中间逼近。
           - 和太小 → 左指针右移（增大）
           - 和太大 → 右指针左移（减小）
    【复杂度】时间 O(n)，空间 O(1)
    """
    left, right = 0, len(nums) - 1

    while left < right:
        current_sum = nums[left] + nums[right]
        if current_sum == target:
            return [left, right]
        elif current_sum < target:
            left += 1   # 总和不够，左指针右移以增大
        else:
            right -= 1  # 总和超了，右指针左移以减小

    return []  # 无解


def two_pointers_reverse(s: list) -> list:
    """
    【题型】原地翻转数组/字符串
    【思路】左右对撞指针，交换元素直到相遇
    【复杂度】时间 O(n)，空间 O(1)
    """
    left, right = 0, len(s) - 1
    while left < right:
        s[left], s[right] = s[right], s[left]
        left += 1
        right -= 1
    return s


# ------------------------------------------------------------
# 3. 滑动窗口 —— 解决子数组/子字符串问题
# ------------------------------------------------------------

def sliding_window_max_sum(nums: list, k: int) -> int:
    """
    【题型】长度为 k 的子数组中的最大和（固定窗口）
    【思路】先算前 k 个的和，然后窗口右移时加入新元素、减去旧元素。
    【复杂度】时间 O(n)，空间 O(1)
    """
    if len(nums) < k:
        return 0

    # 初始化第一个窗口
    window_sum = sum(nums[:k])
    max_sum = window_sum

    # 窗口向右滑动：加入右边新元素，移除左边旧元素
    for i in range(k, len(nums)):
        window_sum += nums[i] - nums[i - k]
        max_sum = max(max_sum, window_sum)

    return max_sum


def sliding_window_longest_no_repeat(s: str) -> int:
    """
    【题型】最长无重复字符子串（可变窗口）
    【思路】用哈希表记录字符最近出现的位置。
           right 向右扩展；当出现重复字符时，left 跳到重复字符上次位置+1。
    【复杂度】时间 O(n)，空间 O(字符集大小)
    """
    char_index = {}  # 记录每个字符最近一次出现的下标
    max_len = 0
    left = 0  # 窗口左边界

    for right, char in enumerate(s):
        # 如果字符已在窗口内，将左边界移到重复字符的下一位
        if char in char_index and char_index[char] >= left:
            left = char_index[char] + 1

        char_index[char] = right  # 更新字符最新位置
        max_len = max(max_len, right - left + 1)

    return max_len


# ------------------------------------------------------------
# 4. 前缀和 —— O(1) 查询任意子数组之和
# ------------------------------------------------------------

class PrefixSum:
    """
    前缀和技巧：将区间查询从 O(n) 优化到 O(1)。
    预处理时间 O(n)，单次查询 O(1)。

    核心公式：sum(i, j) = prefix[j+1] - prefix[i]
    其中 prefix[i] = nums[0] + nums[1] + ... + nums[i-1]
    """

    def __init__(self, nums: list):
        n = len(nums)
        self.prefix = [0] * (n + 1)  # prefix[0] = 0，方便处理边界
        for i in range(n):
            self.prefix[i + 1] = self.prefix[i] + nums[i]

    def range_sum(self, left: int, right: int) -> int:
        """查询 nums[left..right] 的区间和，O(1)"""
        return self.prefix[right + 1] - self.prefix[left]


def subarray_sum_equals_k(nums: list, k: int) -> int:
    """
    【题型】和为 k 的子数组个数
    【思路】前缀和 + 哈希表。
           若 prefix[j] - prefix[i] = k，则 nums[i..j-1] 的和为 k。
           等价于在之前的前缀和中查找 prefix[j] - k 出现了几次。
    【复杂度】时间 O(n)，空间 O(n)
    """
    count = 0
    prefix_sum = 0
    # 哈希表存储：前缀和 → 出现次数
    freq = {0: 1}  # 前缀和为0出现1次（空数组的前缀和）

    for num in nums:
        prefix_sum += num
        # 查找之前是否存在前缀和为 prefix_sum - k
        count += freq.get(prefix_sum - k, 0)
        freq[prefix_sum] = freq.get(prefix_sum, 0) + 1

    return count


# ------------------------------------------------------------
# 5. 字符串常用操作
# ------------------------------------------------------------

def is_palindrome(s: str) -> bool:
    """
    判断字符串是否为回文（只考虑字母和数字，忽略大小写）
    双指针从两端向中间扫描
    """
    left, right = 0, len(s) - 1
    while left < right:
        # 跳过非字母数字字符
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True


def longest_common_prefix(strs: list) -> str:
    """
    求字符串数组的最长公共前缀
    纵向扫描：以第一个字符串为基准，逐列比较
    """
    if not strs:
        return ""

    for i in range(len(strs[0])):
        char = strs[0][i]
        # 检查所有字符串在位置 i 的字符是否相同
        for j in range(1, len(strs)):
            if i >= len(strs[j]) or strs[j][i] != char:
                return strs[0][:i]  # 发现不同，返回到 i 之前的前缀

    return strs[0]  # 第一个字符串本身就是最长公共前缀


# ------------------------------------------------------------
# 主程序演示
# ------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 50)
    print("1. 数组基本操作")
    array_basics()

    print("\n2. 双指针 - 有序数组去重")
    nums = [1, 1, 2, 3, 3, 4, 5, 5]
    length = two_pointers_remove_duplicates(nums)
    print(f"不重复元素个数: {length}，数组前几位: {nums[:length]}")

    print("\n3. 双指针 - 两数之和")
    nums = [2, 7, 11, 15]
    print(f"目标24，结果: {two_pointers_two_sum(nums, 24)}")

    print("\n4. 滑动窗口 - 最大子数组和")
    nums = [1, 3, -1, -3, 5, 3, 6, 7]
    print(f"k=3时最大和: {sliding_window_max_sum(nums, 3)}")

    print("\n5. 滑动窗口 - 最长无重复子串")
    s = "abcabcbb"
    print(f"'{s}' 最长无重复子串长度: {sliding_window_longest_no_repeat(s)}")

    print("\n6. 前缀和查询")
    ps = PrefixSum([1, 2, 3, 4, 5])
    print(f"区间[1,3]的和: {ps.range_sum(1, 3)}")  # 2+3+4=9

    print("\n7. 和为k的子数组个数")
    print(f"[1,1,1] 中和为2的子数组: {subarray_sum_equals_k([1, 1, 1], 2)}")

    print("\n8. 回文判断")
    print(f"'A man a plan a canal Panama': {is_palindrome('A man a plan a canal Panama')}")

    print("\n9. 最长公共前缀")
    print(f"['flower','flow','flight']: {longest_common_prefix(['flower', 'flow', 'flight'])}")
