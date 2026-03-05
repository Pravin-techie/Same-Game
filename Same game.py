# ==========================================================
# SAME GAME - ADT & DSA BASED IMPLEMENTATION
# ==========================================================
# ADTs USED:
# 1. Grid ADT        -> 2D List (Board)
# 2. Graph ADT       -> Implicit Grid Graph
# 3. Stack ADT       -> DFS + Gravity
# 4. Set ADT         -> Visited Nodes
# 5. List ADT        -> Connected Components
# 6. Multiple Strategies:
#    - Greedy (Merge Sort based)
#    - Divide & Conquer + Dynamic Programming
#    - Backtracking + Memoization
# ==========================================================

import random
import time

# -------------------------------
# GLOBAL GAME VARIABLES
# -------------------------------
ROWS = 6
COLS = 6
COLORS = ['R', 'G', 'B', 'Y']
STRATEGY_MODE = "dc_dp"  # Default strategy

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
                print(self.board[r][c] if self.board[r][c] is not None else '.', end=" ")
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
# DFS (CONNECTED COMPONENT) - Renamed from BFS
# ==========================================================
def dfs(grid, r, c, color, visited, component):
    """DFS to find connected component"""
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
    dfs(grid, r, c, grid.board[r][c], visited, component)
    return component

# ==========================================================
# GET ALL COMPONENTS - Added missing function
# ==========================================================
def get_all_components(grid):
    """
    Returns list of all connected components (size > 1) on the board
    """
    visited = set()
    components = []

    for r in range(grid.rows):
        for c in range(grid.cols):
            if (r, c) in visited:
                continue
            if grid.board[r][c] is None:
                continue

            comp = []
            dfs(grid, r, c, grid.board[r][c], visited, comp)

            if len(comp) > 1:  # Only keep removable components
                components.append(comp)

    return components

# ==========================================================
# REMOVE COMPONENT
# ==========================================================
def remove_component(grid, component):
    for r, c in component:
        grid.board[r][c] = None

# ==========================================================
# GRAVITY USING STACK ADT - Fixed with grid.rows/grid.cols
# ==========================================================
def apply_gravity(grid):
    # Vertical Shift
    for c in range(grid.cols):
        stack = []

        for r in range(grid.rows):
            if grid.board[r][c] is not None:
                stack.append(grid.board[r][c])

        for r in range(grid.rows-1, -1, -1):
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
# GAME OVER CHECK - Fixed with get_all_components
# ==========================================================
def is_game_over(grid):
    components = get_all_components(grid)
    return len(components) == 0

# ==========================================================
# HELPER FUNCTION: DUPLICATE COPY OF THE GRID - Fixed
# ==========================================================
def copy_grid(grid):
    """Create a deep copy of the grid"""
    new_grid = GridADT.__new__(GridADT)
    new_grid.rows = grid.rows
    new_grid.cols = grid.cols
    new_grid.board = [row[:] for row in grid.board]
    return new_grid

# ==========================================================
# STRATEGY 1: GREEDY (Optimized with visited set)
# CSE24044 - S SRIJITH
# ==========================================================
def greedy_best_move(grid):
    """
    Greedy Strategy:
    - Find all components using visited set
    - Sort by score (size^2) in descending order
    - Pick the largest component
    """
    visited = set()
    components = []

    for r in range(grid.rows):
        for c in range(grid.cols):
            if (r, c) in visited:
                continue
            if grid.board[r][c] is None:
                continue

            comp = []
            dfs(grid, r, c, grid.board[r][c], visited, comp)

            if len(comp) > 1:
                score = len(comp) ** 2
                components.append((score, comp))

    if not components:
        return None

    components.sort(reverse=True, key=lambda x: x[0])
    
    best_score, best_component = components[0]
    print(f"Greedy selected: size {len(best_component)} with score {best_score}")
    
    return best_component



# ==========================================================
# ====== STRATEGY 2: DIVIDE & CONQUER + DP ALGORITHM ======
# ==========================================================
# PASTE DC+DP FUNCTIONS HERE:
# 1. dp_score_difference(grid, memo, is_cpu_turn)
# 2. divide_board_regions(grid)
# 3. conquer_region(grid, region_cols, memo)
# 4. combine_results(results)
# 5. cpu_best_move_dc_dp(grid)
# ==========================================================

