# ==========================================================
# SAME GAME - ADT & DSA BASED IMPLEMENTATION (REVIEW - 2)
# ==========================================================
# ADTs USED:
# 1. Grid ADT        -> 2D List (Board Representation)
# 2. Graph ADT       -> Implicit Grid Graph (Neighbor Traversal)
# 3. Stack ADT       -> Used in DFS + Gravity Mechanism
# 4. Set ADT         -> To track visited nodes
# 5. List ADT        -> Store connected components
#
# ALGORITHMS USED:
# 1. DFS (Connected Component Detection)
# 2. Stack-based Gravity
# 3. Merge Sort (Divide & Conquer)  [From Review-1]
# 4. Dynamic Programming (Memoization for Optimal CPU Move)
# ==========================================================

import random
import copy
import sys
sys.setrecursionlimit(10000)

# -------------------------------
# GLOBAL GAME VARIABLES
# -------------------------------
ROWS = 6
COLS = 6
COLORS = ['R', 'G', 'B', 'Y']

# ==========================================================
# GRID ADT
# ==========================================================
class GridADT:
    """
    Grid Abstract Data Type
    Responsible for board creation and display
    Space Complexity: O(R * C)
    """

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.board = self.create_board()

    def create_board(self):
        # Time Complexity: O(R * C)
        return [[random.choice(COLORS) for _ in range(self.cols)]
                for _ in range(self.rows)]

    def display(self):
        # Time Complexity: O(R * C)
        print("\nBoard:")
        print("   ", end="")
        for c in range(self.cols):
            print(c, end=" ")
        print()

        for r in range(self.rows):
            print(r, " ", end="")
            for c in range(self.cols):
                print(self.board[r][c] if self.board[r][c] else '.', end=" ")
            print()
        print()

# ==========================================================
# GRAPH ADT (IMPLICIT GRID GRAPH)
# ==========================================================
class GraphADT:
    """
    Graph Representation:
    Each cell is treated as a node.
    Edges exist between adjacent cells
    (Up, Down, Left, Right)
    """

    @staticmethod
    def neighbors(r, c):
        return [(r+1, c), (r-1, c), (r, c+1), (r, c-1)]

# ==========================================================
# DFS - CONNECTED COMPONENT DETECTION
# ==========================================================
# Time Complexity: O(R * C)
# Each cell is visited at most once.
# Space Complexity: O(R * C) (Recursion stack + visited set)
# ==========================================================

def dfs(grid, r, c, color, visited, component):

    if r < 0 or r >= grid.rows or c < 0 or c >= grid.cols:
        return
    if (r, c) in visited:
        return
    if grid.board[r][c] != color:
        return

    visited.add((r, c))
    component.append((r, c))

    for nr, nc in GraphADT.neighbors(r, c):
        dfs(grid, nr, nc, color, visited, component)

def get_component(grid, r, c):

    if grid.board[r][c] is None:
        return []

    visited = set()
    component = []
    dfs(grid, r, c, grid.board[r][c], visited, component)
    return component

# ==========================================================
# REMOVE COMPONENT
# ==========================================================
# Time Complexity: O(k)
# where k = size of component
# ==========================================================

def remove_component(grid, component):
    for r, c in component:
        grid.board[r][c] = None

# ==========================================================
# GRAVITY USING STACK ADT
# ==========================================================
# Time Complexity: O(R * C)
# For each column:
#   1. Push non-empty elements into stack
#   2. Refill from bottom
# Space Complexity: O(R)
# ==========================================================

def apply_gravity(grid):

    for c in range(grid.cols):
        stack = []

        for r in range(grid.rows):
            if grid.board[r][c]:
                stack.append(grid.board[r][c])

        for r in range(grid.rows - 1, -1, -1):
            grid.board[r][c] = stack.pop() if stack else None

# ==========================================================
# GAME OVER CHECK
# ==========================================================
# Time Complexity: O((R*C)^2) worst case
# ==========================================================

def is_game_over(grid):

    for r in range(grid.rows):
        for c in range(grid.cols):
            if grid.board[r][c]:
                if len(get_component(grid, r, c)) > 1:
                    return False
    return True

# ==========================================================
# MERGE SORT (DIVIDE & CONQUER) - REVIEW 1
# ==========================================================
# Time Complexity: O(n log n)
# Used previously for greedy CPU move selection.
# ==========================================================

