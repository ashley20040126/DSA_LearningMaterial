# ============================================================
# 数据结构与算法 - 第三章：栈与队列
# ============================================================
# 栈：后进先出（LIFO）。只在一端（栈顶）进行插入和删除。
# 队列：先进先出（FIFO）。在一端插入（队尾），另一端删除（队头）。
# 两者都是线性数据结构，核心操作均为 O(1)。
# ============================================================

from collections import deque
import heapq


# ------------------------------------------------------------
# 1. 栈的实现与基本操作
# ------------------------------------------------------------

class Stack:
    """
    用 Python 列表实现栈。
    列表尾部 = 栈顶，append/pop 均为 O(1)（摊销）。
    """
    def __init__(self):
        self._data = []

    def push(self, val):
        self._data.append(val)  # 入栈

    def pop(self):
        if self.is_empty():
            raise IndexError("栈为空")
        return self._data.pop()  # 出栈（弹出栈顶元素）

    def peek(self):
        """查看栈顶元素但不弹出"""
        if self.is_empty():
            raise IndexError("栈为空")
        return self._data[-1]

    def is_empty(self):
        return len(self._data) == 0

    def size(self):
        return len(self._data)


# ------------------------------------------------------------
# 2. 栈的经典应用
# ------------------------------------------------------------

def is_valid_parentheses(s: str) -> bool:
    """
    【题型】有效括号匹配
    【思路】遇到左括号入栈，遇到右括号弹出栈顶检查是否匹配。
    【复杂度】时间 O(n)，空间 O(n)
    """
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}  # 右括号 -> 对应左括号

    for char in s:
        if char in mapping:
            # 是右括号，弹出栈顶（栈空则用 '#' 占位）
            top = stack.pop() if stack else '#'
            if mapping[char] != top:
                return False
        else:
            # 是左括号，入栈
            stack.append(char)

    return not stack  # 栈为空则所有括号匹配成功


def daily_temperatures(temperatures: list) -> list:
    """
    【题型】每日温度——找下一个更大元素的距离
    【思路】单调递减栈：维护一个下标栈，栈内温度从底到顶单调递减。
           当遇到比栈顶更高的温度时，栈顶元素"找到了"它的答案。
    【复杂度】时间 O(n)，空间 O(n)
    """
    n = len(temperatures)
    result = [0] * n
    stack = []  # 存储下标，栈内对应温度单调递减

    for i, temp in enumerate(temperatures):
        # 当前温度大于栈顶温度，说明栈顶找到了"下一个更热的天"
        while stack and temperatures[stack[-1]] < temp:
            idx = stack.pop()
            result[idx] = i - idx  # 等待天数 = 当前下标 - 栈顶下标
        stack.append(i)

    return result


def largest_rectangle_in_histogram(heights: list) -> int:
    """
    【题型】柱状图中最大的矩形
    【思路】单调递增栈：当遇到比栈顶更小的高度时，弹出栈顶并计算以栈顶为高的最大矩形。
           矩形宽度 = 当前下标 - 栈顶前一个下标 - 1
    【复杂度】时间 O(n)，空间 O(n)
    """
    # 在两端加入哨兵 0，简化边界处理
    heights = [0] + heights + [0]
    stack = [0]  # 存储下标，栈内高度单调递增
    max_area = 0

    for i in range(1, len(heights)):
        # 遇到更小高度，弹出并计算面积
        while heights[i] < heights[stack[-1]]:
            h = heights[stack.pop()]  # 被弹出柱子的高度
            w = i - stack[-1] - 1    # 宽度：当前位置到新栈顶之间
            max_area = max(max_area, h * w)
        stack.append(i)

    return max_area


def min_stack():
    """
    【题型】最小栈——支持 O(1) 获取最小值的栈
    【思路】用辅助栈同步记录每个状态下的最小值。
           主栈每 push 一个元素，辅助栈也 push 当前最小值。
    """
    class MinStack:
        def __init__(self):
            self.stack = []
            self.min_stack = []  # 辅助栈，存当前最小值

        def push(self, val: int):
            self.stack.append(val)
            # 辅助栈记录：新最小值 = min(当前值, 已有最小值)
            if self.min_stack:
                self.min_stack.append(min(val, self.min_stack[-1]))
            else:
                self.min_stack.append(val)

        def pop(self):
            self.stack.pop()
            self.min_stack.pop()  # 同步弹出

        def top(self):
            return self.stack[-1]

        def get_min(self):
            return self.min_stack[-1]  # 辅助栈顶就是当前最小值

    return MinStack