# ==========================================================
# DP SCORE DIFFERENCE - Turn-aware optimal evaluation
# CSE24058 VIDHYADHARAN RP
# ==========================================================
def dp_score_difference(grid, memo, is_cpu_turn):
    """
    Returns maximum score DIFFERENCE (current player - opponent)
    from this board state.
    """
    state = (tuple(tuple(row) for row in grid.board), is_cpu_turn)

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
# DIVIDE BOARD REGIONS
# CSE24059 VIJAY SATHAPPAN
# ==========================================================
def divide_board_regions(grid):
    """
    DIVIDING STRATEGY - VIJAY CSE24059
    Split board into independent column regions
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
# CONQUER REGION
# CSE24037 PRAVIN R
# ==========================================================
def conquer_region(grid, region_cols, memo):
    """
    CONQUERING STRATEGY - PRAVIN R CSE24037
    Evaluate best move inside one independent region
    """
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
        future = dp_score_difference(sim, memo, False)
        value = gain - future

        if value > best_value:
            best_value = value
            best_component = comp

    return best_component, best_value

# ==========================================================
# COMBINE RESULTS
# CSE24044 S SRIJITH
# ==========================================================
def combine_results(results):
    """
    COMBINING PHASE - S SRIJITH CSE24044
    Select best move among all region results
    """
    best_component = None
    best_value = float('-inf')

    for comp, value in results:
        if comp is not None and value > best_value:
            best_value = value
            best_component = comp

    return best_component



# ==========================================================
# ========== STRATEGY 3: BACKTRACKING + MEMOIZATION =======
# ==========================================================
# PASTE BACKTRACKING FUNCTIONS HERE:
# 1. backtracking_score(grid)
# 2. backtracking_best_move(grid)
# ==========================================================

# ==========================================================
# BACKTRACKING SCORE
# CSE24058 & 37 - [Vidhyadharan & Pravin]
# ==========================================================
backtrack_cache = {}

def backtracking_score(grid):
    """
    Recursive backtracking to find maximum possible score
    """
    state = tuple(tuple(row) for row in grid.board)

    if state in backtrack_cache:
        return backtrack_cache[state]

    components = get_all_components(grid)

    if not components:
        return 0

    best = 0

    for comp in components:
        sim = copy_grid(grid)
        remove_component(sim, comp)
        apply_gravity(sim)

        gain = len(comp) ** 2
        future = backtracking_score(sim)
        total = gain + future

        best = max(best, total)

    backtrack_cache[state] = best
    return best

# ==========================================================
# BACKTRACKING BEST MOVE
# CSE24059 & 44 - [Vijay Sathappan & Srijith]
# ==========================================================
def backtracking_best_move(grid):
    """
    Backtracking Strategy:
    - Try all possible moves recursively
    - Use memoization to cache results
    - Return move that leads to maximum total score
    """
    global backtrack_cache
    backtrack_cache = {}

    components = get_all_components(grid)
    
    if not components:
        return None

    best_component = None
    best_total = -1

    print("\n" + "="*50)
    print("BACKTRACKING + MEMOIZATION")
    print("="*50)
    
    for comp in components:
        sim = copy_grid(grid)
        remove_component(sim, comp)
        apply_gravity(sim)

        gain = len(comp) ** 2
        future = backtracking_score(sim)
        total = gain + future

        print(f"Component at {comp[0]}: immediate={gain}, future={future:.2f}, total={total:.2f}")

        if total > best_total:
            best_total = total
            best_component = comp

    if best_component:
        print(f"[RESULT] Selected component of size {len(best_component)} at {best_component[0]}")
    
    print("="*50)
    return best_component

# ==========================================================
# HINT STRATEGY - VIJAY SATHAPPAN CSE24059 - FIXED
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
        
        # FIXED: After human move, CPU plays next (is_cpu_turn=False)
        future = -dp_score_difference(sim, memo, False)
        total = len(comp) ** 2 + future
        
        if total > best_total:
            best_total = total
            best_component = comp
    
    if best_component is None:
        return None, 0
    
    return best_component[0], len(best_component) ** 2

# ==========================================================
# CPU MOVE CONTROLLER
# ==========================================================
def cpu_best_move(grid):
    """Controller that selects the appropriate strategy"""
    
    if STRATEGY_MODE == "greedy":
        print("\n🤖 CPU Strategy: GREEDY")
        return greedy_best_move(grid)

    elif STRATEGY_MODE == "dc_dp":
        print("\n🤖 CPU Strategy: DIVIDE & CONQUER + DP")
        return cpu_best_move_dc_dp(grid)

    elif STRATEGY_MODE == "backtracking":
        print("\n🤖 CPU Strategy: BACKTRACKING + MEMOIZATION")
        return backtracking_best_move(grid)

    else:
        print("\n🤖 CPU Strategy: Default (DC+DP)")
        return cpu_best_move_dc_dp(grid)

# ==========================================================
# SELECT STRATEGY
# ==========================================================
def select_strategy():
    global STRATEGY_MODE

    print("\n" + "="*50)
    print("SELECT CPU STRATEGY")
    print("="*50)
    print("1. Greedy Strategy")
    print("2. Divide & Conquer + Dynamic Programming")
    print("3. Backtracking + Memoization")
    print("="*50)

    choice = input("Choice (1-3): ")

    if choice == '1':
        STRATEGY_MODE = "greedy"
        print("✅ Greedy Strategy selected")
    elif choice == '2':
        STRATEGY_MODE = "dc_dp"
        print("✅ Divide & Conquer + DP selected")
    elif choice == '3':
        STRATEGY_MODE = "backtracking"
        print("✅ Backtracking + Memoization selected")
    else:
        print("❌ Invalid choice. Using Divide & Conquer + DP.")
        STRATEGY_MODE = "dc_dp"

# ==========================================================
# INSTRUCTIONS
# ==========================================================
def print_instructions():
    print("\n========= SAME GAME RULES =========")
    print("1. Select a cell (row, column)")
    print("2. Connected same-color blocks are removed")
    print("3. Score = (blocks removed)^2")
    print("4. Gravity applies after removal (vertical drop + horizontal shift)")
    print("5. CPU Strategy Selection:")
    print("   - Greedy: Largest component only")
    print("   - Divide & Conquer + DP: Optimal with region splitting")
    print("   - Backtracking + Memoization: Exhaustive search")
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
# SINGLE PLAYER MODE - With input validation
# ==========================================================
def single_player():
    select_board_size()
    grid = GridADT(ROWS, COLS)
    score = 0
    print_instructions()

    while not is_game_over(grid):
        grid.display()
        print("Score:", score)

        try:
            r = int(input("Row: "))
            c = int(input("Column: "))
        except ValueError:
            print("Invalid input! Please enter numbers.")
            continue

        if r < 0 or r >= grid.rows or c < 0 or c >= grid.cols:
            print("Invalid coordinates! Out of bounds.")
            continue

        comp = get_component(grid, r, c)
        if len(comp) <= 1:
            print("Invalid Move! Select a cell that is part of a group of 2 or more.")
            continue

        score += len(comp) ** 2
        remove_component(grid, comp)
        apply_gravity(grid)

    print("\n" + "="*50)
    print(f"GAME OVER | Final Score: {score}")
    print("="*50)

# ==========================================================
# MULTIPLAYER MODE - With strategy selection
# ==========================================================
def multiplayer():
    select_board_size()
    select_strategy()
    grid = GridADT(ROWS, COLS)
    human = cpu = 0
    print_instructions()

    while not is_game_over(grid):
        grid.display()
        print("Human:", human, "| CPU:", cpu)

        # HUMAN HINT OPTION
        choice = input("Do you want optimal hint? (y/n): ").lower()
        if choice == 'y':
            start_time = time.time()
            hint_cell, hint_score = get_optimal_hint(grid)
            end_time = time.time()
            
            if hint_cell is not None:
                print(f"\n💡 Optimal Move → Row {hint_cell[0]}, Column {hint_cell[1]}")
                print(f"💡 Immediate Score: {hint_score}")
                print(f"💡 Calculation time: {end_time - start_time:.2f}s\n")
            else:
                print("No hints available - game might be ending soon!\n")

        # -------- HUMAN MOVE --------
        try:
            r = int(input("\nYour move - Row: "))
            c = int(input("Your move - Column: "))
        except ValueError:
            print("Invalid input! Please enter numbers.")
            continue

        if r < 0 or r >= grid.rows or c < 0 or c >= grid.cols:
            print("Invalid coordinates! Out of bounds.")
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
        print("\n🤖 CPU thinking...")
        start_time = time.time()
        cpu_comp = cpu_best_move(grid)
        end_time = time.time()
        
        if cpu_comp is not None:
            cpu += len(cpu_comp) ** 2
            remove_component(grid, cpu_comp)
            apply_gravity(grid)
            print(f"✅ CPU played! (+{len(cpu_comp)**2} points)")
            print(f"⏱️  Thinking time: {end_time - start_time:.2f}s\n")
        else:
            print("CPU has no valid moves!\n")
            break

    print("\n" + "="*50)
    print("GAME OVER")
    print("="*50)
    print("Human:", human, "| CPU:", cpu)
    print("-"*20)
    if human > cpu:
        print("Winner: Human 🎉")
    elif cpu > human:
        print("Winner: CPU 🤖")
    else:
        print("It's a tie! 🤝")
    print("="*50)

# ==========================================================
# BENCHMARK MODE - With random seed fix
# ==========================================================
def benchmark_strategies():
    """Compare all three strategies on the same board"""
    print("\n" + "="*50)
    print("📊 BENCHMARK: Comparing All Strategies")
    print("="*50)
    
    # Save current random state
    current_seed = random.getstate()
    
    # Use fixed seed for reproducibility
    random.seed(42)
    grid = GridADT(6, 6)
    
    print("\nInitial Board:")
    grid.display()
    
    strategies = [
        ("Greedy", greedy_best_move),
        ("DC+DP", cpu_best_move_dc_dp),
        ("Backtracking", backtracking_best_move)
    ]
    
    results = []
    
    for name, strategy in strategies:
        print(f"\n{'-'*40}")
        print(f"Testing {name} Strategy...")
        
        # Copy the original grid
        test_grid = copy_grid(grid)
        score = 0
        moves = 0
        
        start_time = time.time()
        
        # Play until game over
        while not is_game_over(test_grid):
            move = strategy(test_grid)
            if move is None:
                break
            score += len(move) ** 2
            remove_component(test_grid, move)
            apply_gravity(test_grid)
            moves += 1
        
        end_time = time.time()
        
        results.append({
            'name': name,
            'score': score,
            'moves': moves,
            'time': end_time - start_time
        })
    
    # Restore random state
    random.setstate(current_seed)
    
    # Print comparison table
    print("\n" + "="*50)
    print("📊 BENCHMARK RESULTS")
    print("="*50)
    print(f"{'Strategy':<15} {'Score':<10} {'Moves':<10} {'Time (s)':<10}")
    print("-"*45)
    
    for r in results:
        print(f"{r['name']:<15} {r['score']:<10} {r['moves']:<10} {r['time']:<10.2f}")
    
    print("="*50)

# ==========================================================
# MAIN MENU
# ==========================================================
def main_menu():
    while True:
        print("\n====== SAME GAME MENU ======")
        print("1. Single Player")
        print("2. Multiplayer")
        print("3. Instructions")
        print("4. Benchmark Strategies")
        print("5. Exit")

        ch = input("Choice: ")

        if ch == '1':
            single_player()
        elif ch == '2':
            multiplayer()
        elif ch == '3':
            print_instructions()
        elif ch == '4':
            benchmark_strategies()
        elif ch == '5':
            print("Thanks for playing!")
            break
        else:
            print("Invalid choice!")

# ==========================================================
# PROGRAM START
# ==========================================================
if __name__ == "__main__":
    main_menu()






