# ==========================================================
# SAME GAME - ADT & DSA BASED IMPLEMENTATION
# ==========================================================
# ADTs USED:
# 1. Grid ADT        -> 2D List (Board)
# 2. Graph ADT       -> Implicit Grid Graph
# 3. Stack ADT       -> Iterative DFS + Gravity
# 4. Set ADT         -> Visited Nodes
# 5. List ADT        -> Connected Components
# 6. Greedy + Merge Sort -> CPU Move Selection
# 7. Backtracking    -> Optimal Move Search
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
                # FIXED: Explicit None check instead of truthiness
                print(self.board[r][c] if self.board[r][c] is not None else '.', end=" ")
            print()
        print()

# ==========================================================
# GRAPH ADT (IMPLICIT GRID GRAPH)
# ==========================================================
class GraphADT:
    @staticmethod
    def neighbors(r, c):
        # Cleaner order: up, down, left, right
        return [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]

# ==========================================================
# ITERATIVE DFS (STACK-BASED)
# ==========================================================
def dfs(grid, r, c, color, visited, component):
    """Iterative DFS using stack ADT - no recursion, safe for large boards"""
    stack = [(r, c)]

    while stack:
        cr, cc = stack.pop()

        # Check bounds first (more efficient)
        if cr < 0 or cr >= grid.rows or cc < 0 or cc >= grid.cols:
            continue

        if (cr, cc) in visited:
            continue

        if grid.board[cr][cc] != color:
            continue

        visited.add((cr, cc))
        component.append((cr, cc))

        for nr, nc in GraphADT.neighbors(cr, cc):
            stack.append((nr, nc))

# ==========================================================
# GET COMPONENT - With boundary safety
# ==========================================================
def get_component(grid, r, c):
    """Get connected component with full boundary safety"""
    if r < 0 or r >= grid.rows or c < 0 or c >= grid.cols:
        return []

    if grid.board[r][c] is None:
        return []

    visited = set()
    component = []
    dfs(grid, r, c, grid.board[r][c], visited, component)
    return component

# ==========================================================
# GET COMPONENT - WITH BOUNDARY SAFETY (Alias for compatibility)
# ==========================================================
def get_component_safe(grid, r, c):
    """Alias for get_component (both are now safe)"""
    return get_component(grid, r, c)

# ==========================================================
# GET ALL COMPONENTS
# ==========================================================
def get_all_components(grid):
    """Returns list of all valid components (size > 1) on the board"""
    visited = set()
    components = []
    
    for r in range(grid.rows):
        for c in range(grid.cols):
            if grid.board[r][c] is not None and (r, c) not in visited:
                comp = []
                dfs(grid, r, c, grid.board[r][c], visited, comp)
                if len(comp) > 1:
                    components.append(comp)
    
    return components

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
    for c in range(grid.cols):
        stack = []

        # Use explicit None check
        for r in range(grid.rows):
            if grid.board[r][c] is not None:
                stack.append(grid.board[r][c])

        for r in range(grid.rows - 1, -1, -1):
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
# GAME OVER CHECK - FIXED: Explicit None check
# ==========================================================
def is_game_over(grid):
    """Check if game is over by finding if any valid component exists"""
    visited = set()

    for r in range(grid.rows):
        for c in range(grid.cols):
            # FIXED: Use explicit None check instead of truthiness
            if grid.board[r][c] is not None and (r, c) not in visited:
                comp = []
                dfs(grid, r, c, grid.board[r][c], visited, comp)
                if len(comp) > 1:
                    return False
    
    return True

# ==========================================================
# HELPER FUNCTION: DUPLICATE COPY OF THE GRID (Optimized)
# ==========================================================
def copy_grid(grid):
    """Optimized copy that avoids unnecessary random board generation"""
    new_grid = GridADT.__new__(GridADT)
    new_grid.rows = grid.rows
    new_grid.cols = grid.cols
    new_grid.board = [row[:] for row in grid.board]
    return new_grid

# ==========================================================
# CHECK IF BOARD IS COMPLETELY EMPTY
# ==========================================================
def is_board_empty(grid):
    """Check if every cell is None - using generator expression"""
    return all(cell is None for row in grid.board for cell in row)

# ==========================================================
# MERGE SORT FOR CPU MOVE SELECTION
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
# BACKTRACKING MAX SCORE
# ==========================================================
def backtrack_max_score(grid, current_score):
    """
    Recursive backtracking to find maximum possible score from current state
    Note: For boards larger than 8x8, this may be slow
    """
    # Base case: no moves left
    if is_game_over(grid):
        return current_score
    
    best_score = current_score
    components = get_all_components(grid)
    
    # Try every possible move
    for comp in components:
        # Simulate the move
        sim = copy_grid(grid)
        remove_component(sim, comp)
        apply_gravity(sim)
        
        # Calculate score for this move
        gain = len(comp) ** 2
        
        # Recursively explore future moves
        score = backtrack_max_score(sim, current_score + gain)
        
        # Track best score
        if score > best_score:
            best_score = score
    
    return best_score