def calculate(s: str) -> int:
    """
    【题型】基本计算器（含 +、-、括号，无 * /）
    【思路】用栈处理括号嵌套。遇到 '(' 将当前结果和符号入栈，
           遇到 ')' 将括号内结果与栈中上下文合并。
    【复杂度】时间 O(n)，空间 O(n)
    """
    stack = []
    result = 0
    sign = 1   # 当前数字前的符号（+1 或 -1）
    num = 0

    for char in s:
        if char.isdigit():
            num = num * 10 + int(char)  # 处理多位数
        elif char in '+-':
            result += sign * num  # 将前一个数加入结果
            num = 0
            sign = 1 if char == '+' else -1
        elif char == '(':
            # 将当前状态（已计算结果和括号前的符号）压栈
            stack.append(result)
            stack.append(sign)
            result = 0  # 重置，开始计算括号内的表达式
            sign = 1
        elif char == ')':
            result += sign * num  # 先把括号内最后的数加进去
            num = 0
            # 弹出括号外的符号和上下文结果
            result *= stack.pop()   # 乘以括号前的符号
            result += stack.pop()   # 加上括号前的累计结果

    result += sign * num  # 处理最后一个数
    return result


# ------------------------------------------------------------
# 3. 队列的实现
# ------------------------------------------------------------

class Queue:
    """
    用 deque（双端队列）实现队列。
    deque 的 appendleft/popleft 均为 O(1)（不像列表 insert(0) 是 O(n)）。
    """
    def __init__(self):
        self._data = deque()

    def enqueue(self, val):
        self._data.append(val)  # 从队尾入队

    def dequeue(self):
        if self.is_empty():
            raise IndexError("队列为空")
        return self._data.popleft()  # 从队头出队

    def front(self):
        return self._data[0]

    def is_empty(self):
        return len(self._data) == 0


# ------------------------------------------------------------
# 4. 用栈实现队列 / 用队列实现栈
# ------------------------------------------------------------

class MyQueue:
    """
    【题型】用两个栈实现队列
    【思路】栈1（输入栈）接收所有入队操作。
           出队时，若栈2（输出栈）为空，则将栈1所有元素倒入栈2，再从栈2弹出。
           摊销时间复杂度：每个元素最多移动一次，O(1)。
    """
    def __init__(self):
        self.in_stack = []   # 输入栈（接收 push）
        self.out_stack = []  # 输出栈（接收 pop/peek）

    def push(self, x: int):
        self.in_stack.append(x)

    def _transfer(self):
        """当输出栈为空时，将输入栈全部倒入输出栈"""
        if not self.out_stack:
            while self.in_stack:
                self.out_stack.append(self.in_stack.pop())

    def pop(self) -> int:
        self._transfer()
        return self.out_stack.pop()

    def peek(self) -> int:
        self._transfer()
        return self.out_stack[-1]

    def empty(self) -> bool:
        return not self.in_stack and not self.out_stack


class MyStack:
    """
    【题型】用两个队列实现栈
    【思路】push 时，先将新元素加入空队列，再将非空队列的所有元素移入，
           始终保持队列头部为栈顶。
    """
    def __init__(self):
        self.q1 = deque()  # 始终保持栈的顺序（新元素在最前）
        self.q2 = deque()  # 辅助队列

    def push(self, x: int):
        self.q2.append(x)
        # 将 q1 的所有元素排到新元素后面
        while self.q1:
            self.q2.append(self.q1.popleft())
        self.q1, self.q2 = self.q2, self.q1  # 交换引用

    def pop(self) -> int:
        return self.q1.popleft()

    def top(self) -> int:
        return self.q1[0]

    def empty(self) -> bool:
        return not self.q1


# ------------------------------------------------------------
# 5. 单调队列（滑动窗口最大值）
# ------------------------------------------------------------

