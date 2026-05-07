# ============================================================
# 数据结构与算法 - 第九章：排序算法
# ============================================================
# 排序算法分类：
# 【比较排序】下界 O(n log n)
#   - 简单排序：冒泡 O(n²)、选择 O(n²)、插入 O(n²)
#   - 高效排序：归并 O(n log n)、快速 O(n log n)、堆排序 O(n log n)
# 【非比较排序】可突破 O(n log n)
#   - 计数排序 O(n+k)、桶排序 O(n+k)、基数排序 O(d*(n+k))
# ============================================================

import random
from typing import List


# ------------------------------------------------------------
# 1. 冒泡排序（Bubble Sort）
# ------------------------------------------------------------

def bubble_sort(arr: List[int]) -> List[int]:
    """
    【思路】每轮将最大元素"冒泡"到末尾。
           设 flag 优化：若某轮没有交换，说明已有序，提前终止。
    【复杂度】时间 O(n²) 最坏/平均，O(n) 最好（有序序列）；空间 O(1)
    【稳定性】稳定（相等元素不交换）
    """
    arr = arr[:]  # 不修改原数组
    n = len(arr)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):  # 每轮末尾 i 个已排好
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break  # 本轮无交换，已完全有序
    return arr


# ------------------------------------------------------------
# 2. 选择排序（Selection Sort）
# ------------------------------------------------------------

def selection_sort(arr: List[int]) -> List[int]:
    """
    【思路】每轮在未排序部分找最小值，放到已排序部分末尾。
    【复杂度】时间 O(n²)（不论原始顺序）；空间 O(1)
    【稳定性】不稳定（跨越式交换可能打乱相等元素顺序）
    """
    arr = arr[:]
    n = len(arr)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


# ------------------------------------------------------------
# 3. 插入排序（Insertion Sort）
# ------------------------------------------------------------

def insertion_sort(arr: List[int]) -> List[int]:
    """
    【思路】将每个元素插入到前面已排好序的合适位置（如同整理扑克牌）。
    【复杂度】时间 O(n²) 最坏，O(n) 最好（几乎有序）；空间 O(1)
    【稳定性】稳定
    【应用】小数组或接近有序时比快排更高效，常作为混合排序的基础
    """
    arr = arr[:]
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        # 将比 key 大的元素后移，为 key 腾出位置
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


# ------------------------------------------------------------
# 4. 希尔排序（Shell Sort）
# ------------------------------------------------------------

def shell_sort(arr: List[int]) -> List[int]:
    """
    【思路】插入排序的改进版：先对间隔较大的元素排序（快速消除远距离乱序），
           逐渐缩小间隔，最终 gap=1 时等同于普通插入排序但数组已近有序。
    【复杂度】取决于间隔序列，一般为 O(n^1.3) 到 O(n^1.5)；空间 O(1)
    【稳定性】不稳定
    """
    arr = arr[:]
    n = len(arr)
    gap = n // 2  # 初始间隔

    while gap > 0:
        # 对每个间隔为 gap 的子序列执行插入排序
        for i in range(gap, n):
            key = arr[i]
            j = i - gap
            while j >= 0 and arr[j] > key:
                arr[j + gap] = arr[j]
                j -= gap
            arr[j + gap] = key
        gap //= 2

    return arr


# ------------------------------------------------------------
# 5. 归并排序（Merge Sort）
# ------------------------------------------------------------

def merge_sort(arr: List[int]) -> List[int]:
    """
    【思路】分治：将数组一分为二，分别排序后合并。
           合并两个有序数组：双指针，O(n) 时间。
    【复杂度】时间 O(n log n) 最坏/平均/最好；空间 O(n)（需要辅助数组）
    【稳定性】稳定
    【应用】链表排序（不需要随机访问）、外部排序（数据量超过内存时）
    """
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)


