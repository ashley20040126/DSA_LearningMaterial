# ============================================================
# 数据结构与算法 - 第八章：最短路径 & 最小生成树
# ============================================================
# 最短路径算法：
#   - Dijkstra：非负权重，贪心+优先队列，O((V+E) log V)
#   - Bellman-Ford：允许负权重（但无负权环），O(VE)
#   - Floyd-Warshall：全源最短路，O(V³)
# 最小生成树：
#   - Kruskal：按边权排序，并查集合并，O(E log E)
#   - Prim：从顶点扩展，优先队列，O((V+E) log V)
# ============================================================

import heapq
from collections import defaultdict
from typing import List, Tuple, Dict


# ------------------------------------------------------------
# 1. Dijkstra 最短路径算法
# ------------------------------------------------------------

def dijkstra(graph: Dict, start) -> Dict:
    """
    Dijkstra 算法：单源最短路径（非负权重）。

    【思路】贪心策略：每次从未访问节点中选取距离最小的节点，
           用它来更新邻居的距离。优先队列保证 O(log V) 取最小值。

    【复杂度】时间 O((V+E) log V)，空间 O(V)

    graph 格式：{节点: [(邻居, 权重), ...]}
    """
    dist = {node: float('inf') for node in graph}
    dist[start] = 0
    # 优先队列：(距离, 节点)
    heap = [(0, start)]

    while heap:
        d, u = heapq.heappop(heap)
        # 如果弹出的距离大于已知最短距离，跳过（已有更短路径更新过）
        if d > dist[u]:
            continue
        for v, weight in graph[u]:
            new_dist = dist[u] + weight
            if new_dist < dist[v]:
                dist[v] = new_dist
                heapq.heappush(heap, (new_dist, v))

    return dist


def dijkstra_with_path(graph: Dict, start, end):
    """
    Dijkstra 算法（同时返回最短路径）。
    用 prev 字典记录每个节点的前驱节点，最终回溯出路径。
    """
    dist = {node: float('inf') for node in graph}
    dist[start] = 0
    prev = {node: None for node in graph}
    heap = [(0, start)]

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        if u == end:
            break
        for v, weight in graph[u]:
            new_dist = dist[u] + weight
            if new_dist < dist[v]:
                dist[v] = new_dist
                prev[v] = u
                heapq.heappush(heap, (new_dist, v))

    # 回溯路径
    path = []
    cur = end
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    path.reverse()

    return dist[end], path if path[0] == start else []


# ------------------------------------------------------------
# 2. Bellman-Ford 算法（允许负权重）
# ------------------------------------------------------------

