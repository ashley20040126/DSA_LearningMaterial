# ============================================================
# 数据结构与算法 - 第五章：二叉树基础
# ============================================================
# 二叉树：每个节点最多有两个子节点（左子树、右子树）。
# 核心操作：遍历（前序/中序/后序/层序），递归思维是关键。
# 解题框架：明确每个节点"需要做什么"，交给递归处理子树。
# ============================================================

from collections import deque
from typing import Optional, List


# ------------------------------------------------------------
# 1. 二叉树节点定义
# ------------------------------------------------------------

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build_tree(arr: list) -> Optional[TreeNode]:
    """
    用数组（层序表示，None 表示空节点）构建二叉树。
    方便测试时快速创建树。
    """
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    queue = deque([root])
    i = 1
    while queue and i < len(arr):
        node = queue.popleft()
        if i < len(arr) and arr[i] is not None:
            node.left = TreeNode(arr[i])
            queue.append(node.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            node.right = TreeNode(arr[i])
            queue.append(node.right)
        i += 1
    return root


def tree_to_list(root: Optional[TreeNode]) -> list:
    """将二叉树转为层序列表（方便打印）"""
    if not root:
        return []
    result = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node:
            result.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
        else:
            result.append(None)
    # 去掉末尾的 None
    while result and result[-1] is None:
        result.pop()
    return result


# ------------------------------------------------------------
# 2. 二叉树遍历（递归版 & 迭代版）
# ------------------------------------------------------------

def preorder_recursive(root: Optional[TreeNode]) -> List[int]:
    """前序遍历（递归）：根 -> 左 -> 右"""
    if not root:
        return []
    return [root.val] + preorder_recursive(root.left) + preorder_recursive(root.right)


def inorder_recursive(root: Optional[TreeNode]) -> List[int]:
    """中序遍历（递归）：左 -> 根 -> 右（BST 的中序遍历结果有序）"""
    if not root:
        return []
    return inorder_recursive(root.left) + [root.val] + inorder_recursive(root.right)


def postorder_recursive(root: Optional[TreeNode]) -> List[int]:
    """后序遍历（递归）：左 -> 右 -> 根（常用于删除/释放节点）"""
    if not root:
        return []
    return postorder_recursive(root.left) + postorder_recursive(root.right) + [root.val]


def preorder_iterative(root: Optional[TreeNode]) -> List[int]:
    """
    前序遍历（迭代版）：用栈模拟递归调用栈。
    每次弹出节点后，先压右子节点再压左子节点（保证左先被处理）。
    """
    if not root:
        return []
    result = []
    stack = [root]
    while stack:
        node = stack.pop()
        result.append(node.val)
        if node.right:
            stack.append(node.right)  # 右子节点先入栈（后处理）
        if node.left:
            stack.append(node.left)   # 左子节点后入栈（先处理）
    return result


def inorder_iterative(root: Optional[TreeNode]) -> List[int]:
    """
    中序遍历（迭代版）：模拟"一直往左走到底，再回溯"的过程。
    """
    result = []
    stack = []
    cur = root
    while cur or stack:
        # 一直向左走，将路径上的节点全部入栈
        while cur:
            stack.append(cur)
            cur = cur.left
        # 弹出栈顶节点（已无左子节点）
        cur = stack.pop()
        result.append(cur.val)
        cur = cur.right  # 转向右子树
    return result


def level_order(root: Optional[TreeNode]) -> List[List[int]]:
    """
    层序遍历（BFS）：用队列按层处理节点。
    返回二维列表，每个子列表是一层的值。
    """
    if not root:
        return []
    result = []
    queue = deque([root])
    while queue:
        level_size = len(queue)  # 当前层的节点数
        level = []
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level)
    return result


# ------------------------------------------------------------
# 3. 二叉树属性
# ------------------------------------------------------------

def max_depth(root: Optional[TreeNode]) -> int:
    """
    【题型】二叉树最大深度
    【思路】后序遍历：左右子树的最大深度取最大值 + 1。
    """
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))


def min_depth(root: Optional[TreeNode]) -> int:
    """
    【题型】二叉树最小深度（注意：叶子节点才算终点，非叶子节点不算）
    【思路】若只有一侧子树，不能用 min，否则会把 None 的深度0算进去。
    """
    if not root:
        return 0
    if not root.left:
        return 1 + min_depth(root.right)
    if not root.right:
        return 1 + min_depth(root.left)
    return 1 + min(min_depth(root.left), min_depth(root.right))