# ==========================================================
# BACKTRACKING BEST MOVE
# ==========================================================
def backtracking_best_move(grid):
    """
    Find the best first move using backtracking
    Returns the component that leads to maximum final score
    """
    components = get_all_components(grid)
    
    if not components:
        return None
    
    best_score = -1
    best_component = None
    
    # Evaluate each possible first move
    for comp in components:
        # Simulate this move
        sim = copy_grid(grid)
        remove_component(sim, comp)
        apply_gravity(sim)
        
        # Calculate immediate gain
        gain = len(comp) ** 2
        
        # Use backtracking to find final score from this state
        final_score = backtrack_max_score(sim, gain)
        
        # Track best move
        if final_score > best_score:
            best_score = final_score
            best_component = comp
    
    return best_component

# ==========================================================
# BACKTRACKING HINT - With size check
# ==========================================================
def get_backtracking_hint(grid):
    """
    Provide hint using backtracking
    Only used for small boards (≤ 8x8) to prevent slowdown
    """
    if grid.rows * grid.cols > 64:  # 8x8 = 64 cells
        print("  Board too large for backtracking hint (using fast hint instead)")
        return None, 0
    
    best_component = backtracking_best_move(grid)
    
    if best_component:
        return best_component[0], len(best_component) ** 2
    return None, 0

# ==========================================================
# DP SCORE DIFFERENCE - Turn-aware optimal evaluation
# ==========================================================
def dp_score_difference(grid, memo, is_cpu_turn):
    """
    Returns maximum score DIFFERENCE (current player - opponent)
    from this board state.
    """
    # Using map(tuple) for faster conversion
    board_tuple = tuple(map(tuple, grid.board))
    state = (board_tuple, is_cpu_turn)

    if state in memo:
        return memo[state]

    components = get_all_components(grid)

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
# HINT STRATEGY (Fast DP-based)
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

    # None check before returning
    if best_component is None:
        return None, 0

    return best_component[0], len(best_component) ** 2

# ==========================================================
# DIVIDING STRATEGY (Heuristic - regions may interact after gravity)
# ==========================================================
def divide_board_regions(grid):
    """
    DIVIDE PHASE (Heuristic):
    Split board into column regions separated by empty columns.
    Note: This is a heuristic - regions may still interact after gravity shifts columns.
    """
    regions = []
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
                regions.append(current_region)
                current_region = []

    if current_region:
        regions.append(current_region)

    return regions

# ==========================================================
# CONQUERING STRATEGY
# ==========================================================
def conquer_region(grid, region_cols, memo):
    """
    CONQUER PHASE:
    Evaluate best move inside one region.
    Uses turn-aware DP.
    """
    # Safety check: empty region
    if not region_cols:
        return None, float('-inf')

    best_component = None
    best_value = float('-inf')

    components = get_all_components(grid)

    # Only consider components fully inside the region columns
    region_components = [
        comp for comp in components
        if all(c in region_cols for r, c in comp)
    ]

    for comp in region_components:
        sim = copy_grid(grid)
        remove_component(sim, comp)
        apply_gravity(sim)

        gain = len(comp) ** 2

        # Opponent turn next
        future = dp_score_difference(sim, memo, False)

        value = gain - future

        if value > best_value:
            best_value = value
            best_component = comp

    return best_component, best_value

# ==========================================================
# COMBINING PHASE
# ==========================================================
def combine_results(results):
    """
    COMBINE PHASE:
    Select best move among all region results.
    """

    best_component = None
    best_value = float('-inf')

    for comp, value in results:
        if comp is not None and value > best_value:
            best_value = value
            best_component = comp

    return best_component

# ==========================================================
# GREEDY CPU MOVE (MERGE SORT BASED) - FIXED: Explicit None check
# ==========================================================
def cpu_best_move_greedy(grid):
    """Simple greedy CPU move using merge sort - avoids duplicate components"""
    components = []
    visited = set()

    for r in range(grid.rows):
        for c in range(grid.cols):
            # FIXED: Use explicit None check instead of truthiness
            if grid.board[r][c] is not None and (r, c) not in visited:
                comp = []
                dfs(grid, r, c, grid.board[r][c], visited, comp)
                
                if len(comp) > 1:
                    score = len(comp) ** 2
                    components.append((score, comp))

    if not components:
        return None

    sorted_components = merge_sort_components(components)
    best_score, best_component = sorted_components[0]

    return best_component

