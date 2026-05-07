# ============================================================
# 数据结构与算法 - 第十三章：贪心算法
# ============================================================
# 贪心算法：每步都做当前看起来最优的选择，希望全局最优。
# 关键：证明贪心选择的正确性（交换论证 / 反证法）。
# 贪心 vs DP：贪心不回头（每步唯一选择），DP 考虑所有可能。
# 适用场景：活动选择、区间调度、霍夫曼编码等。
# ============================================================

from typing import List
import heapq


# ------------------------------------------------------------
# 1. 区间贪心
# ------------------------------------------------------------

def activity_selection(intervals: List[List[int]]) -> int:
    """
    【题型】区间调度最大化（最多选几个不重叠区间）
    【贪心策略】按结束时间排序，优先选结束最早的区间（给后续活动留更多空间）。
    【时间复杂度】O(n log n)
    """
    if not intervals:
        return 0

    # 按结束时间升序排列
    intervals.sort(key=lambda x: x[1])

    count = 1
    last_end = intervals[0][1]

    for start, end in intervals[1:]:
        if start >= last_end:  # 当前区间与上一个不重叠
            count += 1
            last_end = end

    return count


def erase_overlap_intervals(intervals: List[List[int]]) -> int:
    """
    【题型】移除最少区间使剩余区间不重叠
    等价于：总区间数 - 最多不重叠区间数
    """
    n = len(intervals)
    return n - activity_selection(intervals)


def min_arrows_to_burst_balloons(points: List[List[int]]) -> int:
    """
    【题型】用最少的箭射爆所有气球（每个气球横跨 [xstart, xend]）
    【贪心策略】按右端点排序，尽量用一支箭射穿多个气球。
    当箭的当前位置不能覆盖下一个气球时，再射一支新箭。
    """
    if not points:
        return 0

    points.sort(key=lambda x: x[1])  # 按右端点排序
    arrows = 1
    arrow_pos = points[0][1]  # 第一支箭射在第一个气球右端点

    for start, end in points[1:]:
        if start > arrow_pos:  # 当前气球左端点超过当前箭，需要新箭
            arrows += 1
            arrow_pos = end

    return arrows


def merge_intervals(intervals: List[List[int]]) -> List[List[int]]:
    """
    【题型】合并重叠区间
    【策略】按左端点排序，遍历时若当前区间与上一个重叠则合并（更新右端点）。
    """
    if not intervals:
        return []

    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]

    for start, end in intervals[1:]:
        if start <= merged[-1][1]:  # 重叠：更新合并区间的右端点
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])

    return merged


def insert_interval(intervals: List[List[int]], new_interval: List[int]) -> List[List[int]]:
    """
    【题型】在有序不重叠区间列表中插入新区间（并合并重叠）
    三个阶段：新区间左侧的不重叠部分 → 合并阶段 → 新区间右侧的不重叠部分
    """
    result = []
    i = 0
    n = len(intervals)

    # 阶段1：在新区间左侧的所有区间直接加入
    while i < n and intervals[i][1] < new_interval[0]:
        result.append(intervals[i])
        i += 1

    # 阶段2：合并所有与新区间重叠的区间
    while i < n and intervals[i][0] <= new_interval[1]:
        new_interval[0] = min(new_interval[0], intervals[i][0])
        new_interval[1] = max(new_interval[1], intervals[i][1])
        i += 1
    result.append(new_interval)

    # 阶段3：新区间右侧的所有区间直接加入
    result.extend(intervals[i:])
    return result


def partition_labels(s: str) -> List[int]:
    """
    【题型】划分字母区间（将字符串分成尽可能多的片段，每个字母只出现在一个片段中）
    【策略】贪心地扩展当前片段的右边界到包含当前所有已遇字符的最后出现位置。
    """
    # 预处理：每个字符最后出现的位置
    last = {c: i for i, c in enumerate(s)}

    result = []
    start = end = 0

    for i, c in enumerate(s):
        end = max(end, last[c])  # 扩展当前片段右边界
        if i == end:             # 到达当前片段的边界
            result.append(end - start + 1)
            start = i + 1

    return result


# ------------------------------------------------------------
# 2. 跳跃游戏系列
# ------------------------------------------------------------

def can_jump(nums: List[int]) -> bool:
    """
    【题型】跳跃游戏 I（能否到达末尾）
    【贪心策略】维护能到达的最远位置。若当前位置超过了最远位置，则无法继续。
    """
    max_reach = 0
    for i, jump in enumerate(nums):
        if i > max_reach:
            return False  # 当前位置不可达
        max_reach = max(max_reach, i + jump)
    return True


def jump_game_min_steps(nums: List[int]) -> int:
    """
    【题型】跳跃游戏 II（最少跳跃次数到达末尾）
    【贪心策略】BFS 思想：每一跳内，找下一跳能到达的最远位置。
    当当前跳的范围用完时（i 到达 cur_end），跳数+1，更新范围。
    """
    jumps = 0
    cur_end = 0     # 当前跳能到达的最远位置（当前"层"的右边界）
    farthest = 0    # 下一跳能到达的最远位置

    for i in range(len(nums) - 1):
        farthest = max(farthest, i + nums[i])
        if i == cur_end:  # 到达当前跳的边界，必须跳一次
            jumps += 1
            cur_end = farthest
            if cur_end >= len(nums) - 1:
                break

    return jumps


# ------------------------------------------------------------
# 3. 贪心 + 排序
# ------------------------------------------------------------