def _merge(left: List[int], right: List[int]) -> List[int]:
    """合并两个有序数组"""
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:  # <= 保证稳定性（相等时先取左边）
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def count_inversions(arr: List[int]) -> int:
    """
    【扩展】归并排序统计逆序对数量
    逆序对：i < j 但 arr[i] > arr[j]
    【思路】在归并的过程中，当右侧元素被先取出时，它比左侧剩余所有元素都小，
           逆序对数 += 左侧剩余元素个数。
    """
    count = [0]

    def sort_and_count(arr):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = sort_and_count(arr[:mid])
        right = sort_and_count(arr[mid:])
        return merge_count(left, right)

    def merge_count(left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
                # right[j] 比 left[i..] 的所有元素都小
                count[0] += len(left) - i
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    sort_and_count(arr)
    return count[0]


# ------------------------------------------------------------
# 6. 快速排序（Quick Sort）
# ------------------------------------------------------------

def quick_sort(arr: List[int]) -> List[int]:
    """
    【思路】分治：选一个基准（pivot），将数组分为"小于pivot"和"大于pivot"两部分，
           递归排序两部分。
    【复杂度】时间 O(n log n) 平均，O(n²) 最坏（有序数组+固定pivot）；空间 O(log n)
    【稳定性】不稳定
    【优化】随机选 pivot 避免最坏情况；三路划分处理大量重复元素
    """
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]  # 取中间元素为 pivot
    left = [x for x in arr if x < pivot]
    mid = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + mid + quick_sort(right)


def quick_sort_inplace(arr: List[int], low: int = None, high: int = None):
    """
    快速排序（原地版）：空间 O(log n)（递归栈深度）。
    使用随机化 pivot 避免最坏情况。
    """
    if low is None:
        low, high = 0, len(arr) - 1

    if low < high:
        # 随机选 pivot，与末尾交换
        pivot_idx = random.randint(low, high)
        arr[pivot_idx], arr[high] = arr[high], arr[pivot_idx]
        # 划分
        p = _partition(arr, low, high)
        quick_sort_inplace(arr, low, p - 1)
        quick_sort_inplace(arr, p + 1, high)


def _partition(arr: List[int], low: int, high: int) -> int:
    """
    Lomuto 划分：以 arr[high] 为 pivot。
    维护 i（小于 pivot 的区域末尾），j 向前扫描。
    """
    pivot = arr[high]
    i = low - 1  # 指向小于 pivot 区域的末尾
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def three_way_partition(arr: List[int], low: int, high: int):
    """
    三路划分（荷兰国旗问题）：将数组分为 <pivot、=pivot、>pivot 三部分。
    适合处理大量重复元素（避免退化）。
    返回 (lt, gt)：arr[lt..gt] 全等于 pivot
    """
    pivot = arr[low]
    lt = low       # arr[low..lt-1] < pivot
    gt = high      # arr[gt+1..high] > pivot
    i = low + 1    # 当前处理的元素

    while i <= gt:
        if arr[i] < pivot:
            arr[lt], arr[i] = arr[i], arr[lt]
            lt += 1
            i += 1
        elif arr[i] > pivot:
            arr[gt], arr[i] = arr[i], arr[gt]
            gt -= 1  # i 不前进：新换来的元素还未检查
        else:
            i += 1

    return lt, gt


# ------------------------------------------------------------
# 7. 堆排序（Heap Sort）
# ------------------------------------------------------------

def heap_sort(arr: List[int]) -> List[int]:
    """
    【思路】先建最大堆，再反复将堆顶（最大值）移到末尾并重新堆化。
    【复杂度】时间 O(n log n) 最坏/平均/最好；空间 O(1)
    【稳定性】不稳定
    """
    arr = arr[:]
    n = len(arr)

    def sift_down(root, size):
        """下沉操作：维护堆性质"""
        while True:
            largest = root
            left, right = 2 * root + 1, 2 * root + 2
            if left < size and arr[left] > arr[largest]:
                largest = left
            if right < size and arr[right] > arr[largest]:
                largest = right
            if largest == root:
                break
            arr[root], arr[largest] = arr[largest], arr[root]
            root = largest

    # 建堆：从最后一个非叶节点开始下沉，O(n)
    for i in range(n // 2 - 1, -1, -1):
        sift_down(i, n)

    # 排序：反复将堆顶（最大值）移到末尾
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]  # 堆顶与末尾交换
        sift_down(0, i)                   # 重新堆化（范围缩小）

    return arr


# ------------------------------------------------------------
# 8. 计数排序（Counting Sort）
# ------------------------------------------------------------

def counting_sort(arr: List[int]) -> List[int]:
    """
    【思路】统计每个值出现的次数，根据计数重建有序数组。
    【复杂度】时间 O(n+k)，k 为值域大小；空间 O(k)
    【限制】只适用于整数，且值域不能太大
    【稳定性】稳定（倒序填充保证稳定性）
    """
    if not arr:
        return []

    min_val, max_val = min(arr), max(arr)
    k = max_val - min_val + 1
    count = [0] * k

    for num in arr:
        count[num - min_val] += 1

    # 前缀和：count[i] 变为 "值 ≤ min_val+i 的元素个数"
    for i in range(1, k):
        count[i] += count[i - 1]

    # 倒序填充，保证稳定性
    result = [0] * len(arr)
    for num in reversed(arr):
        count[num - min_val] -= 1
        result[count[num - min_val]] = num

    return result


