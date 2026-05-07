# ============================================================
# 数据结构与算法 - 第十四章：回溯算法
# ============================================================
# 回溯 = DFS + 剪枝。通过探索所有可能的候选解来找到所有（或最优）解。
# 当确定候选解不可能成为有效解时，"回溯"到上一步并尝试其他选择。
#
# 回溯框架：
#   def backtrack(path, choices):
#       if 终止条件:
#           记录结果
#           return
#       for choice in choices:
#           if 不合法: continue  # 剪枝
#           做选择（将 choice 加入 path）
#           backtrack(新状态)
#           撤销选择（将 choice 从 path 移除）
# ============================================================

from typing import List


# ------------------------------------------------------------
# 1. 子集与组合
# ------------------------------------------------------------

def subsets(nums: List[int]) -> List[List[int]]:
    """
    【题型】子集（每个元素选或不选）
    【思路】在回溯时，每个位置做"选/不选"两种决策。
    无重复元素，无需排序。结果包含空集到全集。
    """
    result = []

    def backtrack(start: int, path: List[int]):
        result.append(path[:])  # 每次进入都记录当前路径（包括空集）
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)  # i+1：每个元素只用一次，且不重复
            path.pop()              # 回溯：撤销选择

    backtrack(0, [])
    return result


def subsets_with_dup(nums: List[int]) -> List[List[int]]:
    """
    【题型】子集 II（含重复元素，不含重复子集）
    【剪枝策略】排序后，若当前元素与前一个相同且前一个没被选（在同一层跳过），则跳过。
    """
    nums.sort()
    result = []

    def backtrack(start: int, path: List[int]):
        result.append(path[:])
        for i in range(start, len(nums)):
            # 跳过同一层中的重复元素
            if i > start and nums[i] == nums[i - 1]:
                continue
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()

    backtrack(0, [])
    return result


def combinations(n: int, k: int) -> List[List[int]]:
    """
    【题型】组合（从 1..n 中选 k 个数）
    【剪枝】若剩余元素不足 k 个，提前终止：i 最大到 n - (k - len(path)) + 1
    """
    result = []

    def backtrack(start: int, path: List[int]):
        if len(path) == k:
            result.append(path[:])
            return
        # 剪枝：剩余元素不够选 k 个时停止
        for i in range(start, n - (k - len(path)) + 2):
            path.append(i)
            backtrack(i + 1, path)
            path.pop()

    backtrack(1, [])
    return result


def combination_sum(candidates: List[int], target: int) -> List[List[int]]:
    """
    【题型】组合总和（可重复选取，目标和为 target）
    【策略】每次从 start 开始枚举，允许重复选同一元素（下次 backtrack 仍从 i 开始）。
    """
    candidates.sort()
    result = []

    def backtrack(start: int, path: List[int], remaining: int):
        if remaining == 0:
            result.append(path[:])
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break  # 排序后，后续元素更大，直接剪枝
            path.append(candidates[i])
            backtrack(i, path, remaining - candidates[i])  # i 而非 i+1：可重复选
            path.pop()

    backtrack(0, [], target)
    return result


def combination_sum_2(candidates: List[int], target: int) -> List[List[int]]:
    """
    【题型】组合总和 II（每个元素只能用一次，但有重复元素）
    【剪枝】排序后，同一层中跳过重复元素（与 subsets_with_dup 相同的去重策略）。
    """
    candidates.sort()
    result = []

    def backtrack(start: int, path: List[int], remaining: int):
        if remaining == 0:
            result.append(path[:])
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break
            # 同一层跳过重复
            if i > start and candidates[i] == candidates[i - 1]:
                continue
            path.append(candidates[i])
            backtrack(i + 1, path, remaining - candidates[i])
            path.pop()

    backtrack(0, [], target)
    return result


# ------------------------------------------------------------
# 2. 排列
# ------------------------------------------------------------

def permutations(nums: List[int]) -> List[List[int]]:
    """
    【题型】全排列（无重复元素）
    【思路】每次在剩余未选的数中选一个，used 数组记录已用元素。
    """
    result = []
    used = [False] * len(nums)

    def backtrack(path: List[int]):
        if len(path) == len(nums):
            result.append(path[:])
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            used[i] = True
            path.append(nums[i])
            backtrack(path)
            path.pop()
            used[i] = False

    backtrack([])
    return result


def permutations_with_dup(nums: List[int]) -> List[List[int]]:
    """
    【题型】全排列 II（含重复元素）
    【剪枝】排序后，若当前元素与前一个相同且前一个未被使用，跳过。
           这保证重复元素必须按顺序选取（先选 nums[i-1] 再选 nums[i]）。
    """
    nums.sort()
    result = []
    used = [False] * len(nums)

    def backtrack(path: List[int]):
        if len(path) == len(nums):
            result.append(path[:])
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            # 去重：同一层中，相同值只选第一个（必须保证前一个已被选）
            if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
                continue
            used[i] = True
            path.append(nums[i])
            backtrack(path)
            path.pop()
            used[i] = False

    backtrack([])
    return result


# ------------------------------------------------------------
# 3. 棋盘问题
# ------------------------------------------------------------

