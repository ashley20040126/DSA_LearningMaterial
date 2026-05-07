# ============================================================
# 数据结构与算法 - 第七章：图论基础
# ============================================================
# 图由顶点（Vertex）和边（Edge）组成，分有向图和无向图。
# 图的存储方式：邻接矩阵（O(V²)空间）和邻接表（O(V+E)空间）。
# 图遍历：DFS（深度优先）和 BFS（广度优先），是解决图问题的基础。
# ============================================================

from collections import defaultdict, deque
from typing import List, Dict, Set


# ------------------------------------------------------------
# 1. 图的表示方式
# ------------------------------------------------------------

class Graph:
    """
    使用邻接表表示的图（适合稀疏图）。
    邻接矩阵适合稠密图（边数接近 V²）但空间浪费大。
    """

    def __init__(self, directed=False):
        self.adj = defaultdict(list)  # 邻接表：顶点 -> [邻居列表]
        self.directed = directed

    def add_edge(self, u, v, weight=1):
        """添加边（默认无向图，添加双向）"""
        self.adj[u].append((v, weight))
        if not self.directed:
            self.adj[v].append((u, weight))

    def get_neighbors(self, u):
        return self.adj[u]

    def vertices(self):
        return list(self.adj.keys())


# ------------------------------------------------------------
# 2. 深度优先搜索（DFS）
# ------------------------------------------------------------

def dfs_recursive(graph: Graph, start, visited: Set = None) -> List:
    """
    DFS 递归版：沿着一条路走到底，再回溯探索其他路径。
    时间复杂度 O(V+E)，空间 O(V)（递归栈 + visited 集合）。
    """
    if visited is None:
        visited = set()
    visited.add(start)
    result = [start]

    for neighbor, _ in graph.get_neighbors(start):
        if neighbor not in visited:
            result.extend(dfs_recursive(graph, neighbor, visited))

    return result


def dfs_iterative(graph: Graph, start) -> List:
    """
    DFS 迭代版：用显式栈替代递归调用栈，避免深度过大时栈溢出。
    """
    visited = set()
    stack = [start]
    result = []

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            result.append(node)
            # 将未访问的邻居压栈（逆序压入保证顺序与递归一致）
            for neighbor, _ in reversed(graph.get_neighbors(node)):
                if neighbor not in visited:
                    stack.append(neighbor)

    return result


# ------------------------------------------------------------
# 3. 广度优先搜索（BFS）
# ------------------------------------------------------------

def bfs(graph: Graph, start) -> List:
    """
    BFS：逐层扩散，先访问所有距离为1的节点，再访问距离为2的节点……
    适合求最短路径（无权图）。
    时间复杂度 O(V+E)，空间 O(V)。
    """
    visited = {start}
    queue = deque([start])
    result = []

    while queue:
        node = queue.popleft()
        result.append(node)
        for neighbor, _ in graph.get_neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return result


def bfs_shortest_path(graph: Graph, start, end) -> List:
    """
    BFS 求无权图中 start 到 end 的最短路径。
    使用父节点字典回溯路径。
    """
    if start == end:
        return [start]

    visited = {start}
    queue = deque([start])
    parent = {start: None}  # 记录每个节点的父节点，用于回溯路径

    while queue:
        node = queue.popleft()
        for neighbor, _ in graph.get_neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = node
                if neighbor == end:
                    # 找到终点，回溯路径
                    path = []
                    cur = end
                    while cur is not None:
                        path.append(cur)
                        cur = parent[cur]
                    return path[::-1]
                queue.append(neighbor)

    return []  # 不可达


# ------------------------------------------------------------
# 4. 连通性问题
# ------------------------------------------------------------

