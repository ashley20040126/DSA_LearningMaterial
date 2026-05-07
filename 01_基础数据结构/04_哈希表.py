# ============================================================
# 数据结构与算法 - 第四章：哈希表
# ============================================================
# 哈希表通过哈希函数将键映射到数组下标，实现平均 O(1) 的增删改查。
# 核心问题：哈希冲突处理（链地址法 / 开放寻址法）。
# Python 的 dict 和 set 都是哈希表的封装。
# ============================================================

from collections import defaultdict, Counter


# ------------------------------------------------------------
# 1. 手写哈希表（链地址法处理冲突）
# ------------------------------------------------------------

class HashMap:
    """
    基于链地址法的哈希表实现。
    每个桶存储一个链表（用列表模拟），解决哈希冲突。
    装载因子 > 0.75 时自动扩容（翻倍）。
    """

    def __init__(self, capacity=16):
        self.capacity = capacity
        self.size = 0
        # 桶数组，每个桶是一个列表（存 [key, value] 对）
        self.buckets = [[] for _ in range(capacity)]

    def _hash(self, key) -> int:
        """哈希函数：对 key 的 hash 值取模得到桶下标"""
        return hash(key) % self.capacity

    def _load_factor(self) -> float:
        return self.size / self.capacity

    def _resize(self):
        """装载因子超过0.75时，将容量翻倍并重新哈希所有元素"""
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0
        for bucket in old_buckets:
            for key, val in bucket:
                self.put(key, val)

    def put(self, key, value):
        """插入或更新键值对"""
        if self._load_factor() > 0.75:
            self._resize()

        idx = self._hash(key)
        bucket = self.buckets[idx]

        # 检查是否已存在该 key（更新）
        for pair in bucket:
            if pair[0] == key:
                pair[1] = value
                return

        # 不存在则新增
        bucket.append([key, value])
        self.size += 1

    def get(self, key):
        """获取 key 对应的值，不存在返回 -1"""
        idx = self._hash(key)
        for k, v in self.buckets[idx]:
            if k == key:
                return v
        return -1

    def remove(self, key):
        """删除键值对"""
        idx = self._hash(key)
        bucket = self.buckets[idx]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self.size -= 1
                return


# ------------------------------------------------------------
# 2. 哈希表经典题型
# ------------------------------------------------------------

def two_sum(nums: list, target: int) -> list:
    """
    【题型】两数之和（最经典的哈希表题）
    【思路】遍历时，检查 target - nums[i] 是否已在哈希表中。
           边遍历边存入，避免重复使用同一元素。
    【复杂度】时间 O(n)，空间 O(n)
    """
    seen = {}  # 存储：值 -> 下标
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []


def group_anagrams(strs: list) -> list:
    """
    【题型】字母异位词分组
    【思路】异位词排序后一定相同，以排序后的字符串为键分组。
    【复杂度】时间 O(n * k log k)，k 为最长字符串长度
    """
    groups = defaultdict(list)
    for s in strs:
        key = ''.join(sorted(s))  # 排序作为哈希键
        groups[key].append(s)
    return list(groups.values())


def longest_consecutive_sequence(nums: list) -> int:
    """
    【题型】最长连续序列
    【思路】将所有数存入集合，仅从序列起点（num-1 不在集合中）开始计数，
           避免重复计算，每个数只被处理一次。
    【复杂度】时间 O(n)，空间 O(n)
    """
    num_set = set(nums)
    max_len = 0

    for num in num_set:
        # 只从连续序列的起点开始统计（num-1 不在集合中说明是起点）
        if num - 1 not in num_set:
            current = num
            length = 1
            while current + 1 in num_set:
                current += 1
                length += 1
            max_len = max(max_len, length)

    return max_len


def subarray_sum_zero(nums: list) -> list:
    """
    【题型】和为零的最长子数组（前缀和 + 哈希表）
    【思路】若 prefix[j] == prefix[i]，则 nums[i+1..j] 的和为零。
           用哈希表记录每个前缀和第一次出现的位置。
    【复杂度】时间 O(n)，空间 O(n)
    """
    prefix_sum = 0
    first_seen = {0: -1}  # 前缀和 -> 第一次出现的下标
    max_len = 0
    result = []

    for i, num in enumerate(nums):
        prefix_sum += num
        if prefix_sum in first_seen:
            length = i - first_seen[prefix_sum]
            if length > max_len:
                max_len = length
                result = nums[first_seen[prefix_sum] + 1: i + 1]
        else:
            first_seen[prefix_sum] = i

    return result


