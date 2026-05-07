# ============================================================
# 数据结构与算法 - 第十五章：分治算法 & 字符串匹配
# ============================================================
# 分治：将问题分解为规模更小的同类子问题，递归解决后合并结果。
# 经典算法：归并排序、快速排序（已在排序章节）、快速幂、FFT 等。
# 字符串匹配：KMP、Rabin-Karp（滚动哈希）、Trie（前缀树）等。
# ============================================================

from typing import List, Optional
from collections import defaultdict


# ------------------------------------------------------------
# 1. 分治经典题
# ------------------------------------------------------------

def majority_element(nums: List[int]) -> int:
    """
    【题型】多数元素（出现超过 n/2 次）
    【方法一】Boyer-Moore 投票算法：O(n) 时间，O(1) 空间。
    维护候选人和计数，遇到相同的加1，不同的减1，减到0换候选人。
    """
    candidate = None
    count = 0
    for num in nums:
        if count == 0:
            candidate = num
        count += 1 if num == candidate else -1
    return candidate


def majority_element_divide(nums: List[int]) -> int:
    """
    多数元素（分治版）：左右两半各找多数元素，若相同则直接返回，否则统计频率取大者。
    """
    def divide(lo, hi):
        if lo == hi:
            return nums[lo]
        mid = (lo + hi) // 2
        left = divide(lo, mid)
        right = divide(mid + 1, hi)
        if left == right:
            return left
        # 两侧多数元素不同，统计各自频率
        left_count = sum(1 for i in range(lo, hi + 1) if nums[i] == left)
        right_count = sum(1 for i in range(lo, hi + 1) if nums[i] == right)
        return left if left_count > right_count else right

    return divide(0, len(nums) - 1)


def fast_power(base: float, exp: int) -> float:
    """
    快速幂：将指数 n 每次折半，O(log n) 次乘法完成 base^exp。
    处理负指数：转为 1 / base^(-exp)。
    """
    if exp < 0:
        base = 1 / base
        exp = -exp

    result = 1.0
    while exp > 0:
        if exp % 2 == 1:       # 奇数：多乘一次 base
            result *= base
        base *= base           # base 平方
        exp //= 2

    return result