def n_queens(n: int) -> List[List[str]]:
    """
    【题型】N 皇后问题（在 n×n 棋盘上放 n 个皇后，使互不攻击）
    【状态】col_set, diagonal1, diagonal2 分别记录已占用的列、主对角线、副对角线。
    【复杂度】O(n!) 时间（剪枝后）
    """
    result = []
    col_set = set()
    diag1 = set()  # 主对角线：row - col 相同的格子在同一主对角线
    diag2 = set()  # 副对角线：row + col 相同的格子在同一副对角线

    board = [['.' ] * n for _ in range(n)]

    def backtrack(row: int):
        if row == n:
            result.append([''.join(r) for r in board])
            return
        for col in range(n):
            if col in col_set or (row - col) in diag1 or (row + col) in diag2:
                continue  # 有冲突，剪枝
            # 放置皇后
            board[row][col] = 'Q'
            col_set.add(col)
            diag1.add(row - col)
            diag2.add(row + col)

            backtrack(row + 1)

            # 撤销
            board[row][col] = '.'
            col_set.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)

    backtrack(0)
    return result


def solve_sudoku(board: List[List[str]]):
    """
    【题型】解数独（原地修改）
    【策略】依次尝试在空格中填入 1-9，检查行/列/3×3宫格是否合法。
    若当前格子无法填入任何数字，回溯。
    """
    def is_valid(row: int, col: int, num: str) -> bool:
        # 检查同行
        if num in board[row]:
            return False
        # 检查同列
        if num in [board[r][col] for r in range(9)]:
            return False
        # 检查 3x3 宫格
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if board[r][c] == num:
                    return False
        return True

    def backtrack() -> bool:
        for r in range(9):
            for c in range(9):
                if board[r][c] != '.':
                    continue
                for num in '123456789':
                    if is_valid(r, c, num):
                        board[r][c] = num
                        if backtrack():
                            return True
                        board[r][c] = '.'  # 回溯
                return False  # 所有数字都不合法
        return True  # 所有格子都填完

    backtrack()


# ------------------------------------------------------------
# 4. 字符串回溯
# ------------------------------------------------------------

def generate_parentheses(n: int) -> List[str]:
    """
    【题型】括号生成（n 对括号的所有合法组合）
    【规则】当前左括号数 < n 时可加左括号；右括号数 < 左括号数时可加右括号。
    """
    result = []

    def backtrack(path: str, left: int, right: int):
        if len(path) == 2 * n:
            result.append(path)
            return
        if left < n:
            backtrack(path + '(', left + 1, right)
        if right < left:  # 右括号不能多于左括号
            backtrack(path + ')', left, right + 1)

    backtrack('', 0, 0)
    return result


def letter_combinations(digits: str) -> List[str]:
    """
    【题型】电话号码的字母组合
    【思路】每个数字对应几个字母，依次枚举每个数字对应的字母。
    """
    if not digits:
        return []

    phone_map = {
        '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
        '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'
    }
    result = []

    def backtrack(idx: int, path: str):
        if idx == len(digits):
            result.append(path)
            return
        for char in phone_map[digits[idx]]:
            backtrack(idx + 1, path + char)

    backtrack(0, '')
    return result


def word_search(board: List[List[str]], word: str) -> bool:
    """
    【题型】单词搜索（在矩阵中搜索单词，可上下左右相邻但不重复使用同一格）
    """
    rows, cols = len(board), len(board[0])
    visited = set()

    def dfs(r: int, c: int, idx: int) -> bool:
        if idx == len(word):
            return True
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return False
        if (r, c) in visited or board[r][c] != word[idx]:
            return False

        visited.add((r, c))
        found = (dfs(r+1,c,idx+1) or dfs(r-1,c,idx+1) or
                 dfs(r,c+1,idx+1) or dfs(r,c-1,idx+1))
        visited.remove((r, c))  # 回溯

        return found

    for r in range(rows):
        for c in range(cols):
            if dfs(r, c, 0):
                return True
    return False


def restore_ip_addresses(s: str) -> List[str]:
    """
    【题型】复原 IP 地址（将字符串分为 4 段，每段 0-255，无前导0）
    """
    result = []

    def backtrack(start: int, parts: List[str]):
        if len(parts) == 4:
            if start == len(s):
                result.append('.'.join(parts))
            return
        for length in range(1, 4):  # 每段 1-3 位
            if start + length > len(s):
                break
            segment = s[start:start + length]
            # 剪枝：有前导零（长度>1且以0开头）或 > 255
            if (len(segment) > 1 and segment[0] == '0') or int(segment) > 255:
                continue
            backtrack(start + length, parts + [segment])

    backtrack(0, [])
    return result


# ------------------------------------------------------------
# 主程序演示
# ------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 50)
    print("1. 子集")
    print(f"  [1,2,3]: {subsets([1,2,3])}")

    print("\n2. 含重复元素的子集")
    print(f"  [1,2,2]: {subsets_with_dup([1,2,2])}")

    print("\n3. 组合总和")
    print(f"  candidates=[2,3,6,7], target=7: {combination_sum([2,3,6,7], 7)}")

    print("\n4. 全排列")
    print(f"  [1,2,3]: {permutations([1,2,3])}")

    print("\n5. 含重复的全排列")
    print(f"  [1,1,2]: {permutations_with_dup([1,1,2])}")

    print("\n6. N 皇后")
    solutions = n_queens(4)
    print(f"  4皇后有 {len(solutions)} 个解，第一个解：")
    for row in solutions[0]:
        print(f"    {row}")

    print("\n7. 括号生成")
    print(f"  n=3: {generate_parentheses(3)}")

    print("\n8. 电话号码字母组合")
    print(f"  '23': {letter_combinations('23')}")

    print("\n9. 单词搜索")
    board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]]
    print(f"  'ABCCED': {word_search(board, 'ABCCED')}")
    print(f"  'ABCB': {word_search(board, 'ABCB')}")

    print("\n10. 复原IP地址")
    print(f"  '25525511135': {restore_ip_addresses('25525511135')}")