def is_balanced(root: Optional[TreeNode]) -> bool:
    """
    【题型】判断平衡二叉树（任意节点左右子树高度差 ≤ 1）
    【思路】自底向上：返回高度，若子树不平衡返回 -1。
           避免重复计算高度（若先判断平衡再算高度是 O(n log n)）。
    """
    def check(node) -> int:
        if not node:
            return 0
        left_h = check(node.left)
        right_h = check(node.right)
        # 若子树不平衡，或当前节点不平衡，返回 -1 表示不平衡
        if left_h == -1 or right_h == -1 or abs(left_h - right_h) > 1:
            return -1
        return 1 + max(left_h, right_h)

    return check(root) != -1


def is_symmetric(root: Optional[TreeNode]) -> bool:
    """
    【题型】对称二叉树（镜像）
    【思路】递归比较：左子树的左节点 = 右子树的右节点，左子树的右节点 = 右子树的左节点。
    """
    def check(left, right) -> bool:
        if not left and not right:
            return True
        if not left or not right:
            return False
        return (left.val == right.val and
                check(left.left, right.right) and  # 外侧比较
                check(left.right, right.left))       # 内侧比较

    return check(root.left, root.right) if root else True


def diameter_of_binary_tree(root: Optional[TreeNode]) -> int:
    """
    【题型】二叉树直径（任意两节点间的最长路径，路径经过的边数）
    【思路】直径 = 左子树深度 + 右子树深度（不一定经过根节点）。
           在递归求深度时，顺便更新全局最大直径。
    """
    max_diameter = 0

    def depth(node) -> int:
        nonlocal max_diameter
        if not node:
            return 0
        left_d = depth(node.left)
        right_d = depth(node.right)
        # 经过当前节点的最大路径长度 = 左深度 + 右深度
        max_diameter = max(max_diameter, left_d + right_d)
        return 1 + max(left_d, right_d)

    depth(root)
    return max_diameter


def max_path_sum(root: Optional[TreeNode]) -> int:
    """
    【题型】二叉树中的最大路径和（节点值可为负数）
    【思路】与直径类似，但求的是节点值的和。
           每个节点作为路径最高点时，贡献 = max(左路径和,0) + 节点值 + max(右路径和,0)。
           负数子树不选（贡献 0 比贡献负数更优）。
    """
    max_sum = float('-inf')

    def gain(node) -> int:
        nonlocal max_sum
        if not node:
            return 0
        # 负数贡献取 0（不如不选）
        left_gain = max(gain(node.left), 0)
        right_gain = max(gain(node.right), 0)
        # 以当前节点为最高点的路径和
        max_sum = max(max_sum, node.val + left_gain + right_gain)
        # 向父节点返回：只能选左右中的一条路（不能分叉）
        return node.val + max(left_gain, right_gain)

    gain(root)
    return max_sum


# ------------------------------------------------------------
# 4. 二叉树路径问题
# ------------------------------------------------------------

def has_path_sum(root: Optional[TreeNode], target: int) -> bool:
    """
    【题型】路径总和（根到叶的路径和是否等于目标值）
    【思路】递归：每到达一个节点，目标值减去当前节点值。叶节点时检查是否恰好减到0。
    """
    if not root:
        return False
    if not root.left and not root.right:  # 叶子节点
        return root.val == target
    return (has_path_sum(root.left, target - root.val) or
            has_path_sum(root.right, target - root.val))


def path_sum_all(root: Optional[TreeNode], target: int) -> List[List[int]]:
    """
    【题型】路径总和 II（找所有根到叶路径和等于目标的路径）
    【思路】DFS 回溯：维护当前路径，到达叶节点时检查路径和。
    """
    result = []

    def dfs(node, path, remaining):
        if not node:
            return
        path.append(node.val)
        if not node.left and not node.right and remaining == node.val:
            result.append(path[:])  # 注意要复制当前路径
        dfs(node.left, path, remaining - node.val)
        dfs(node.right, path, remaining - node.val)
        path.pop()  # 回溯：撤销当前节点

    dfs(root, [], target)
    return result


