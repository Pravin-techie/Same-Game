# ==========================================================
# SAME GAME - ADT & DSA BASED IMPLEMENTATION
# ==========================================================
# ADTs USED:
# 1. Grid ADT        -> 2D List (Board)
# 2. Graph ADT       -> Implicit Grid Graph
# 3. Stack ADT       -> DFS + Gravity
# 4. Set ADT         -> Visited Nodes
# 5. List ADT        -> Connected Components
# 6. Greedy + Merge Sort -> CPU Move Selection
# ==========================================================

import random

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
    """Abstract Data Type for Game Board"""

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
# GRAPH ADT (IMPLICIT GRID GRAPH)
# ==========================================================
class GraphADT:
    @staticmethod
    def neighbors(r, c):
        return [(r+1, c), (r-1, c), (r, c+1), (r, c-1)]

# ==========================================================
# BFS (CONNECTED COMPONENT)
# ==========================================================
def bfs(grid, r, c, color, visited, component):
    if r < 0 or r >= ROWS or c < 0 or c >= COLS:
        return
    if (r, c) in visited:
        return
    if grid.board[r][c] != color:
        return

    visited.add((r, c))
    component.append((r, c))

    for nr, nc in GraphADT.neighbors(r, c):
        bfs(grid, nr, nc, color, visited, component)

def get_component(grid, r, c):
    if grid.board[r][c] is None:
        return []

    visited = set()
    component = []
    bfs(grid, r, c, grid.board[r][c], visited, component)
    return component

# ==========================================================
# REMOVE COMPONENT
# ==========================================================
def remove_component(grid, component):
    for r, c in component:
        grid.board[r][c] = None

# ==========================================================
# GRAVITY USING STACK ADT
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
# GAME OVER CHECK
# ==========================================================
def is_game_over(grid):
    for r in range(ROWS):
        for c in range(COLS):
            if grid.board[r][c]:
                if len(get_component(grid, r, c)) > 1:
                    return False
    return True

# ==========================================================
# MERGE SORT FOR CPU MOVE SELECTION
# ==========================================================
""" def merge(left, right):
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

    return result """ # completed for part for evaluation 1

""" def merge_sort_components(components):
    if len(components) <= 1:
        return components

    mid = len(components) // 2
    left = merge_sort_components(components[:mid])
    right = merge_sort_components(components[mid:])

    return merge(left, right) """ # completed part for evaluation 1

# ==========================================================
# GREEDY CPU MOVE (MERGE SORT BASED)
# ==========================================================
""" def cpu_best_move(grid):
    components = []

    for r in range(ROWS):
        for c in range(COLS):
            if grid.board[r][c]:
                comp = get_component(grid, r, c)
                if len(comp) > 1:
                    score = len(comp) ** 2
                    components.append((score, comp))

    if not components:
        return []

    sorted_components = merge_sort_components(components)
    best_score, best_component = sorted_components[0]

    return best_component """ # completed part for evaluation 1
#  FUNCTION 2: DP SCORE DIFFERENCE - Turn-aware optimal evaluation
def dp_score_difference(grid, memo, is_cpu_turn):
    """
    Returns maximum score DIFFERENCE (current player - opponent)
    from this board state.
    """

    state = (tuple(tuple(row) for row in grid.board), is_cpu_turn)

    if state in memo:
        return memo[state]

    components = divide_moves(grid)

    if not components:
        return 0

    if is_cpu_turn:
        best = float('-inf')
        for comp in components:
            sim = copy_grid(grid)
            remove_component(sim, comp)
            apply_gravity(sim)

            gain = len(comp) ** 2
            future = dp_score_difference(sim, memo, False)

            best = max(best, gain - future)

        memo[state] = best
        return best

    else:
        worst = float('inf')
        for comp in components:
            sim = copy_grid(grid)
            remove_component(sim, comp)
            apply_gravity(sim)

            gain = len(comp) ** 2
            future = dp_score_difference(sim, memo, True)

            worst = min(worst, future - gain)

        memo[state] = worst
        return worst

# FUNCTION 3: CPU MOVE - Using turn-aware adversarial DP
def cpu_best_move(grid):
    """
    CPU MOVE USING Divide & Conquer + DP
    Turn-aware adversarial score difference evaluation.
    """
    
    memo = {}
    components = divide_moves(grid)
    
    if not components:
        return []
    
    best_component = []
    best_value = float('-inf')
    
    for comp in components:
        sim = copy_grid(grid)
        remove_component(sim, comp)
        apply_gravity(sim)
        
        gain = len(comp) ** 2
        value = gain - dp_score_difference(sim, memo, False)
        
        if value > best_value:
            best_value = value
            best_component = comp
    
    return best_component

# ==========================================================
# INSTRUCTIONS
# ==========================================================
def print_instructions():
    print("\n========= SAME GAME RULES =========")
    print("1. Select a cell (row, column)")
    print("2. Connected same-color blocks are removed")
    print("3. Score = (blocks removed)^2")
    print("4. Gravity applies after removal")
    print("5. CPU uses Greedy + Merge Sort")
    print("6. Game ends when no moves exist")
    print("==================================\n")

# ==========================================================
# BOARD SIZE MENU
# ==========================================================
def select_board_size():
    global ROWS, COLS

    print("\n--- SELECT BOARD SIZE ---")
    print("1. 5 x 5")
    print("2. 10 x 5")
    print("3. 15 x 10")
    print("4. 20 x 5")

    choice = input("Choice: ")

    if choice == '1':
        ROWS, COLS = 5, 5
    elif choice == '2':
        ROWS, COLS = 10, 5
    elif choice == '3':
        ROWS, COLS = 15, 10
    elif choice == '4':
        ROWS, COLS = 20, 5
    else:
        ROWS, COLS = 5, 5

# ==========================================================
# SINGLE PLAYER MODE
# ==========================================================
def single_player():
    select_board_size()
    grid = GridADT(ROWS, COLS)
    score = 0
    print_instructions()

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
# MULTIPLAYER MODE
# ==========================================================
def multiplayer():
    select_board_size()
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
        print("3. Instructions")
        print("4. Exit")

        ch = input("Choice: ")

        if ch == '1':
            single_player()
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
# PROGRAM START
# ==========================================================
main_menu()




