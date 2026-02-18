# ==========================================================
# SAME GAME - ADT & DSA BASED IMPLEMENTATION
# NOW WITH OPTIMAL DP + MERGE SORT
# ==========================================================

import random
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
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.board = self.create_board()

    def create_board(self):
        return [[random.choice(COLORS) for _ in range(self.cols)]
                for _ in range(self.rows)]

    def display(self):
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
# GRAPH ADT
# ==========================================================
class GraphADT:
    @staticmethod
    def neighbors(r, c):
        return [(r+1, c), (r-1, c), (r, c+1), (r, c-1)]

# ==========================================================
# DFS
# ==========================================================
def dfs(grid, r, c, color, visited, component):
    if r < 0 or r >= ROWS or c < 0 or c >= COLS:
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
# REMOVE
# ==========================================================
def remove_component(grid, component):
    for r, c in component:
        grid.board[r][c] = None

# ==========================================================
# GRAVITY
# ==========================================================
def apply_gravity(grid):
    for c in range(COLS):
        stack = []
        for r in range(ROWS):
            if grid.board[r][c]:
                stack.append(grid.board[r][c])

        for r in range(ROWS-1, -1, -1):
            grid.board[r][c] = stack.pop() if stack else None

# ==========================================================
# GAME OVER
# ==========================================================
def is_game_over(grid):
    visited_global = set()
    for r in range(ROWS):
        for c in range(COLS):
            if grid.board[r][c] and (r, c) not in visited_global:
                comp = get_component(grid, r, c)
                for cell in comp:
                    visited_global.add(cell)
                if len(comp) > 1:
                    return False
    return True

# ==========================================================
# MERGE SORT (UNCHANGED)
# ==========================================================
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

    while i < len(left):
        result.append(left[i])
        i += 1

    while j < len(right):
        result.append(right[j])
        j += 1

    return result

def merge_sort_components(components):
    if len(components) <= 1:
        return components

    mid = len(components) // 2
    left = merge_sort_components(components[:mid])
    right = merge_sort_components(components[mid:])

    return merge(left, right)

# ==========================================================
# DYNAMIC PROGRAMMING (OPTIMAL PLAY)
# ==========================================================
def board_to_tuple(grid):
    return tuple(tuple(row) for row in grid.board)

def copy_grid(grid):
    new_grid = GridADT(ROWS, COLS)
    new_grid.board = [row[:] for row in grid.board]
    return new_grid

def dp_best_score(grid, memo):
    state = board_to_tuple(grid)

    if state in memo:
        return memo[state]

    if is_game_over(grid):
        memo[state] = 0
        return 0

    max_score = 0
    visited_cells = set()

    for r in range(ROWS):
        for c in range(COLS):
            if grid.board[r][c] and (r, c) not in visited_cells:

                comp = get_component(grid, r, c)
                for cell in comp:
                    visited_cells.add(cell)

                if len(comp) > 1:
                    temp = copy_grid(grid)
                    remove_component(temp, comp)
                    apply_gravity(temp)

                    future_score = dp_best_score(temp, memo)
                    total_score = len(comp) ** 2 + future_score

                    if total_score > max_score:
                        max_score = total_score

    memo[state] = max_score
    return max_score

# ==========================================================
# CPU MOVE
# ==========================================================
def cpu_best_move(grid):
    memo = {}
    components = []
    visited_cells = set()

    for r in range(ROWS):
        for c in range(COLS):
            if grid.board[r][c] and (r, c) not in visited_cells:

                comp = get_component(grid, r, c)
                for cell in comp:
                    visited_cells.add(cell)

                if len(comp) > 1:
                    temp = copy_grid(grid)
                    remove_component(temp, comp)
                    apply_gravity(temp)

                    future_score = dp_best_score(temp, memo)
                    total_achievable = len(comp) ** 2 + future_score

                    components.append((total_achievable, comp))

    if not components:
        return [], 0, 0

    sorted_components = merge_sort_components(components)

    best_total, best_component = sorted_components[0]
    immediate_score = len(best_component) ** 2

    return best_component, immediate_score, best_total

# ==========================================================
# INSTRUCTIONS
# ==========================================================
def print_instructions():
    print("\n========= SAME GAME RULES =========")
    print("1. Select a cell (row, column)")
    print("2. Connected same-color blocks are removed")
    print("3. Score = (blocks removed)^2")
    print("4. Gravity applies after removal")
    print("5. CPU uses Optimal DP + Merge Sort")
    print("6. Game ends when no moves exist")
    print("==================================\n")

# ==========================================================
# SINGLE PLAYER (WITH FUTURE BEST SCORE DISPLAY)
# ==========================================================
def single_player():
    grid = GridADT(ROWS, COLS)
    score = 0
    print_instructions()

    while not is_game_over(grid):
        grid.display()

        # Show maximum possible achievable score from this state
        memo = {}
        max_possible = dp_best_score(grid, memo)

        print("Current Score:", score)
        print("Maximum Achievable Score From This State:", max_possible)
        print()

        try:
            r = int(input("Row: "))
            c = int(input("Column: "))
        except:
            print("Invalid input!")
            continue

        if r < 0 or r >= ROWS or c < 0 or c >= COLS:
            print("Out of bounds!")
            continue

        comp = get_component(grid, r, c)

        if len(comp) <= 1:
            print("Invalid Move!")
            continue

        gained = len(comp) ** 2
        score += gained

        remove_component(grid, comp)
        apply_gravity(grid)

        print("You gained:", gained)
        print()

    print("GAME OVER")
    print("Final Score:", score)

# ==========================================================
# MULTIPLAYER
# ==========================================================
def multiplayer():
    grid = GridADT(ROWS, COLS)
    human = cpu = 0
    print_instructions()

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

        print("CPU thinking...")
        cpu_comp, immediate_score, max_future = cpu_best_move(grid)

        print("Maximum Achievable Score From This State:", max_future)

        cpu += immediate_score
        remove_component(grid, cpu_comp)
        apply_gravity(grid)

        print("CPU gained:", immediate_score)
        print("CPU played...\n")

    print("GAME OVER")
    print("Human:", human, "| CPU:", cpu)
    print("Winner:", "Human 🎉" if human > cpu else "CPU 🤖")

# ==========================================================
# MAIN MENU
# ==========================================================
# ==========================================================
# MAIN MENU
# ==========================================================
def main_menu():
    while True:
        print("\n====== SAME GAME MENU ======")
        print("1. Single Player (With Optimal Future Score Display)")
        print("2. Multiplayer (CPU Optimal)")
        print("3. Instructions")
        print("4. Exit")

        ch = input("Choice: ")

        if ch == '1':
            single_player()   # <-- calls the updated DP version
        elif ch == '2':
            multiplayer()
        elif ch == '3':
            print_instructions()
        elif ch == '4':
            print("Thanks for playing!")
            break
        else:
            print("Invalid choice!")

# ==========================================================
# START
# ==========================================================
main_menu()