def sliding_window_maximum(nums: list, k: int) -> list:
    """
    【题型】滑动窗口最大值
    【思路】单调递减双端队列（存下标）：
           - 入队时：从队尾移除所有比当前元素小的下标（它们不可能是未来的最大值）
           - 每次取队头（最大值下标），若队头下标已不在窗口内则移除
    【复杂度】时间 O(n)，空间 O(k)
    """
    if not nums or k == 0:
        return []

    dq = deque()   # 单调递减队列，存下标
    result = []

    for i in range(len(nums)):
        # 移除队尾所有比当前值小的下标（维护单调递减性）
        while dq and nums[dq[-1]] < nums[i]:
            dq.pop()

        dq.append(i)

        # 移除已不在窗口内的队头
        if dq[0] < i - k + 1:
            dq.popleft()

        # 窗口形成后才开始记录结果
        if i >= k - 1:
            result.append(nums[dq[0]])

    return result


# ------------------------------------------------------------
# 6. 优先队列（堆）
# ------------------------------------------------------------

def find_k_largest(nums: list, k: int) -> list:
    """
    【题型】找数组中最大的 K 个数
    【思路】用最小堆（大小为 k）：维护一个包含 k 个最大元素的小顶堆。
           新元素若比堆顶大，则替换堆顶并重新堆化。
    【复杂度】时间 O(n log k)，空间 O(k)
    """
    min_heap = []
    for num in nums:
        heapq.heappush(min_heap, num)
        if len(min_heap) > k:
            heapq.heappop(min_heap)  # 弹出最小值，保持堆大小为 k
    return sorted(min_heap, reverse=True)


def task_scheduler(tasks: list, n: int) -> int:
    """
    【题型】任务调度器（CPU 调度）
    【思路】优先队列（最大堆）+ 冷却队列：
           每次从堆中取出频率最高的任务执行，执行后放入冷却队列（n 轮后可再用）。
    【复杂度】时间 O(T log T)，T 为任务种类数
    """
    from collections import Counter

    # Python heapq 是最小堆，用负数模拟最大堆
    freq = Counter(tasks)
    max_heap = [-f for f in freq.values()]
    heapq.heapify(max_heap)

    time = 0
    cooldown = deque()  # (next_available_time, count) 冷却队列

    while max_heap or cooldown:
        time += 1
        if max_heap:
            cnt = heapq.heappop(max_heap) + 1  # 执行一次（负数加1）
            if cnt < 0:  # 还有剩余次数
                cooldown.append((time + n, cnt))  # n 轮后可再用

        # 将冷却结束的任务重新放回堆
        if cooldown and cooldown[0][0] == time:
            _, cnt = cooldown.popleft()
            heapq.heappush(max_heap, cnt)

    return time


# ------------------------------------------------------------
# 主程序演示
# ------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 50)
    print("1. 有效括号")
    tests = ["()", "()[]{}", "(]", "([)]", "{[]}"]
    for t in tests:
        print(f"  '{t}': {is_valid_parentheses(t)}")

    print("\n2. 每日温度")
    temps = [73, 74, 75, 71, 69, 72, 76, 73]
    print(f"  温度: {temps}")
    print(f"  等待: {daily_temperatures(temps)}")

    print("\n3. 柱状图最大矩形")
    heights = [2, 1, 5, 6, 2, 3]
    print(f"  高度: {heights}, 最大面积: {largest_rectangle_in_histogram(heights)}")

    print("\n4. 计算器")
    expr = "(1+(4+5+2)-3)+(6+8)"
    print(f"  '{expr}' = {calculate(expr)}")

    print("\n5. 两栈实现队列")
    q = MyQueue()
    q.push(1); q.push(2); q.push(3)
    print(f"  依次出队: {q.pop()}, {q.pop()}, {q.pop()}")

    print("\n6. 滑动窗口最大值")
    nums = [1, 3, -1, -3, 5, 3, 6, 7]
    print(f"  nums={nums}, k=3, 结果={sliding_window_maximum(nums, 3)}")

    print("\n7. 前K大元素")
    nums = [3, 2, 1, 5, 6, 4]
    print(f"  {nums} 中前3大: {find_k_largest(nums, 3)}")