def fast_power_recursive(base: float, exp: int) -> float:
    """快速幂递归版"""
    if exp == 0:
        return 1
    if exp < 0:
        return fast_power_recursive(1 / base, -exp)
    half = fast_power_recursive(base, exp // 2)
    if exp % 2 == 0:
        return half * half
    else:
        return half * half * base


def find_median_sorted_arrays(nums1: List[int], nums2: List[int]) -> float:
    """
    【题型】两个有序数组的中位数（O(log(m+n)) 时间）
    【思路】二分查找：在较短数组中二分切割位置，保证两个切割左侧元素数 = 总元素数//2。
    确保左侧最大值 ≤ 右侧最小值时，找到了正确的切割点。
    """
    # 保证 nums1 是较短的数组
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1

    m, n = len(nums1), len(nums2)
    total = m + n
    half = total // 2

    left, right = 0, m
    while left <= right:
        i = (left + right) // 2  # nums1 的切割点
        j = half - i              # nums2 的切割点

        # 切割点左侧的最大值和右侧的最小值
        nums1_left = nums1[i - 1] if i > 0 else float('-inf')
        nums1_right = nums1[i] if i < m else float('inf')
        nums2_left = nums2[j - 1] if j > 0 else float('-inf')
        nums2_right = nums2[j] if j < n else float('inf')

        if nums1_left <= nums2_right and nums2_left <= nums1_right:
            # 找到正确切割点
            if total % 2 == 1:
                return min(nums1_right, nums2_right)
            return (max(nums1_left, nums2_left) + min(nums1_right, nums2_right)) / 2
        elif nums1_left > nums2_right:
            right = i - 1  # nums1 左侧太大，左移切割点
        else:
            left = i + 1   # nums1 右侧太小，右移切割点


def max_subarray_divide(nums: List[int]) -> int:
    """
    最大子数组和（分治法）：
    最大子数组要么完全在左半，要么完全在右半，要么跨越中间。
    跨越中间：从中点向左/右分别找最大连续和，合并。
    """
    def divide(lo, hi):
        if lo == hi:
            return nums[lo]
        mid = (lo + hi) // 2

        # 左侧最大子数组
        left_max = divide(lo, mid)
        # 右侧最大子数组
        right_max = divide(mid + 1, hi)

        # 跨越中间的最大子数组
        left_cross = right_cross = 0
        running = 0
        for i in range(mid, lo - 1, -1):
            running += nums[i]
            left_cross = max(left_cross, running)
        running = 0
        for i in range(mid + 1, hi + 1):
            running += nums[i]
            right_cross = max(right_cross, running)
        cross_max = left_cross + right_cross

        return max(left_max, right_max, cross_max)

    return divide(0, len(nums) - 1)


# ------------------------------------------------------------
# 2. KMP 字符串匹配
# ------------------------------------------------------------

def kmp_search(text: str, pattern: str) -> List[int]:
    """
    KMP 算法：在文本串 text 中查找所有模式串 pattern 出现的位置。

    【核心】失配函数（PMT/next 数组）：记录模式串每个位置的最长公共前后缀长度。
    当匹配失败时，利用 next 数组将模式串向右滑动，避免重复比较。

    【复杂度】预处理 O(m)，搜索 O(n)，总体 O(n+m)
    """

    def build_next(pattern: str) -> List[int]:
        """
        构建 next 数组（部分匹配表）。
        next[i] = pattern[0..i] 的最长相等前后缀的长度。
        """
        m = len(pattern)
        next_arr = [0] * m
        k = 0  # 当前已匹配的前缀长度

        for i in range(1, m):
            # 失配时，跳到上一个最长前后缀的末尾继续比较
            while k > 0 and pattern[k] != pattern[i]:
                k = next_arr[k - 1]
            if pattern[k] == pattern[i]:
                k += 1
            next_arr[i] = k

        return next_arr

    if not pattern:
        return list(range(len(text) + 1))

    next_arr = build_next(pattern)
    matches = []
    k = 0  # 已匹配的字符数

    for i, char in enumerate(text):
        while k > 0 and pattern[k] != char:
            k = next_arr[k - 1]  # 利用 next 数组回退
        if pattern[k] == char:
            k += 1
        if k == len(pattern):
            matches.append(i - k + 1)  # 找到一个匹配，记录起始位置
            k = next_arr[k - 1]        # 继续搜索下一个

    return matches


def rabin_karp(text: str, pattern: str) -> List[int]:
    """
    Rabin-Karp 滚动哈希：通过哈希比较快速定位匹配，避免逐字符比较。

    【思路】计算模式串哈希值，滑动窗口维护文本子串的哈希值（O(1) 更新）。
           哈希相同时再逐字符验证（防止哈希冲突）。

    【复杂度】平均 O(n+m)，最坏 O(nm)（频繁哈希冲突）
    """
    n, m = len(text), len(pattern)
    if m > n:
        return []

    BASE = 26
    MOD = 10**9 + 7

    # 计算 BASE^(m-1) % MOD（用于滑动时移除最高位）
    power = pow(BASE, m - 1, MOD)

    # 计算模式串哈希
    pattern_hash = 0
    window_hash = 0
    for i in range(m):
        pattern_hash = (pattern_hash * BASE + ord(pattern[i])) % MOD
        window_hash = (window_hash * BASE + ord(text[i])) % MOD

    matches = []
    if window_hash == pattern_hash and text[:m] == pattern:
        matches.append(0)

    for i in range(1, n - m + 1):
        # 滚动哈希：移除最左字符，加入新右字符
        window_hash = (window_hash - ord(text[i - 1]) * power) % MOD
        window_hash = (window_hash * BASE + ord(text[i + m - 1])) % MOD

        if window_hash == pattern_hash and text[i:i + m] == pattern:
            matches.append(i)

    return matches


# ------------------------------------------------------------
# 3. 前缀树（Trie）
# ------------------------------------------------------------

class TrieNode:
    def __init__(self):
        self.children = {}     # 子节点字典：字符 -> TrieNode
        self.is_end = False    # 标记是否是某个单词的结尾


class Trie:
    """
    前缀树（字典树）：高效地存储和查找字符串集合。
    insert/search/startsWith 均为 O(m)，m 为字符串长度。
    空间：O(总字符数 * 字符集大小)
    """

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str):
        """插入单词"""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True  # 标记单词结尾

    def search(self, word: str) -> bool:
        """查找单词是否完整存在"""
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end  # 必须是单词结尾（不只是前缀）

    def starts_with(self, prefix: str) -> bool:
        """查找是否存在以 prefix 为前缀的单词"""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

    def find_words_with_prefix(self, prefix: str) -> List[str]:
        """找出所有以 prefix 为前缀的单词（自动补全）"""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]

        # DFS 收集所有以该节点为起点的单词
        result = []

        def dfs(cur_node, cur_word):
            if cur_node.is_end:
                result.append(cur_word)
            for c, child in cur_node.children.items():
                dfs(child, cur_word + c)

        dfs(node, prefix)
        return result


class WordDictionary:
    """
    带通配符的 Trie（'.' 匹配任意单个字符）
    在搜索时，遇到 '.' 则枚举所有子节点递归搜索。
    """

    def __init__(self):
        self.root = TrieNode()

    def add_word(self, word: str):
        node = self.root
        for c in word:
            if c not in node.children:
                node.children[c] = TrieNode()
            node = node.children[c]
        node.is_end = True

    def search(self, word: str) -> bool:
        def dfs(node, idx):
            if idx == len(word):
                return node.is_end
            c = word[idx]
            if c == '.':
                # 通配符：尝试所有子节点
                return any(dfs(child, idx + 1) for child in node.children.values())
            else:
                if c not in node.children:
                    return False
                return dfs(node.children[c], idx + 1)

        return dfs(self.root, 0)