def count_connected_components(n: int, edges: List[List[int]]) -> int:
    """
    【题型】无向图中连通分量的数目
    【思路】DFS/BFS：遍历所有未访问的节点，每次从新节点出发的遍历对应一个连通分量。
    """
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    visited = set()
    components = 0

    def dfs(node):
        visited.add(node)
        for neighbor in adj[node]:
            if neighbor not in visited:
                dfs(neighbor)

    for node in range(n):
        if node not in visited:
            dfs(node)
            components += 1  # 每个未访问节点的 DFS 对应一个连通分量

    return components


def has_cycle_undirected(n: int, edges: List[List[int]]) -> bool:
    """
    【题型】无向图是否有环（DFS 版）
    【思路】DFS 时记录当前节点的父节点，若发现访问过的邻居不是父节点，则有环。
    """
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    visited = set()

    def dfs(node, parent) -> bool:
        visited.add(node)
        for neighbor in adj[node]:
            if neighbor not in visited:
                if dfs(neighbor, node):
                    return True
            elif neighbor != parent:
                # 访问过且不是父节点 → 存在环
                return True
        return False

    for node in range(n):
        if node not in visited:
            if dfs(node, -1):
                return True
    return False


def has_cycle_directed(n: int, edges: List[List[int]]) -> bool:
    """
    【题型】有向图是否有环（三色标记法）
    【思路】白色(0)=未访问，灰色(1)=访问中（在当前路径上），黑色(2)=已完成。
           DFS 中若访问到灰色节点，说明当前路径形成了环。
    """
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)

    color = [0] * n  # 0:白, 1:灰, 2:黑

    def dfs(node) -> bool:
        color[node] = 1  # 标记为灰色（访问中）
        for neighbor in adj[node]:
            if color[neighbor] == 1:
                return True   # 遇到灰色节点，有环
            if color[neighbor] == 0:
                if dfs(neighbor):
                    return True
        color[node] = 2  # 标记为黑色（完成）
        return False

    for i in range(n):
        if color[i] == 0:
            if dfs(i):
                return True
    return False


# ------------------------------------------------------------
# 5. 拓扑排序（有向无环图 DAG）
# ------------------------------------------------------------

def topological_sort_dfs(n: int, edges: List[List[int]]) -> List[int]:
    """
    拓扑排序（DFS 后序版）：
    DFS 完成时将节点加入结果列表（后续节点先入，最终反转）。
    适用于有向无环图（DAG），如任务依赖关系、课程安排。
    """
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)

    visited = set()
    result = []

    def dfs(node):
        visited.add(node)
        for neighbor in adj[node]:
            if neighbor not in visited:
                dfs(neighbor)
        result.append(node)  # 后序：所有后继节点处理完后才加入

    for i in range(n):
        if i not in visited:
            dfs(i)

    return result[::-1]  # 反转得到拓扑序


def topological_sort_bfs(n: int, edges: List[List[int]]) -> List[int]:
    """
    拓扑排序（Kahn 算法 / BFS 版）：
    维护入度表，每次将入度为0的节点加入结果，同时减少其邻居的入度。
    可以检测有向图是否有环（结果长度 < n 则有环）。
    """
    adj = defaultdict(list)
    in_degree = [0] * n

    for u, v in edges:
        adj[u].append(v)
        in_degree[v] += 1

    # 将所有入度为0的节点加入队列（可以立即处理）
    queue = deque([i for i in range(n) if in_degree[i] == 0])
    result = []

    while queue:
        node = queue.popleft()
        result.append(node)
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)  # 入度降为0，可以被处理

    return result if len(result) == n else []  # 空列表表示有环


# ------------------------------------------------------------
# 6. 岛屿问题（网格 DFS/BFS）
# ------------------------------------------------------------

def num_islands(grid: List[List[str]]) -> int:
    """
    【题型】岛屿数量
    【思路】DFS：遇到 '1' 则从该格开始 DFS，将连通的所有 '1' 标记为已访问（改为 '0'）。
           每次触发 DFS 的次数即为岛屿数。
    【复杂度】时间 O(m*n)，空间 O(m*n)（递归栈）
    """
    if not grid:
        return 0

    rows, cols = len(grid), len(grid[0])
    count = 0

    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != '1':
            return
        grid[r][c] = '0'  # 标记为已访问
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1
                dfs(r, c)

    return count


