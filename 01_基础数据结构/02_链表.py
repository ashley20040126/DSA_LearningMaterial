# ============================================================
# 数据结构与算法 - 第二章：链表
# ============================================================
# 链表是由节点组成的线性结构，每个节点存储数据和指向下一节点的引用。
# 与数组相比：插入/删除 O(1)（已知位置），随机访问 O(n)。
# ============================================================

from typing import Optional


# ------------------------------------------------------------
# 1. 链表节点定义
# ------------------------------------------------------------

class ListNode:
    """单链表节点"""
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next  # 指向下一个节点的引用


class DoublyListNode:
    """双向链表节点（可向前/向后访问）"""
    def __init__(self, val=0, prev=None, next=None):
        self.val = val
        self.prev = prev  # 指向前一个节点
        self.next = next  # 指向后一个节点


# ------------------------------------------------------------
# 2. 单链表实现
# ------------------------------------------------------------

class LinkedList:
    """单链表完整实现"""

    def __init__(self):
        # 使用哑节点（dummy head）简化边界处理，避免单独处理头节点为空的情况
        self.dummy = ListNode(0)
        self.size = 0

    def _get_node(self, index: int) -> ListNode:
        """获取第 index 个节点，O(n)"""
        node = self.dummy.next
        for _ in range(index):
            node = node.next
        return node

    def append(self, val: int):
        """在末尾追加节点，O(n)"""
        node = self.dummy
        while node.next:
            node = node.next
        node.next = ListNode(val)
        self.size += 1

    def prepend(self, val: int):
        """在头部插入节点，O(1)"""
        new_node = ListNode(val)
        new_node.next = self.dummy.next
        self.dummy.next = new_node
        self.size += 1

    def insert(self, index: int, val: int):
        """在 index 位置插入节点，O(n)"""
        if index < 0 or index > self.size:
            raise IndexError("下标越界")
        # 找到 index-1 位置的节点（前驱节点）
        prev = self.dummy
        for _ in range(index):
            prev = prev.next
        new_node = ListNode(val)
        new_node.next = prev.next  # 新节点指向原 index 位置的节点
        prev.next = new_node        # 前驱节点指向新节点
        self.size += 1

    def delete(self, index: int) -> int:
        """删除 index 位置的节点并返回其值，O(n)"""
        if index < 0 or index >= self.size:
            raise IndexError("下标越界")
        prev = self.dummy
        for _ in range(index):
            prev = prev.next
        # 绕过要删除的节点
        deleted = prev.next
        prev.next = deleted.next
        self.size -= 1
        return deleted.val

    def to_list(self) -> list:
        """将链表转为 Python 列表（方便打印）"""
        result = []
        node = self.dummy.next
        while node:
            result.append(node.val)
            node = node.next
        return result


# ------------------------------------------------------------
# 3. 链表辅助函数（将列表转为链表）
# ------------------------------------------------------------

def list_to_linkedlist(arr: list) -> Optional[ListNode]:
    """将 Python 列表转换为链表，返回头节点"""
    if not arr:
        return None
    dummy = ListNode(0)
    cur = dummy
    for val in arr:
        cur.next = ListNode(val)
        cur = cur.next
    return dummy.next


def linkedlist_to_list(head: Optional[ListNode]) -> list:
    """将链表转换为 Python 列表"""
    result = []
    while head:
        result.append(head.val)
        head = head.next
    return result


# ------------------------------------------------------------
# 4. 链表经典算法题
# ------------------------------------------------------------