# ------------------------------------------------------------
# 4. 字符串的其他经典算法
# ------------------------------------------------------------

def z_function(s: str) -> List[int]:
    """
    Z 函数（Z-array）：z[i] = s[i:] 与 s 的最长公共前缀长度。
    可用于字符串匹配（模式+分隔符+文本，找 z[i] == m 的位置）。
    【复杂度】O(n)
    """
    n = len(s)
    z = [0] * n
    z[0] = n
    l = r = 0  # 维护当前最远 Z-box 的左右边界

    for i in range(1, n):
        if i < r:
            z[i] = min(r - i, z[i - l])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] > r:
            l, r = i, i + z[i]

    return z


def manacher(s: str) -> str:
    """
    Manacher 算法：O(n) 找到字符串中最长回文子串。
    【思路】在每个字符间插入分隔符 '#'，将奇偶长度统一处理。
    利用已知的最长回文信息，减少重复比较。
    """
    # 预处理：插入 '#' 和边界 '$','@'
    t = '#'.join('^{}$'.format(s))
    n = len(t)
    p = [0] * n  # p[i] = 以 t[i] 为中心的回文半径
    c = r = 0    # 当前最右回文串的中心和右边界

    for i in range(1, n - 1):
        if i < r:
            mirror = 2 * c - i
            p[i] = min(r - i, p[mirror])

        # 暴力扩展
        while t[i + p[i] + 1] == t[i - p[i] - 1]:
            p[i] += 1

        # 更新最右回文串
        if i + p[i] > r:
            c, r = i, i + p[i]

    # 找最大回文半径，转回原字符串
    max_len, center = max((v, i) for i, v in enumerate(p))
    start = (center - max_len) // 2
    return s[start: start + max_len]


def minimum_window_substring(s: str, t: str) -> str:
    """
    【题型】最小覆盖子串（s 中包含 t 所有字符的最小窗口）
    【思路】滑动窗口 + 哈希表：右指针扩展到满足条件，左指针收缩到最小。
    """
    from collections import Counter
    if not t or not s:
        return ""

    need = Counter(t)         # 需要的字符及数量
    missing = len(t)          # 还差多少个字符
    start = end = 0
    result = ""

    for j, c in enumerate(s, 1):
        if need[c] > 0:
            missing -= 1
        need[c] -= 1

        if missing == 0:  # 当前窗口包含 t 的所有字符
            # 左指针收缩：移除不必要的字符
            while need[s[start]] < 0:
                need[s[start]] += 1
                start += 1
            if not result or j - start < len(result):
                result = s[start:j]
            # 再移出一个字符，准备继续扩展
            need[s[start]] += 1
            missing += 1
            start += 1

    return result


# ------------------------------------------------------------
# 主程序演示
# ------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 50)
    print("1. 分治")
    print(f"  多数元素[2,2,1,1,1,2,2]: {majority_element([2,2,1,1,1,2,2])}")
    print(f"  快速幂 2^10: {fast_power(2, 10)}")
    print(f"  快速幂 2^-2: {fast_power(2, -2)}")

    print("\n2. 两个有序数组中位数")
    print(f"  [1,3],[2]: {find_median_sorted_arrays([1,3],[2])}")
    print(f"  [1,2],[3,4]: {find_median_sorted_arrays([1,2],[3,4])}")

    print("\n3. KMP 字符串匹配")
    text = "AABAACAADAABAABA"
    pattern = "AABA"
    print(f"  文本='{text}', 模式='{pattern}'")
    print(f"  KMP 匹配位置: {kmp_search(text, pattern)}")
    print(f"  RK 匹配位置: {rabin_karp(text, pattern)}")

    print("\n4. Trie 前缀树")
    trie = Trie()
    for word in ["apple", "app", "application", "apply", "banana"]:
        trie.insert(word)
    print(f"  search('app'): {trie.search('app')}")
    print(f"  search('appl'): {trie.search('appl')}")
    print(f"  startsWith('app'): {trie.starts_with('app')}")
    print(f"  以'app'开头的单词: {trie.find_words_with_prefix('app')}")

    print("\n5. 带通配符的字典")
    wd = WordDictionary()
    for w in ["bad", "dad", "mad"]:
        wd.add_word(w)
    print(f"  search('pad'): {wd.search('pad')}")
    print(f"  search('.ad'): {wd.search('.ad')}")
    print(f"  search('b..'): {wd.search('b..')}")

    print("\n6. Manacher 最长回文子串")
    print(f"  'babad': {manacher('babad')}")
    print(f"  'cbbd': {manacher('cbbd')}")

    print("\n7. 最小覆盖子串")
    print(f"  s='ADOBECODEBANC', t='ABC': '{minimum_window_substring('ADOBECODEBANC','ABC')}'")