def max_area_of_island(grid: List[List[int]]) -> int:
    """
    【题型】岛屿的最大面积
    【思路】DFS 时累计面积，返回每次 DFS 探索的总格子数。
    """
    rows, cols = len(grid), len(grid[0])

    def dfs(r, c) -> int:
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] == 0:
            return 0
        grid[r][c] = 0  # 标记已访问
        return 1 + dfs(r+1,c) + dfs(r-1,c) + dfs(r,c+1) + dfs(r,c-1)

    return max(dfs(r, c) for r in range(rows) for c in range(cols))


def surrounded_regions(board: List[List[str]]):
    """
    【题型】被围绕的区域（将被 'X' 包围的 'O' 替换为 'X'）
    【思路】反向思维：从边界的 'O' 开始 DFS，将与边界相连的 'O' 标记为 '#'（安全）。
           遍历完后，'O' 变为 'X'，'#' 变回 'O'。
    """
    if not board:
        return
    rows, cols = len(board), len(board[0])

    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or board[r][c] != 'O':
            return
        board[r][c] = '#'  # 安全标记
        for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            dfs(r+dr, c+dc)

    # 从四条边界出发 DFS 标记安全的 'O'
    for r in range(rows):
        if board[r][0] == 'O': dfs(r, 0)
        if board[r][cols-1] == 'O': dfs(r, cols-1)
    for c in range(cols):
        if board[0][c] == 'O': dfs(0, c)
        if board[rows-1][c] == 'O': dfs(rows-1, c)

    # 遍历整个棋盘：'O'→'X'（被围），'#'→'O'（安全）
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == 'O':
                board[r][c] = 'X'
            elif board[r][c] == '#':
                board[r][c] = 'O'


# ------------------------------------------------------------
# 主程序演示
# ------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 50)
    print("1. 图的构建与遍历")
    g = Graph(directed=False)
    for u, v in [(0,1),(0,2),(1,3),(2,4),(3,4)]:
        g.add_edge(u, v)
    print(f"  DFS（递归）: {dfs_recursive(g, 0)}")
    print(f"  DFS（迭代）: {dfs_iterative(g, 0)}")
    print(f"  BFS:        {bfs(g, 0)}")

    print("\n2. 最短路径（BFS）")
    print(f"  0->4: {bfs_shortest_path(g, 0, 4)}")

    print("\n3. 连通分量")
    print(f"  5个节点，3条边的连通分量数: {count_connected_components(5, [[0,1],[1,2],[3,4]])}")

    print("\n4. 拓扑排序")
    # 课程安排：[a,b] 表示 b 是 a 的先修课
    # 0->1->3, 0->2->3
    edges = [[0,1],[0,2],[1,3],[2,3]]
    print(f"  DFS 版: {topological_sort_dfs(4, edges)}")
    print(f"  BFS 版: {topological_sort_bfs(4, edges)}")

    print("\n5. 岛屿问题")
    grid = [["1","1","0","0","0"],
            ["1","1","0","0","0"],
            ["0","0","1","0","0"],
            ["0","0","0","1","1"]]
    print(f"  岛屿数量: {num_islands(grid)}")

    grid2 = [[0,0,1,0,0,0,0,1,0,0,0,0,0],
             [0,0,0,0,0,0,0,1,1,1,0,0,0],
             [0,1,1,0,1,0,0,0,0,0,0,0,0],
             [0,1,0,0,1,1,0,0,1,0,1,0,0],
             [0,1,0,0,1,1,0,0,1,1,1,0,0],
             [0,0,0,0,0,0,0,0,0,0,1,0,0],
             [0,0,0,0,0,0,0,1,1,1,0,0,0],
             [0,0,0,0,0,0,0,1,1,0,0,0,0]]
    print(f"  最大岛屿面积: {max_area_of_island(grid2)}")