def assign_cookies(g: List[int], s: List[int]) -> int:
    """
    【题型】分发饼干（每个孩子胃口为 g[i]，每块饼干大小为 s[j]，尽量满足多的孩子）
    【贪心】将孩子和饼干都排序，用最小的能满足当前孩子胃口的饼干满足他。
    """
    g.sort()
    s.sort()
    child = cookie = 0
    while child < len(g) and cookie < len(s):
        if s[cookie] >= g[child]:
            child += 1  # 满足一个孩子
        cookie += 1     # 无论是否满足，饼干都被用掉（或跳过）
    return child


def wiggle_subsequence(nums: List[int]) -> int:
    """
    【题型】摆动序列（相邻差值正负交替）的最长子序列长度
    【贪心】统计"峰值"和"谷值"的数量：每次方向改变时计数+1。
    """
    if len(nums) < 2:
        return len(nums)
    up = down = 1
    for i in range(1, len(nums)):
        if nums[i] > nums[i - 1]:
            up = down + 1
        elif nums[i] < nums[i - 1]:
            down = up + 1
    return max(up, down)


def is_possible_reconstruct(nums: List[int]) -> bool:
    """
    【题型】拼接连续子数组（每个子序列长度 ≥ 3，且为连续整数）
    【贪心策略】维护两个计数字典：freq（剩余次数），tail（以某值结尾的子序列数）。
    优先将当前数接在已有子序列末尾（贪心）；否则开启新子序列（需要后续 +1, +2）。
    """
    from collections import Counter
    freq = Counter(nums)
    tail = Counter()  # tail[i] = 有多少个子序列以 i 结尾

    for num in nums:
        if freq[num] == 0:
            continue  # 已被用完

        if tail[num - 1] > 0:
            # 接在以 num-1 结尾的子序列后
            tail[num - 1] -= 1
            tail[num] += 1
            freq[num] -= 1
        elif freq[num + 1] > 0 and freq[num + 2] > 0:
            # 开启新子序列：num, num+1, num+2
            tail[num + 2] += 1
            freq[num] -= 1
            freq[num + 1] -= 1
            freq[num + 2] -= 1
        else:
            return False  # 无法安置

    return True


# ------------------------------------------------------------
# 4. 霍夫曼编码（贪心经典应用）
# ------------------------------------------------------------

def huffman_encoding(freq: dict) -> dict:
    """
    霍夫曼编码：根据字符频率构建最优前缀码树，高频字符编码短，低频字符编码长。
    【算法】优先队列每次取两个最小频率节点合并，直到只剩根节点。
    返回每个字符的编码。
    """
    heap = [[f, [c, ""]] for c, f in freq.items()]
    heapq.heapify(heap)

    if len(heap) == 1:
        _, [c, _] = heapq.heappop(heap)
        return {c: "0"}

    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        # 为低频节点的每个编码前加 '0'，高频节点前加 '1'
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])

    return dict(heapq.heappop(heap)[1:])


# ------------------------------------------------------------
# 5. 贪心在任务调度中的应用
# ------------------------------------------------------------

def minimum_waiting_time(query_times: List[int]) -> int:
    """
    最小等待时间（将短查询排在前面，减少后续等待）
    排序后，第 i 个查询使后续 n-1-i 个查询都多等 query_times[i]。
    """
    query_times.sort()
    return sum(t * (len(query_times) - 1 - i) for i, t in enumerate(query_times))


def optimal_file_merge(files: List[int]) -> int:
    """
    最优文件合并（每次合并两个文件，费用为合并后的文件大小，求最小总费用）
    等价于霍夫曼树的构建：用最小堆每次取最小两个合并。
    """
    heapq.heapify(files)
    total = 0
    while len(files) > 1:
        a = heapq.heappop(files)
        b = heapq.heappop(files)
        total += a + b
        heapq.heappush(files, a + b)
    return total


# ------------------------------------------------------------
# 主程序演示
# ------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 50)
    print("1. 区间调度")
    intervals = [[1,2],[2,3],[3,4],[1,3]]
    print(f"  最多不重叠区间: {activity_selection(intervals)}")
    print(f"  最少移除区间数: {erase_overlap_intervals(intervals)}")

    print("\n2. 气球与箭")
    points = [[10,16],[2,8],[1,6],[7,12]]
    print(f"  最少箭数: {min_arrows_to_burst_balloons(points)}")

    print("\n3. 合并区间")
    intervals2 = [[1,3],[2,6],[8,10],[15,18]]
    print(f"  合并结果: {merge_intervals(intervals2)}")

    print("\n4. 插入区间")
    print(f"  {insert_interval([[1,3],[6,9]], [2,5])}")

    print("\n5. 划分字母区间")
    print(f"  'ababcbacadefegdehijhklij': {partition_labels('ababcbacadefegdehijhklij')}")

    print("\n6. 跳跃游戏")
    print(f"  [2,3,1,1,4] 能否到达: {can_jump([2,3,1,1,4])}")
    print(f"  [3,2,1,0,4] 能否到达: {can_jump([3,2,1,0,4])}")
    print(f"  [2,3,1,1,4] 最少跳数: {jump_game_min_steps([2,3,1,1,4])}")

    print("\n7. 分发饼干")
    print(f"  g=[1,2,3] s=[1,1]: {assign_cookies([1,2,3],[1,1])}")
    print(f"  g=[1,2] s=[1,2,3]: {assign_cookies([1,2],[1,2,3])}")

    print("\n8. 霍夫曼编码")
    freq = {'a': 45, 'b': 13, 'c': 12, 'd': 16, 'e': 9, 'f': 5}
    codes = huffman_encoding(freq)
    for char, code in sorted(codes.items()):
        print(f"  '{char}'({freq[char]}): {code}")

    print("\n9. 最优文件合并")
    print(f"  [4,3,2,6] 最小合并费: {optimal_file_merge([4,3,2,6])}")