def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i][0] >= right[j][0]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result

# ==========================================================
# DYNAMIC PROGRAMMING (MEMOIZATION) - REVIEW 2
# ==========================================================
# State:
#   Board configuration (converted to tuple)
#
# Recurrence:
#   DP(state) = max(size^2 + DP(next_state))
#
# Without Memoization:
#   Exponential time complexity
#
# With Memoization:
#   Reduced significantly by avoiding recomputation
#
# Space Complexity:
#   O(number of unique board states)
# ==========================================================

memo = {}

def board_state(grid):
    return tuple(tuple(row) for row in grid.board)

def dp_max_score(grid):

    state = board_state(grid)

    if state in memo:
        return memo[state]

    components = []
    visited_global = set()

    for r in range(grid.rows):
        for c in range(grid.cols):
            if grid.board[r][c] and (r, c) not in visited_global:
                comp = get_component(grid, r, c)
                for cell in comp:
                    visited_global.add(cell)
                if len(comp) > 1:
                    components.append(comp)

    if not components:
        return 0

    max_score = 0

    for comp in components:
        new_grid = copy.deepcopy(grid)
        remove_component(new_grid, comp)
        apply_gravity(new_grid)

        score = len(comp) ** 2 + dp_max_score(new_grid)
        max_score = max(max_score, score)

    memo[state] = max_score
    return max_score

# ==========================================================
# CPU MOVE USING DYNAMIC PROGRAMMING
# ==========================================================

def cpu_best_move(grid):

    best_move = []
    best_score = 0
    visited_global = set()

    for r in range(grid.rows):
        for c in range(grid.cols):
            if grid.board[r][c] and (r, c) not in visited_global:
                comp = get_component(grid, r, c)
                for cell in comp:
                    visited_global.add(cell)

                if len(comp) > 1:
                    new_grid = copy.deepcopy(grid)
                    remove_component(new_grid, comp)
                    apply_gravity(new_grid)

                    future_score = dp_max_score(new_grid)
                    total_score = len(comp) ** 2 + future_score

                    if total_score > best_score:
                        best_score = total_score
                        best_move = comp

    return best_move

# ==========================================================
# SINGLE PLAYER MODE
# ==========================================================

def single_player():

    grid = GridADT(ROWS, COLS)
    score = 0

    while not is_game_over(grid):

        grid.display()
        print("Score:", score)

        r = int(input("Row: "))
        c = int(input("Column: "))

        comp = get_component(grid, r, c)

        if len(comp) <= 1:
            print("Invalid Move!")
            continue

        score += len(comp) ** 2
        remove_component(grid, comp)
        apply_gravity(grid)

    print("GAME OVER | Final Score:", score)

# ==========================================================
# MULTIPLAYER MODE (HUMAN VS CPU)
# ==========================================================

def multiplayer():

    grid = GridADT(ROWS, COLS)
    human = cpu = 0

    while not is_game_over(grid):

        grid.display()
        print("Human:", human, "| CPU:", cpu)

        r = int(input("Row: "))
        c = int(input("Column: "))

        comp = get_component(grid, r, c)

        if len(comp) <= 1:
            print("Invalid Move!")
            continue

        human += len(comp) ** 2
        remove_component(grid, comp)
        apply_gravity(grid)

        if is_game_over(grid):
            break

        cpu_comp = cpu_best_move(grid)
        cpu += len(cpu_comp) ** 2
        remove_component(grid, cpu_comp)
        apply_gravity(grid)

        print("CPU played...\n")

    print("GAME OVER")
    print("Human:", human, "| CPU:", cpu)
    print("Winner:", "Human 🎉" if human > cpu else "CPU 🤖")

# ==========================================================
# MAIN MENU
# ==========================================================

def main_menu():

    while True:
        print("\n====== SAME GAME MENU ======")
        print("1. Single Player")
        print("2. Multiplayer")
        print("3. Exit")

        ch = input("Choice: ")

        if ch == '1':
            single_player()
        elif ch == '2':
            multiplayer()
        elif ch == '3':
            print("Thanks for playing!")
            break
        else:
            print("Invalid choice!")

# ==========================================================
# DRIVER CODE
# ==========================================================

if __name__ == "__main__":
    main_menu()