def reverse_list(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    【题型】反转单链表
    【思路】迭代：用三个指针 prev/cur/next，逐个反转指针方向。
    【复杂度】时间 O(n)，空间 O(1)
    """
    prev = None
    cur = head
    while cur:
        next_node = cur.next  # 先保存下一个节点（防止断链后找不到）
        cur.next = prev       # 反转当前节点的指针
        prev = cur            # prev 前进
        cur = next_node       # cur 前进
    return prev  # prev 最终指向新的头节点


def reverse_list_recursive(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    【题型】反转单链表（递归版）
    【思路】递归到最后一个节点，再从后往前逐个反转。
    【复杂度】时间 O(n)，空间 O(n)（递归栈）
    """
    if not head or not head.next:
        return head
    # 假设 head.next 之后的部分已经反转好，new_head 是新的头
    new_head = reverse_list_recursive(head.next)
    # 让 head.next 的 next 指回 head（反转这一步的连接）
    head.next.next = head
    head.next = None  # head 变成了新的末尾，next 置 None
    return new_head


def has_cycle(head: Optional[ListNode]) -> bool:
    """
    【题型】判断链表是否有环
    【思路】Floyd 快慢指针：慢指针每次走1步，快指针每次走2步。
           若有环，快指针一定会追上慢指针（在环内相遇）。
    【复杂度】时间 O(n)，空间 O(1)
    """
    slow = fast = head
    while fast and fast.next:
        slow = slow.next        # 慢指针：每次走1步
        fast = fast.next.next  # 快指针：每次走2步
        if slow == fast:
            return True  # 相遇，说明有环
    return False


def detect_cycle(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    【题型】找环的入口节点
    【思路】Floyd 算法扩展：
           1. 快慢指针找到相遇点
           2. 将一个指针重置到 head，两个指针都以步长1前进
           3. 再次相遇时即为环的入口
    【数学推导】设链表头到环入口距离为 a，环入口到相遇点为 b，
              环剩余长度为 c。相遇时：慢指针走了 a+b，
              快指针走了 a+b+k*(b+c)=2(a+b)，化简得 a = k*(b+c)-b。
              所以从 head 和相遇点同步走 a 步后恰好在入口汇合。
    """
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            # 找到相遇点，重置一个指针到头
            pointer = head
            while pointer != slow:
                pointer = pointer.next
                slow = slow.next
            return slow  # 环的入口
    return None


def find_middle(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    【题型】找链表中间节点
    【思路】快慢指针：慢指针走1步，快指针走2步，快指针到末尾时慢指针在中间。
           偶数长度链表返回第二个中间节点。
    【复杂度】时间 O(n)，空间 O(1)
    """
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow


def merge_two_sorted_lists(l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
    """
    【题型】合并两个有序链表
    【思路】用哑节点作为新链表的起始，比较两链表当前节点值，逐个接入较小的节点。
    【复杂度】时间 O(m+n)，空间 O(1)
    """
    dummy = ListNode(0)  # 哑节点，避免处理空头节点的边界情况
    cur = dummy

    while l1 and l2:
        if l1.val <= l2.val:
            cur.next = l1
            l1 = l1.next
        else:
            cur.next = l2
            l2 = l2.next
        cur = cur.next

    # 将剩余的链表直接接上（剩余部分本身已有序）
    cur.next = l1 if l1 else l2
    return dummy.next


def remove_nth_from_end(head: Optional[ListNode], n: int) -> Optional[ListNode]:
    """
    【题型】删除链表倒数第 n 个节点
    【思路】双指针：fast 先走 n 步，然后 fast 和 slow 同步前进，
           fast 到末尾时 slow 刚好在倒数第 n+1 个节点（前驱节点）。
    【复杂度】时间 O(L)，空间 O(1)，一次遍历完成
    """
    dummy = ListNode(0)
    dummy.next = head
    fast = slow = dummy

    # fast 先走 n+1 步（多走一步是为了让 slow 停在目标节点的前驱）
    for _ in range(n + 1):
        fast = fast.next

    # fast 和 slow 同步前进
    while fast:
        fast = fast.next
        slow = slow.next

    # slow 现在在倒数第 n 个节点的前驱，执行删除
    slow.next = slow.next.next
    return dummy.next


def merge_k_lists(lists: list) -> Optional[ListNode]:
    """
    【题型】合并 K 个有序链表
    【思路】分治法：两两合并，每轮处理数量减半。
    【复杂度】时间 O(N log k)，N 为总节点数，k 为链表个数
    """
    if not lists:
        return None

    def merge_two(l1, l2):
        dummy = ListNode(0)
        cur = dummy
        while l1 and l2:
            if l1.val <= l2.val:
                cur.next, l1 = l1, l1.next
            else:
                cur.next, l2 = l2, l2.next
            cur = cur.next
        cur.next = l1 or l2
        return dummy.next

    # 分治：每轮将 lists 中相邻两个链表合并
    while len(lists) > 1:
        merged = []
        for i in range(0, len(lists), 2):
            l1 = lists[i]
            l2 = lists[i + 1] if i + 1 < len(lists) else None
            merged.append(merge_two(l1, l2))
        lists = merged

    return lists[0]


def reverse_between(head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:
    """
    【题型】反转链表中第 left 到 right 位置的节点
    【思路】头插法：在 [left, right] 范围内，每次将 cur.next 插入到 pre.next 的位置。
    【复杂度】时间 O(n)，空间 O(1)
    """
    dummy = ListNode(0)
    dummy.next = head
    pre = dummy  # pre 始终在反转区间的前一个节点

    # 将 pre 移动到 left 的前一个节点
    for _ in range(left - 1):
        pre = pre.next

    cur = pre.next  # cur 是反转区间的第一个节点

    # 头插法：将 cur.next 反复插到 pre.next 位置
    for _ in range(right - left):
        next_node = cur.next
        cur.next = next_node.next   # cur 跳过 next_node
        next_node.next = pre.next   # next_node 指向当前的反转头
        pre.next = next_node        # pre.next 更新为 next_node（新的反转头）

    return dummy.next


# ------------------------------------------------------------
# 5. LRU 缓存（链表 + 哈希表的综合应用）
# ------------------------------------------------------------

class LRUCache:
    """
    LRU（最近最少使用）缓存，要求 get/put 均为 O(1)。
    【数据结构】双向链表 + 哈希表
    - 双向链表维护访问顺序（头部最近，尾部最久未用）
    - 哈希表实现 O(1) 查找
    """

    class _Node:
        def __init__(self, key=0, val=0):
            self.key = key
            self.val = val
            self.prev = self.next = None

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # key -> Node

        # 使用哑头和哑尾节点，避免处理边界空指针
        self.head = self._Node()  # 哑头（最近使用的一侧）
        self.tail = self._Node()  # 哑尾（最久未用的一侧）
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        """从双向链表中移除节点"""
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_front(self, node):
        """将节点添加到链表头部（表示最近使用）"""
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._remove(node)         # 从当前位置移除
        self._add_to_front(node)   # 移到链表头部（标记为最近使用）
        return node.val

    def put(self, key: int, value: int):
        if key in self.cache:
            node = self.cache[key]
            node.val = value
            self._remove(node)
            self._add_to_front(node)
        else:
            if len(self.cache) >= self.capacity:
                # 淘汰最久未用的节点（链表尾部的前一个节点）
                lru = self.tail.prev
                self._remove(lru)
                del self.cache[lru.key]
            new_node = self._Node(key, value)
            self.cache[key] = new_node
            self._add_to_front(new_node)


# ------------------------------------------------------------
# 主程序演示
# ------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 50)
    print("1. 链表基本操作")
    ll = LinkedList()
    for v in [1, 2, 3, 4, 5]:
        ll.append(v)
    print(f"初始链表: {ll.to_list()}")
    ll.prepend(0)
    print(f"头部插入0: {ll.to_list()}")
    ll.delete(0)
    print(f"删除头部: {ll.to_list()}")

    print("\n2. 反转链表")
    head = list_to_linkedlist([1, 2, 3, 4, 5])
    reversed_head = reverse_list(head)
    print(f"反转结果: {linkedlist_to_list(reversed_head)}")

    print("\n3. 合并两个有序链表")
    l1 = list_to_linkedlist([1, 2, 4])
    l2 = list_to_linkedlist([1, 3, 4])
    merged = merge_two_sorted_lists(l1, l2)
    print(f"合并结果: {linkedlist_to_list(merged)}")

    print("\n4. 删除倒数第N个节点")
    head = list_to_linkedlist([1, 2, 3, 4, 5])
    result = remove_nth_from_end(head, 2)
    print(f"删除倒数第2个: {linkedlist_to_list(result)}")

    print("\n5. 反转区间 [2,4]")
    head = list_to_linkedlist([1, 2, 3, 4, 5])
    result = reverse_between(head, 2, 4)
    print(f"反转结果: {linkedlist_to_list(result)}")

    print("\n6. LRU 缓存")
    lru = LRUCache(2)
    lru.put(1, 1)
    lru.put(2, 2)
    print(f"get(1): {lru.get(1)}")   # 返回 1
    lru.put(3, 3)                     # 淘汰 key=2
    print(f"get(2): {lru.get(2)}")   # 返回 -1（已淘汰）
    print(f"get(3): {lru.get(3)}")   # 返回 3

    print("\n7. 合并K个有序链表")
    lists = [list_to_linkedlist([1, 4, 5]),
             list_to_linkedlist([1, 3, 4]),
             list_to_linkedlist([2, 6])]
    result = merge_k_lists(lists)
    print(f"合并结果: {linkedlist_to_list(result)}")
