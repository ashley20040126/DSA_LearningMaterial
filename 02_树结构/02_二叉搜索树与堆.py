# ============================================================
# 数据结构与算法 - 第六章：二叉搜索树 & 堆
# ============================================================
# BST：左子树所有值 < 根 < 右子树所有值，中序遍历有序。
# 堆：完全二叉树，父节点 ≥（最大堆）或 ≤（最小堆）所有子节点。
# ============================================================

from typing import Optional, List
import heapq
from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ------------------------------------------------------------
# 1. 二叉搜索树（BST）完整实现
# ------------------------------------------------------------

class BST:
    """
    二叉搜索树实现。
    - 查找/插入/删除平均 O(log n)，最坏（退化为链表）O(n)。
    - 中序遍历结果有序，是 BST 的核心性质。
    """

    def __init__(self):
        self.root = None

    def insert(self, val: int):
        """插入值：递归找到正确的位置插入"""
        def _insert(node, val):
            if not node:
                return TreeNode(val)
            if val < node.val:
                node.left = _insert(node.left, val)
            elif val > node.val:
                node.right = _insert(node.right, val)
            # val == node.val：BST 通常不插入重复值
            return node
        self.root = _insert(self.root, val)

    def search(self, val: int) -> bool:
        """查找值：利用 BST 性质快速定位"""
        def _search(node, val):
            if not node:
                return False
            if val == node.val:
                return True
            elif val < node.val:
                return _search(node.left, val)
            else:
                return _search(node.right, val)
        return _search(self.root, val)

    def delete(self, val: int):
        """
        删除节点，三种情况：
        1. 叶节点：直接删除
        2. 只有一个子节点：用子节点替代
        3. 有两个子节点：用右子树最小节点（后继）替代，再删除后继
        """
        def _get_min(node):
            while node.left:
                node = node.left
            return node

        def _delete(node, val):
            if not node:
                return None
            if val < node.val:
                node.left = _delete(node.left, val)
            elif val > node.val:
                node.right = _delete(node.right, val)
            else:
                # 找到要删除的节点
                if not node.left:
                    return node.right  # 无左子，用右子替代
                if not node.right:
                    return node.left   # 无右子，用左子替代
                # 两个子节点：找右子树的最小值（后继）
                successor = _get_min(node.right)
                node.val = successor.val          # 用后继值覆盖当前节点
                node.right = _delete(node.right, successor.val)  # 删除后继
            return node

        self.root = _delete(self.root, val)

    def inorder(self) -> List[int]:
        """中序遍历（有序输出）"""
        result = []
        def _inorder(node):
            if node:
                _inorder(node.left)
                result.append(node.val)
                _inorder(node.right)
        _inorder(self.root)
        return result


# ------------------------------------------------------------
# 2. BST 经典题型
# ------------------------------------------------------------

def is_valid_bst(root: Optional[TreeNode]) -> bool:
    """
    【题型】验证二叉搜索树
    【思路】中序遍历结果应严格递增；或用上下界递归验证。
           递归时传递合法值范围 (min_val, max_val)。
    【注意】不能只比较父子节点，要确保整棵子树满足约束。
    """
    def validate(node, min_val, max_val):
        if not node:
            return True
        if not (min_val < node.val < max_val):
            return False
        return (validate(node.left, min_val, node.val) and
                validate(node.right, node.val, max_val))

    return validate(root, float('-inf'), float('inf'))


def kth_smallest(root: Optional[TreeNode], k: int) -> int:
    """
    【题型】BST 中第 K 小的元素
    【思路】中序遍历到第 k 个即为答案（中序有序）。
    """
    count = 0
    result = None

    def inorder(node):
        nonlocal count, result
        if not node or result is not None:
            return
        inorder(node.left)
        count += 1
        if count == k:
            result = node.val
            return
        inorder(node.right)

    inorder(root)
    return result