# ------------------------------------------------------------
# 9. 桶排序（Bucket Sort）
# ------------------------------------------------------------

def bucket_sort(arr: List[float]) -> List[float]:
    """
    【思路】将数据分到若干个桶中，对每个桶内部排序，再合并。
    【适用】数据均匀分布在某区间内时效果最好（平均 O(n)）。
    【复杂度】时间 O(n+k) 平均，O(n²) 最坏（所有元素落入同一桶）
    """
    if not arr:
        return []

    min_val, max_val = min(arr), max(arr)
    if min_val == max_val:
        return arr[:]

    n = len(arr)
    # 创建 n 个桶
    buckets = [[] for _ in range(n)]

    # 将每个元素映射到对应桶
    for num in arr:
        idx = int((num - min_val) / (max_val - min_val) * (n - 1))
        buckets[idx].append(num)

    # 对每个桶内部排序（这里用 Python 内置排序，也可用插入排序）
    result = []
    for bucket in buckets:
        result.extend(sorted(bucket))

    return result


# ------------------------------------------------------------
# 10. 基数排序（Radix Sort）
# ------------------------------------------------------------

def radix_sort(arr: List[int]) -> List[int]:
    """
    【思路】从最低位到最高位，对每一位进行稳定的计数排序。
           利用低位排序先稳定，高位排序后决定，最终得到完整有序序列。
    【复杂度】时间 O(d*(n+k))，d 为最大数字位数，k 为基数（10）；空间 O(n+k)
    【稳定性】稳定（基于稳定计数排序）
    """
    if not arr:
        return []

    max_val = max(arr)
    exp = 1  # 当前处理的位（个位、十位、百位……）

    arr = arr[:]
    while max_val // exp > 0:
        arr = _counting_sort_by_digit(arr, exp)
        exp *= 10

    return arr


def _counting_sort_by_digit(arr: List[int], exp: int) -> List[int]:
    """按 exp 位（个位/十位/百位）进行稳定计数排序"""
    n = len(arr)
    output = [0] * n
    count = [0] * 10  # 0-9 共10个桶

    for num in arr:
        digit = (num // exp) % 10
        count[digit] += 1

    # 前缀和
    for i in range(1, 10):
        count[i] += count[i - 1]

    # 倒序填充（保证稳定性）
    for num in reversed(arr):
        digit = (num // exp) % 10
        count[digit] -= 1
        output[count[digit]] = num

    return output


# ------------------------------------------------------------
# 11. 排序算法性能对比
# ------------------------------------------------------------

def sort_comparison():
    """生成随机数组，对比各算法运行时间"""
    import time
    test_arr = [random.randint(0, 10000) for _ in range(5000)]

    algorithms = [
        ("冒泡排序", bubble_sort),
        ("选择排序", selection_sort),
        ("插入排序", insertion_sort),
        ("希尔排序", shell_sort),
        ("归并排序", merge_sort),
        ("快速排序", quick_sort),
        ("堆排序",   heap_sort),
    ]

    print(f"数组大小: {len(test_arr)}")
    for name, func in algorithms:
        start = time.time()
        result = func(test_arr[:])
        elapsed = (time.time() - start) * 1000
        ok = "OK" if result == sorted(test_arr) else "FAIL"
        print(f"  {name:10s}: {elapsed:.2f} ms  验证: {ok}")


# ------------------------------------------------------------
# 主程序演示
# ------------------------------------------------------------

if __name__ == "__main__":
    test = [64, 34, 25, 12, 22, 11, 90, 1, 55, 43]
    print("原始数组:", test)
    print()

    print("冒泡排序:", bubble_sort(test))
    print("选择排序:", selection_sort(test))
    print("插入排序:", insertion_sort(test))
    print("希尔排序:", shell_sort(test))
    print("归并排序:", merge_sort(test))
    print("快速排序:", quick_sort(test))
    print("堆排序:  ", heap_sort(test))
    print("计数排序:", counting_sort(test))
    print("基数排序:", radix_sort(test))

    arr_inplace = test[:]
    quick_sort_inplace(arr_inplace)
    print("快排原地:", arr_inplace)

    print("\n逆序对统计")
    print(f"[2,4,1,3,5] 逆序对数: {count_inversions([2,4,1,3,5])}")

    print("\n排序性能对比")
    sort_comparison()