def is_isomorphic(s: str, t: str) -> bool:
    """
    【题型】同构字符串
    【思路】用两个哈希表，分别记录 s->t 和 t->s 的字符映射，
           确保双向映射一致。
    """
    if len(s) != len(t):
        return False
    s_to_t = {}
    t_to_s = {}
    for c1, c2 in zip(s, t):
        if (c1 in s_to_t and s_to_t[c1] != c2) or \
           (c2 in t_to_s and t_to_s[c2] != c1):
            return False
        s_to_t[c1] = c2
        t_to_s[c2] = c1
    return True


def top_k_frequent(nums: list, k: int) -> list:
    """
    【题型】前 K 个高频元素
    【思路】Counter 统计频次，取前 K 个。
           也可用堆优化到 O(n log k)，此处用 most_common O(n log n)。
    """
    return [num for num, _ in Counter(nums).most_common(k)]


def word_pattern(pattern: str, s: str) -> bool:
    """
    【题型】单词规律（类似同构字符串）
    【思路】双向哈希表建立字母-单词的双射关系。
    """
    words = s.split()
    if len(pattern) != len(words):
        return False
    char_to_word = {}
    word_to_char = {}
    for char, word in zip(pattern, words):
        if char in char_to_word:
            if char_to_word[char] != word:
                return False
        else:
            if word in word_to_char:
                return False
            char_to_word[char] = word
            word_to_char[word] = char
    return True


def four_sum_count(nums1, nums2, nums3, nums4) -> int:
    """
    【题型】四数相加 II（4个数组各取一个，使和为0）
    【思路】分治 + 哈希：先统计前两个数组所有两数之和的频次，
           再遍历后两个数组检查互补值。
    【复杂度】时间 O(n²)，空间 O(n²)
    """
    ab_sum = defaultdict(int)
    for a in nums1:
        for b in nums2:
            ab_sum[a + b] += 1

    count = 0
    for c in nums3:
        for d in nums4:
            count += ab_sum[-(c + d)]  # 查找 0 - (c+d)

    return count


# ------------------------------------------------------------
# 3. 设计哈希集合（不存值，只存键）
# ------------------------------------------------------------

class HashSet:
    """
    手写哈希集合（链地址法）。
    set 相当于 value 固定为 True 的 HashMap。
    """
    def __init__(self, capacity=1024):
        self.capacity = capacity
        self.buckets = [[] for _ in range(capacity)]

    def _hash(self, key: int) -> int:
        return key % self.capacity

    def add(self, key: int):
        idx = self._hash(key)
        if key not in self.buckets[idx]:
            self.buckets[idx].append(key)

    def remove(self, key: int):
        idx = self._hash(key)
        if key in self.buckets[idx]:
            self.buckets[idx].remove(key)

    def contains(self, key: int) -> bool:
        idx = self._hash(key)
        return key in self.buckets[idx]


# ------------------------------------------------------------
# 主程序演示
# ------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 50)
    print("1. 自定义哈希表")
    hm = HashMap()
    hm.put("name", "Alice")
    hm.put("age", 25)
    print(f"  name={hm.get('name')}, age={hm.get('age')}")
    hm.remove("age")
    print(f"  删除 age 后: {hm.get('age')}")

    print("\n2. 两数之和")
    print(f"  [2,7,11,15] 目标9: {two_sum([2,7,11,15], 9)}")

    print("\n3. 字母异位词分组")
    strs = ["eat","tea","tan","ate","nat","bat"]
    for group in group_anagrams(strs):
        print(f"  {group}")

    print("\n4. 最长连续序列")
    print(f"  [100,4,200,1,3,2]: {longest_consecutive_sequence([100,4,200,1,3,2])}")

    print("\n5. 前K高频元素")
    print(f"  [1,1,1,2,2,3] 前2个: {top_k_frequent([1,1,1,2,2,3], 2)}")

    print("\n6. 单词规律")
    print(f"  pattern='abba', s='dog cat cat dog': {word_pattern('abba', 'dog cat cat dog')}")
    print(f"  pattern='abba', s='dog cat cat fish': {word_pattern('abba', 'dog cat cat fish')}")

    print("\n7. 四数相加")
    a = [1, 2]; b = [-2, -1]; c = [-1, 2]; d = [0, 2]
    print(f"  结果: {four_sum_count(a, b, c, d)}")
