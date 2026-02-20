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
# GET COMPONENT - WITH BOUNDARY SAFETY - S SRIJITH CSE24044
# ==========================================================
def get_component(grid, r, c):
    """
    Get connected component at position (r,c) with boundary safety.
    """
    # Boundary safety check
    if r < 0 or r >= grid.rows or c < 0 or c >= grid.cols:
        return []
    
    # Empty cell check
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
    # Vertical Shift
    for c in range(COLS):
        stack = []

        for r in range(ROWS):
            if grid.board[r][c]:
                stack.append(grid.board[r][c])

        for r in range(ROWS-1, -1, -1):
            grid.board[r][c] = stack.pop() if stack else None
  # Horizontal Shift 
    write_col = 0
    for read_col in range(grid.cols):
        column_has_block = any(
            grid.board[r][read_col] is not None
            for r in range(grid.rows)
        )
        
        if column_has_block:
            if write_col != read_col:
                for r in range(grid.rows):
                    grid.board[r][write_col] = grid.board[r][read_col]
                    grid.board[r][read_col] = None
            write_col += 1

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
# HELPER FUNCTION: DUPLICATE COPY OF THE GRID
# ==========================================================
def copy_grid(grid):
    new_grid = GridADT(grid.rows, grid.cols)
    new_grid.board = [row[:] for row in grid.board]
    return new_grid

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

#CSE24058 VIDHYADHARAN RP
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

# ==========================================================
# HINT STRATERGY - VIJAY SATHAPPAN CSE24059
# ==========================================================

def get_optimal_hint(grid):
    memo = {}
    components = get_all_components(grid)
    
    if not components:
        return None, 0
    
    best_component = None
    best_total = -1
    
    for comp in components:
        sim = copy_grid(grid)
        remove_component(sim, comp)
        apply_gravity(sim)
        
        future = -dp_score_difference(sim, memo, True)
        total = len(comp) ** 2 + future
        
        if total > best_total:
            best_total = total
            best_component = comp
    
    return best_component[0], len(best_component) ** 2

# ==========================================================
# DIVIDING STRATERGY - VIJAY CSE24059
# ==========================================================

def divide_board_regions(grid):
    
    independent_regions = []
    current_region = []

    for c in range(grid.cols):
        column_has_block = any(
            grid.board[r][c] is not None
            for r in range(grid.rows)
        )

        if column_has_block:
            current_region.append(c)
        else:
            if current_region:
                independent_regions.append(current_region)
                current_region = []

    if current_region:
        independent_regions.append(current_region)

    print(f"\n[DIVIDE] Independent column regions: {independent_regions}")
    return independent_regions
    
# ==========================================================
# CONQUERING STRATEGY - PRAVIN R CSE24037                
# ==========================================================
def conquer_region(grid, region_components, memo):
    """
    CONQUER PHASE:
    Evaluate each component in a region using turn-aware DP.
    Returns the best component from this region and its value.
    """
    if not region_components:
        return [], float('-inf')
    
    best_component = []
    best_value = float('-inf')

    print(f"\n[CONQUER] Evaluating {len(region_components)} components in region...")
    
    for comp in region_components:
        sim = copy_grid(grid)
        remove_component(sim, comp)
        apply_gravity(sim)

        gain = len(comp) ** 2
        future = dp_score_difference(sim, memo, False)  # After CPU move, human's turn
        value = gain - future

        if value > best_value:
            best_value = value
            best_component = comp

    print(f"[CONQUER] Best component score difference: {best_value}")
    return best_component, best_value

# ==========================================================
# COMBINING RESULTS - S SRIJITH CSE24044
# ==========================================================
def combine_results(results):
    """
    COMBINE PHASE:
    Select best move among all independent regions.
    """
    best_component = None
    best_value = float('-inf')
    best_region_idx = -1

    for i, (comp, value) in enumerate(results):
        if value > best_value:
            best_value = value
            best_component = comp
            best_region_idx = i

    print(f"[COMBINE] Selected region {best_region_idx} with value: {best_value}")
    return best_component

#CSE24058 VIDHYADHARAN RP
def cpu_best_move(grid):
    """
    CPU MOVE USING TRUE DIVIDE & CONQUER + DP
    - DIVIDE: Split into independent column regions (separated by empty columns)
    - CONQUER: Evaluate each region independently with turn-aware DP
    - COMBINE: Select best overall move from all regions
    """
    print("\n" + "="*50)
    print("CPU TURN - TRUE DIVIDE & CONQUER + DP")
    print("="*50)
    
    memo = {}
    
    # -------- PHASE 1: DIVIDE --------
    print("\n🔹 PHASE 1: DIVIDE")
    regions = divide_board_regions(grid)
    
    # -------- PHASE 2: CONQUER --------
    print("\n🔹 PHASE 2: CONQUER")
    results = []
    
    for i, region_cols in enumerate(regions):
        print(f"\n--- Region {i} (cols {region_cols}) ---")
        comp, value = conquer_region(grid, region_cols, memo)
        results.append((comp, value))
    
    # -------- PHASE 3: COMBINE --------
    print("\n🔹 PHASE 3: COMBINE")
    best_component = combine_results(results)
    
    if best_component:
        print(f"[RESULT] Selected component of size {len(best_component)} at {best_component[0]}")
    else:
        print("[RESULT] No valid moves found")
    
    print("="*50)
    return best_component

# ==========================================================
# INSTRUCTIONS
# ==========================================================
def print_instructions():
    print("\n========= SAME GAME RULES =========")
    print("1. Select a cell (row, column)")
    print("2. Connected same-color blocks are removed")
    print("3. Score = (blocks removed)^2")
    print("4. Gravity applies after removal (vertical drop + horizontal shift)")
    print("5. CPU uses VISIBLE DIVIDE & CONQUER + Dynamic Programming")
    print("   - DIVIDE: Split board into Left/Right regions")
    print("   - CONQUER: Evaluate each region with turn-aware DP")
    print("   - COMBINE: Select best region")
    print("6. Game ends when no moves exist")
    print("7. In Multiplayer mode, you can ask for optimal hints!")
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

        # HUMAN HINT OPTION
        choice = input("Do you want optimal hint? (y/n): ").lower()
        if choice == 'y':
            hint_cell, hint_score = get_optimal_hint(grid)
            if hint_cell:
                print(f"Optimal Move → Row {hint_cell[0]}, Column {hint_cell[1]}")
                print(f"Immediate Score: {hint_score}")
                print("Following hints every turn gives maximum possible score.\n")

        # -------- HUMAN MOVE --------
        try:
            r = int(input("Row: "))
            c = int(input("Column: "))
        except ValueError:
            print("Invalid input! Please enter numbers.")
            continue

        comp = get_component(grid, r, c)
        if len(comp) <= 1:
            print("Invalid Move! Select a cell that is part of a group of 2 or more.")
            continue

        human += len(comp) ** 2
        remove_component(grid, comp)
        apply_gravity(grid)

        if is_game_over(grid):
            break

        # -------- CPU MOVE --------
        cpu_comp = cpu_best_move(grid)
        if cpu_comp:  # Check if CPU has a valid move
            cpu += len(cpu_comp) ** 2
            remove_component(grid, cpu_comp)
            apply_gravity(grid)
            print("CPU played with D&C strategy!\n")
        else:
            print("CPU has no valid moves!\n")
            break

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