def path_sum_count(root: Optional[TreeNode], target: int) -> int:
    """
    【题型】路径总和 III（任意起点到任意终点，方向向下，路径数量）
    【思路】前缀和 + 哈希表：类比一维数组的子数组和问题。
           记录从根到当前节点的前缀和出现次数，查找差值为 target 的前缀和个数。
    【复杂度】时间 O(n)，空间 O(n)
    """
    prefix_count = {0: 1}  # 前缀和 0 出现 1 次（空路径）
    count = 0

    def dfs(node, curr_sum):
        nonlocal count
        if not node:
            return
        curr_sum += node.val
        # 查找当前前缀和 - target 是否在之前出现过
        count += prefix_count.get(curr_sum - target, 0)
        prefix_count[curr_sum] = prefix_count.get(curr_sum, 0) + 1
        dfs(node.left, curr_sum)
        dfs(node.right, curr_sum)
        prefix_count[curr_sum] -= 1  # 回溯：撤销当前节点的前缀和

    dfs(root, 0)
    return count


# ------------------------------------------------------------
# 5. 二叉树构造
# ------------------------------------------------------------

def build_from_preorder_inorder(preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
    """
    【题型】从前序与中序遍历序列构造二叉树
    【思路】前序首元素是根节点，在中序中找到根节点位置，
           左侧是左子树，右侧是右子树，递归构造。
    【复杂度】时间 O(n)（用哈希表快速查找中序位置）
    """
    inorder_map = {val: i for i, val in enumerate(inorder)}

    def build(pre_start, pre_end, in_start, in_end):
        if pre_start > pre_end:
            return None
        root_val = preorder[pre_start]
        root = TreeNode(root_val)
        in_root = inorder_map[root_val]  # 根节点在中序中的位置
        left_size = in_root - in_start   # 左子树节点数

        root.left = build(pre_start + 1, pre_start + left_size,
                          in_start, in_root - 1)
        root.right = build(pre_start + left_size + 1, pre_end,
                           in_root + 1, in_end)
        return root

    return build(0, len(preorder) - 1, 0, len(inorder) - 1)


def invert_tree(root: Optional[TreeNode]) -> Optional[TreeNode]:
    """
    【题型】翻转二叉树
    【思路】后序：先翻转左右子树，再交换左右子节点引用。
    """
    if not root:
        return None
    root.left, root.right = invert_tree(root.right), invert_tree(root.left)
    return root


# ------------------------------------------------------------
# 主程序演示
# ------------------------------------------------------------

if __name__ == "__main__":
    # 构建测试树：
    #        3
    #       / \
    #      9  20
    #        /  \
    #       15   7
    root = build_tree([3, 9, 20, None, None, 15, 7])

    print("=" * 50)
    print("二叉树：", tree_to_list(root))

    print("\n1. 遍历结果")
    print(f"  前序（递归）: {preorder_recursive(root)}")
    print(f"  前序（迭代）: {preorder_iterative(root)}")
    print(f"  中序（递归）: {inorder_recursive(root)}")
    print(f"  中序（迭代）: {inorder_iterative(root)}")
    print(f"  后序（递归）: {postorder_recursive(root)}")
    print(f"  层序:        {level_order(root)}")

    print("\n2. 树的属性")
    print(f"  最大深度: {max_depth(root)}")
    print(f"  最小深度: {min_depth(root)}")
    print(f"  是否平衡: {is_balanced(root)}")
    print(f"  是否对称: {is_symmetric(build_tree([1,2,2,3,4,4,3]))}")
    print(f"  直径: {diameter_of_binary_tree(root)}")

    print("\n3. 路径问题")
    root2 = build_tree([5,4,8,11,None,13,4,7,2,None,None,None,1])
    print(f"  路径和=22: {has_path_sum(root2, 22)}")
    print(f"  所有路径: {path_sum_all(root2, 22)}")
    print(f"  路径数量(目标=8): {path_sum_count(build_tree([10,5,-3,3,2,None,11,3,-2,None,1]), 8)}")

    print("\n4. 从前序+中序构造")
    pre = [3, 9, 20, 15, 7]
    ino = [9, 3, 15, 20, 7]
    built = build_from_preorder_inorder(pre, ino)
    print(f"  构造结果: {tree_to_list(built)}")

    print("\n5. 最大路径和")
    print(f"  [-10,9,20,None,None,15,7]: {max_path_sum(root)}")