def lowest_common_ancestor_bst(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    """
    【题型】BST 的最近公共祖先
    【思路】利用 BST 性质：
           - p,q 都在左子树：往左走
           - p,q 都在右子树：往右走
           - 否则当前节点就是 LCA
    """
    while root:
        if p.val < root.val and q.val < root.val:
            root = root.left
        elif p.val > root.val and q.val > root.val:
            root = root.right
        else:
            return root
    return root


def lowest_common_ancestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    """
    【题型】普通二叉树的最近公共祖先
    【思路】后序遍历：
           - 若左子树含 p 或 q，返回对应节点
           - 若右子树含 p 或 q，同上
           - 若左右均非空，当前节点就是 LCA
    """
    if not root or root == p or root == q:
        return root
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    if left and right:
        return root  # p 和 q 分属两侧，当前节点是 LCA
    return left or right  # 只有一侧有结果，返回那侧


def sorted_array_to_bst(nums: List[int]) -> Optional[TreeNode]:
    """
    【题型】有序数组转为高度平衡的 BST
    【思路】取中间元素为根（保证高度平衡），递归构造左右子树。
    """
    if not nums:
        return None
    mid = len(nums) // 2
    root = TreeNode(nums[mid])
    root.left = sorted_array_to_bst(nums[:mid])
    root.right = sorted_array_to_bst(nums[mid + 1:])
    return root


def recover_bst(root: Optional[TreeNode]):
    """
    【题型】恢复二叉搜索树（有两个节点被错误交换）
    【思路】中序遍历时，正常序列应严格递增。
           找到两处"逆序对"：
           - 第一处逆序对的较大节点是第一个错误节点
           - 最后一处逆序对的较小节点是第二个错误节点
           最后交换两者的值。
    """
    first = second = prev = None

    def inorder(node):
        nonlocal first, second, prev
        if not node:
            return
        inorder(node.left)
        if prev and prev.val > node.val:
            if not first:
                first = prev  # 第一个错误节点（逆序对中较大的那个）
            second = node     # 第二个错误节点（逆序对中较小的那个，持续更新）
        prev = node
        inorder(node.right)

    inorder(root)
    if first and second:
        first.val, second.val = second.val, first.val  # 交换值即可


# ------------------------------------------------------------
# 3. 堆（Heap）实现与应用
# ------------------------------------------------------------

class MaxHeap:
    """
    手写最大堆（用数组实现）。
    堆的存储：parent(i) = (i-1)//2，left(i) = 2i+1，right(i) = 2i+2。
    核心操作：上浮（sift_up）和下沉（sift_down）。
    """

    def __init__(self):
        self.data = []

    def push(self, val: int):
        """插入元素：先放到末尾，再上浮"""
        self.data.append(val)
        self._sift_up(len(self.data) - 1)

    def pop(self) -> int:
        """弹出最大值：将末尾元素移到堆顶，再下沉"""
        if not self.data:
            raise IndexError("堆为空")
        # 将最大值（堆顶）与末尾互换，弹出末尾
        self.data[0], self.data[-1] = self.data[-1], self.data[0]
        max_val = self.data.pop()
        if self.data:
            self._sift_down(0)
        return max_val

    def peek(self) -> int:
        return self.data[0]

    def _sift_up(self, i: int):
        """上浮：子节点比父节点大时，与父节点交换"""
        while i > 0:
            parent = (i - 1) // 2
            if self.data[i] > self.data[parent]:
                self.data[i], self.data[parent] = self.data[parent], self.data[i]
                i = parent
            else:
                break

    def _sift_down(self, i: int):
        """下沉：父节点比子节点小时，与较大子节点交换"""
        n = len(self.data)
        while True:
            largest = i
            left, right = 2 * i + 1, 2 * i + 2
            if left < n and self.data[left] > self.data[largest]:
                largest = left
            if right < n and self.data[right] > self.data[largest]:
                largest = right
            if largest == i:
                break  # 当前节点已是最大，停止
            self.data[i], self.data[largest] = self.data[largest], self.data[i]
            i = largest

    @staticmethod
    def heapify(arr: list) -> 'MaxHeap':
        """
        将任意数组原地建堆，时间复杂度 O(n)（比逐个 push 的 O(n log n) 更快）。
        从最后一个非叶节点开始，向前依次下沉。
        """
        heap = MaxHeap()
        heap.data = arr[:]
        n = len(heap.data)
        # 最后一个非叶节点下标为 n//2 - 1
        for i in range(n // 2 - 1, -1, -1):
            heap._sift_down(i)
        return heap


# ------------------------------------------------------------
# 4. 堆的经典应用
# ------------------------------------------------------------

def find_kth_largest(nums: List[int], k: int) -> int:
    """
    【题型】第 K 大的元素
    【思路】维护大小为 k 的最小堆：堆顶始终是当前最小的 top-k 元素。
    【复杂度】时间 O(n log k)，空间 O(k)
    """
    min_heap = []
    for num in nums:
        heapq.heappush(min_heap, num)
        if len(min_heap) > k:
            heapq.heappop(min_heap)
    return min_heap[0]  # 堆顶即第 k 大


def merge_k_sorted_arrays(arrays: List[List[int]]) -> List[int]:
    """
    【题型】合并 K 个有序数组
    【思路】最小堆：初始将每个数组的第一个元素入堆（含数组编号和元素下标）。
           每次弹出最小元素后，将该元素所在数组的下一个元素入堆。
    【复杂度】时间 O(N log k)，N 为总元素数
    """
    result = []
    # 堆元素：(值, 数组下标, 元素下标)
    heap = [(arr[0], i, 0) for i, arr in enumerate(arrays) if arr]
    heapq.heapify(heap)

    while heap:
        val, arr_idx, elem_idx = heapq.heappop(heap)
        result.append(val)
        if elem_idx + 1 < len(arrays[arr_idx]):
            heapq.heappush(heap, (arrays[arr_idx][elem_idx + 1], arr_idx, elem_idx + 1))

    return result


class MedianFinder:
    """
    【题型】数据流的中位数
    【思路】双堆法：
           - max_heap（最大堆）存较小的一半，堆顶是较小半部分的最大值
           - min_heap（最小堆）存较大的一半，堆顶是较大半部分的最小值
           - 保持两堆大小差 ≤ 1，且 max_heap.top ≤ min_heap.top
           - 中位数 = 两堆顶的均值（或元素多的那堆的堆顶）
    """

    def __init__(self):
        self.max_heap = []  # 小值堆（Python 最小堆，存负数模拟最大堆）
        self.min_heap = []  # 大值堆（Python 最小堆）

    def add_num(self, num: int):
        # 先放入最大堆（小值区）
        heapq.heappush(self.max_heap, -num)
        # 保证 max_heap 的最大值 ≤ min_heap 的最小值
        heapq.heappush(self.min_heap, -heapq.heappop(self.max_heap))
        # 维持 max_heap 元素个数 ≥ min_heap（中位数偏向 max_heap）
        if len(self.min_heap) > len(self.max_heap):
            heapq.heappush(self.max_heap, -heapq.heappop(self.min_heap))

    def find_median(self) -> float:
        if len(self.max_heap) > len(self.min_heap):
            return -self.max_heap[0]  # 奇数个，中位数是 max_heap 的堆顶
        return (-self.max_heap[0] + self.min_heap[0]) / 2  # 偶数个，取均值


# ------------------------------------------------------------
# 主程序演示
# ------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 50)
    print("1. BST 基本操作")
    bst = BST()
    for v in [5, 3, 7, 1, 4, 6, 8]:
        bst.insert(v)
    print(f"  中序遍历（应有序）: {bst.inorder()}")
    bst.delete(3)
    print(f"  删除3后: {bst.inorder()}")
    print(f"  查找4: {bst.search(4)}, 查找3: {bst.search(3)}")

    print("\n2. 第K小元素")
    root = bst.root
    # 手动建个 BST 测试
    bst2 = BST()
    for v in [5, 3, 6, 2, 4]:
        bst2.insert(v)
    print(f"  [5,3,6,2,4] 第3小: {kth_smallest(bst2.root, 3)}")

    print("\n3. 有序数组转 BST")
    sorted_arr = [1, 2, 3, 4, 5, 6, 7]
    bst_root = sorted_array_to_bst(sorted_arr)
    # 简单验证：中序应得回原数组
    bst3 = BST()
    bst3.root = bst_root
    print(f"  中序遍历验证: {bst3.inorder()}")

    print("\n4. 最大堆操作")
    heap = MaxHeap()
    for v in [3, 1, 4, 1, 5, 9, 2, 6]:
        heap.push(v)
    print(f"  堆顶（最大值）: {heap.peek()}")
    print(f"  依次弹出: ", end="")
    while heap.data:
        print(heap.pop(), end=" ")
    print()

    print("\n5. 第K大元素")
    print(f"  [3,2,1,5,6,4] 第2大: {find_kth_largest([3,2,1,5,6,4], 2)}")

    print("\n6. 合并K个有序数组")
    arrays = [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
    print(f"  合并结果: {merge_k_sorted_arrays(arrays)}")

    print("\n7. 数据流中位数")
    mf = MedianFinder()
    for num in [1, 2, 3, 4, 5]:
        mf.add_num(num)
        print(f"  加入{num}后中位数: {mf.find_median()}")