def bellman_ford(n: int, edges: List[Tuple], start: int) -> Dict:
    """
    Bellman-Ford 算法：单源最短路径，允许负权重边，可检测负权环。

    【思路】对所有边进行 V-1 轮松弛操作。
           若第 V 轮仍能松弛，说明存在负权环（距离可以无限减小）。

    【复杂度】时间 O(VE)，空间 O(V)

    edges 格式：[(from, to, weight), ...]
    """
    dist = {i: float('inf') for i in range(n)}
    dist[start] = 0

    # 进行 V-1 轮松弛
    for _ in range(n - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                updated = True
        if not updated:
            break  # 提前终止：无更新说明已收敛

    # 第 V 轮检测负权环
    for u, v, w in edges:
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
            return None  # 存在负权环，返回 None

    return dist


# ------------------------------------------------------------
# 3. Floyd-Warshall 全源最短路径
# ------------------------------------------------------------

def floyd_warshall(n: int, edges: List[Tuple]) -> List[List]:
    """
    Floyd-Warshall：计算所有节点对之间的最短路径。

    【思路】动态规划：dp[i][j] = i 到 j 的最短路。
           对每个中间节点 k，尝试以 k 为中转更新 dp[i][j]。
           dp[i][j] = min(dp[i][j], dp[i][k] + dp[k][j])

    【复杂度】时间 O(V³)，空间 O(V²)
    """
    INF = float('inf')
    dist = [[INF] * n for _ in range(n)]

    # 初始化：自己到自己距离为0
    for i in range(n):
        dist[i][i] = 0

    # 填入已知边的权重
    for u, v, w in edges:
        dist[u][v] = w

    # 枚举中间节点 k
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    # 检查负权环：对角线上出现负值
    for i in range(n):
        if dist[i][i] < 0:
            return None  # 存在负权环

    return dist


# ------------------------------------------------------------
# 4. 并查集（Union-Find）—— Kruskal 的基础
# ------------------------------------------------------------

class UnionFind:
    """
    并查集（不相交集合）数据结构。
    支持高效的合并（union）和查找（find）操作。

    优化：
    - 路径压缩：find 时直接将节点挂到根节点，降低树高
    - 按秩合并：将较矮的树合并到较高的树，避免退化成链

    时间复杂度：每次操作接近 O(1)（摊销，严格为 O(α(n))，α 为阿克曼函数的反函数）
    """

    def __init__(self, n: int):
        self.parent = list(range(n))  # 每个节点初始时是自己的父节点
        self.rank = [0] * n           # 树的高度（按秩合并用）
        self.components = n           # 连通分量数

    def find(self, x: int) -> int:
        """查找根节点（路径压缩）"""
        if self.parent[x] != x:
            # 路径压缩：递归找根后，直接将 x 的父节点设为根
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """
        合并两个集合。
        返回 True 表示成功合并（原本不在同一集合）；False 表示已在同一集合（有环）。
        """
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False  # 已连通，加入这条边会形成环

        # 按秩合并：将矮树合并到高树下
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1

        self.components -= 1
        return True

    def connected(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)


# ------------------------------------------------------------
# 5. Kruskal 最小生成树
# ------------------------------------------------------------

def kruskal(n: int, edges: List[Tuple]) -> Tuple[int, List]:
    """
    Kruskal 算法：从最小权重的边开始贪心选择，用并查集避免成环。

    【步骤】
    1. 按权重从小到大排序所有边
    2. 依次尝试加入每条边：若不形成环（两端点不在同一集合），则加入
    3. 直到已选 V-1 条边（生成树完成）

    【复杂度】时间 O(E log E)（主要是排序），空间 O(V)

    返回：(最小生成树总权重, 选中的边列表)
    """
    # 按权重排序
    sorted_edges = sorted(edges, key=lambda x: x[2])
    uf = UnionFind(n)
    total_weight = 0
    mst_edges = []

    for u, v, w in sorted_edges:
        if uf.union(u, v):  # 成功合并（不形成环）
            total_weight += w
            mst_edges.append((u, v, w))
            if len(mst_edges) == n - 1:
                break  # 已选 V-1 条边，生成树完成

    if len(mst_edges) < n - 1:
        return -1, []  # 图不连通，无法生成树

    return total_weight, mst_edges


# ------------------------------------------------------------
# 6. Prim 最小生成树
# ------------------------------------------------------------

def prim(n: int, graph: Dict) -> int:
    """
    Prim 算法：从任意顶点出发，每次将距离已选顶点集最近的顶点加入生成树。

    【思路】维护一个 "切割"（cut）：已选集合 vs 未选集合，
           每次选择横跨切割的最小权重边，用优先队列高效实现。

    【复杂度】时间 O((V+E) log V)，空间 O(V+E)

    graph 格式：{节点: [(邻居, 权重), ...]}
    """
    visited = set()
    heap = [(0, 0)]  # (权重, 节点)，从节点0开始
    total = 0

    while heap and len(visited) < n:
        weight, u = heapq.heappop(heap)
        if u in visited:
            continue
        visited.add(u)
        total += weight
        for v, w in graph.get(u, []):
            if v not in visited:
                heapq.heappush(heap, (w, v))

    return total if len(visited) == n else -1  # -1 表示图不连通


# ------------------------------------------------------------
# 7. 实战题：网络延迟时间
# ------------------------------------------------------------

def network_delay_time(times: List[List[int]], n: int, k: int) -> int:
    """
    【题型】网络延迟时间（LeetCode 743）
    【描述】从节点 k 发出信号，求所有节点都收到信号的最短时间。
    【思路】Dijkstra 求从 k 到所有节点的最短路，取最大值即为答案。
    """
    graph = defaultdict(list)
    for u, v, w in times:
        graph[u].append((v, w))

    dist = dijkstra(graph, k)
    max_dist = max(dist.get(i, float('inf')) for i in range(1, n + 1))
    return max_dist if max_dist != float('inf') else -1


def min_cost_connect_points(points: List[List[int]]) -> int:
    """
    【题型】连接所有点的最小费用（LeetCode 1584）
    【描述】点的连接费用为曼哈顿距离，求连接所有点的最小费用（最小生成树）。
    【思路】Prim 算法（稠密图更高效），用优先队列。
    """
    n = len(points)
    visited = set()
    heap = [(0, 0)]  # (权重, 节点下标)
    total = 0
    count = 0

    while heap and count < n:
        cost, u = heapq.heappop(heap)
        if u in visited:
            continue
        visited.add(u)
        total += cost
        count += 1
        x1, y1 = points[u]
        for v in range(n):
            if v not in visited:
                x2, y2 = points[v]
                dist = abs(x1 - x2) + abs(y1 - y2)
                heapq.heappush(heap, (dist, v))

    return total


# ------------------------------------------------------------
# 主程序演示
# ------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 50)

    # 有向带权图
    graph = {
        0: [(1, 4), (2, 1)],
        1: [(3, 1)],
        2: [(1, 2), (3, 5)],
        3: []
    }

    print("1. Dijkstra 最短路径")
    dist = dijkstra(graph, 0)
    print(f"  从0出发的最短距离: {dist}")
    d, path = dijkstra_with_path(graph, 0, 3)
    print(f"  0->3 最短距离: {d}, 路径: {path}")

    print("\n2. Bellman-Ford（允许负权重）")
    edges_bf = [(0,1,4),(0,2,1),(2,1,2),(1,3,1),(2,3,5)]
    dist_bf = bellman_ford(4, edges_bf, 0)
    print(f"  从0出发: {dist_bf}")

    print("\n3. Floyd-Warshall 全源最短路")
    edges_fw = [(0,1,3),(0,3,5),(1,2,1),(2,3,2)]
    dist_fw = floyd_warshall(4, edges_fw)
    for i, row in enumerate(dist_fw):
        print(f"  从{i}出发: {row}")

    print("\n4. 并查集演示")
    uf = UnionFind(6)
    uf.union(0, 1); uf.union(1, 2); uf.union(3, 4)
    print(f"  0和2连通: {uf.connected(0,2)}")
    print(f"  0和3连通: {uf.connected(0,3)}")
    print(f"  连通分量数: {uf.components}")

    print("\n5. Kruskal 最小生成树")
    edges_k = [(0,1,2),(0,3,6),(1,2,3),(1,3,8),(1,4,5),(2,4,7),(3,4,9)]
    weight, mst = kruskal(5, edges_k)
    print(f"  最小权重: {weight}, 选边: {mst}")

    print("\n6. 网络延迟时间")
    times = [[2,1,1],[2,3,1],[3,4,1]]
    print(f"  结果: {network_delay_time(times, 4, 2)}")

    print("\n7. 连接所有点的最小费用")
    points = [[0,0],[2,2],[3,10],[5,2],[7,0]]
    print(f"  最小费用: {min_cost_connect_points(points)}")