# ==========================================================
# OPTIMAL CPU MOVE (HEURISTIC DIVIDE & CONQUER + DP)
# ==========================================================
def cpu_best_move(grid):
    """
    CPU MOVE USING HEURISTIC DIVIDE & CONQUER + DP
    - DIVIDE: Heuristically split into column regions (may interact after gravity)
    - CONQUER: Evaluate each region with turn-aware DP
    - COMBINE: Select best overall move from all regions
    """
    print("\n" + "="*50)
    print("CPU TURN - HEURISTIC DIVIDE & CONQUER + DP")
    print("="*50)

    memo = {}

    # -------- PHASE 1: DIVIDE --------
    print("\n🔹 PHASE 1: DIVIDE (Heuristic)")
    regions = divide_board_regions(grid)
    
    # Safety check: no regions found
    if not regions:
        print("[RESULT] No valid regions found")
        print("="*50)
        return None

    # -------- PHASE 2: CONQUER --------
    print("\n🔹 PHASE 2: CONQUER")
    results = []

    for i, region_cols in enumerate(regions):
        print(f"\n--- Region {i} (cols {region_cols}) ---")
        comp, value = conquer_region(grid, region_cols, memo)
        
        # Only append non-None components
        if comp is not None:
            results.append((comp, value))

    # -------- PHASE 3: COMBINE --------
    print("\n🔹 PHASE 3: COMBINE")
    
    # FIXED: Check if results is empty before combining
    if not results:
        print("[RESULT] No valid moves found")
        print("="*50)
        return None
    
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
    print("5. CPU uses HEURISTIC DIVIDE & CONQUER + Dynamic Programming")
    print("   - DIVIDE: Heuristically split board into column regions")
    print("   - CONQUER: Evaluate each region with turn-aware DP")
    print("   - COMBINE: Select best region")
    print("6. Game ends when no moves exist")
    print("7. In Multiplayer mode, you can ask for hints!")
    print("   - Fast hint (DP-based)")
    print("   - Optimal hint (Backtracking - best for small boards)")
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
# SINGLE PLAYER MODE - With complete input validation
# ==========================================================
def single_player():
    select_board_size()
    grid = GridADT(ROWS, COLS)
    score = 0
    print_instructions()

    while not is_game_over(grid):
        grid.display()
        print("Score:", score)

        # Input validation
        try:
            r = int(input("Row: "))
            c = int(input("Column: "))
        except ValueError:
            print("Invalid input! Please enter numbers.")
            continue
        
        # Bounds checking
        if r < 0 or r >= grid.rows or c < 0 or c >= grid.cols:
            print("Invalid coordinates! Please enter values within board range.")
            continue

        comp = get_component(grid, r, c)
        if len(comp) <= 1:
            print("Invalid Move! Select a cell that is part of a group of 2 or more.")
            continue

        score += len(comp) ** 2
        remove_component(grid, comp)
        apply_gravity(grid)
        
        # Check if board became completely empty
        if is_board_empty(grid):
            break

    print("GAME OVER | Final Score:", score)

# ==========================================================
# MULTIPLAYER MODE - With complete input validation
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
        choice = input("Do you want a hint? (y/n): ").lower()
        if choice == 'y':
            print("\nChoose hint type:")
            print("1. Fast hint (DP-based) - works for all board sizes")
            print("2. Optimal hint (Backtracking) - best for small boards (≤ 8x8)")
            hint_type = input("Choice (1 or 2): ")
            
            if hint_type == '1':
                hint_cell, hint_score = get_optimal_hint(grid)
                hint_name = "Fast DP-based"
            else:
                hint_cell, hint_score = get_backtracking_hint(grid)
                hint_name = "Optimal Backtracking"
                # If backtracking returned None (board too large), fall back to DP
                if hint_cell is None:
                    print("  Falling back to fast hint...")
                    hint_cell, hint_score = get_optimal_hint(grid)
                    hint_name = "Fast DP-based (fallback)"
            
            if hint_cell:
                print(f"\n[{hint_name} Hint] Optimal Move → Row {hint_cell[0]}, Column {hint_cell[1]}")
                print(f"Immediate Score: {hint_score}")
                print("Following hints maximizes your score.\n")

        # -------- HUMAN MOVE --------
        try:
            r = int(input("Row: "))
            c = int(input("Column: "))
        except ValueError:
            print("Invalid input! Please enter numbers.")
            continue
        
        # Bounds checking
        if r < 0 or r >= grid.rows or c < 0 or c >= grid.cols:
            print("Invalid coordinates! Please enter values within board range.")
            continue

        comp = get_component(grid, r, c)
        if len(comp) <= 1:
            print("Invalid Move! Select a cell that is part of a group of 2 or more.")
            continue

        human += len(comp) ** 2
        remove_component(grid, comp)
        apply_gravity(grid)

        if is_game_over(grid) or is_board_empty(grid):
            break

        # -------- CPU MOVE --------
        cpu_comp = cpu_best_move(grid)
        if cpu_comp is not None:
            gain = len(cpu_comp) ** 2
            cpu += gain
            remove_component(grid, cpu_comp)
            apply_gravity(grid)
            print(f"CPU removed {len(cpu_comp)} blocks for {gain} points!\n")
        else:
            print("CPU has no valid moves!\n")
            break

    print("GAME OVER")
    print("Human:", human, "| CPU:", cpu)
    if human > cpu:
        print("Winner: Human 🎉")
    elif cpu > human:
        print("Winner: CPU 🤖")
    else:
        print("It's a tie!")

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
if __name__ == "__main__":
    main_menu()
