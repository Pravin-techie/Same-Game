# ==========================================================
# SAME GAME - ADT & DSA BASED IMPLEMENTATION
# ==========================================================
# ADTs USED:
# 1. Grid ADT        -> 2D List (Board)
# 2. Graph ADT       -> Implicit Grid Graph
# 3. Stack ADT       -> DFS + Gravity
# 4. Set ADT         -> Visited Nodes
# 5. List ADT        -> Connected Components
# 6. Greedy ADT      -> CPU Move Selection
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
        """Create a random color grid"""
        return [[random.choice(COLORS) for _ in range(self.cols)]
                for _ in range(self.rows)]

    def display(self):
        """Display the board"""
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
    """Provides neighbors of a grid cell"""

    @staticmethod
    def neighbors(r, c):
        return [(r+1, c), (r-1, c), (r, c+1), (r, c-1)]

# ==========================================================
# DFS USING STACK + BACKTRACKING
# ==========================================================
def dfs(grid, r, c, color, visited, component):
    """DFS to find connected same-color blocks"""

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

# ==========================================================
# CONNECTED COMPONENT
# ==========================================================
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
# GREEDY CPU MOVE
# ==========================================================
def cpu_best_move(grid):
    best_component = []
    best_score = 0

    for r in range(ROWS):
        for c in range(COLS):
            if grid.board[r][c]:
                comp = get_component(grid, r, c)
                score = len(comp) ** 2
                if score > best_score:
                    best_score = score
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
    print("5. CPU uses Greedy Algorithm")
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
        print("Invalid choice! Defaulting to 5x5")
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
