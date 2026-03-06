# ==========================================================
# SAME GAME - ADT & DSA IMPLEMENTATION
# Professional GUI with Live Algorithm Visualization
# ==========================================================
# ADTs USED:
# 1. Grid ADT        -> 2D List (Board)
# 2. Graph ADT       -> Implicit Grid Graph
# 3. Stack ADT       -> Iterative DFS + Gravity
# 4. Set ADT         -> Visited Nodes
# 5. List ADT        -> Connected Components
# 6. Greedy Strategy -> Local heuristic optimization
# 7. Optimal Strategy -> Divide & Conquer + Dynamic Programming
# 8. Exhaustive Strategy -> Backtracking with/without Memoization
# ==========================================================

import tkinter as tk
from tkinter import messagebox, ttk
import random
import time
import threading

# -------------------------------
# GLOBAL GAME VARIABLES
# -------------------------------
COLORS = ['R', 'G', 'B', 'Y']
COLOR_MAP = {
    'R': '#ef4444',  # Red
    'G': '#22c55e',  # Green
    'B': '#3b82f6',  # Blue
    'Y': '#eab308',  # Yellow
    None: '#1e293b'  # Empty (dark)
}

# Theme colors
BG_COLOR = '#0f172a'
FG_COLOR = '#f8fafc'
ACCENT_COLOR = '#fbbf24'
PANEL_COLOR = '#1e293b'
BUTTON_COLOR = '#334155'
HIGHLIGHT_COLOR = '#fbbf24'

# Statistics for search tree pruning (advanced demo)
search_stats = {
    'nodes_visited': 0,
    'pruned_branches': 0,
    'max_depth': 0
}

def reset_search_stats():
    """Reset search tree statistics"""
    global search_stats
    search_stats = {
        'nodes_visited': 0,
        'pruned_branches': 0,
        'max_depth': 0
    }

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

    def copy(self):
        """Create a deep copy of the grid"""
        new_grid = GridADT.__new__(GridADT)
        new_grid.rows = self.rows
        new_grid.cols = self.cols
        new_grid.board = [row[:] for row in self.board]
        return new_grid

# ==========================================================
# GRAPH ADT
# ==========================================================
class GraphADT:
    @staticmethod
    def neighbors(r, c):
        return [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]

# ==========================================================
# ITERATIVE DFS (STACK-BASED)
# ==========================================================
def dfs(grid, r, c, color, visited, component):
    """Iterative DFS using stack ADT"""
    stack = [(r, c)]

    while stack:
        cr, cc = stack.pop()

        if cr < 0 or cr >= grid.rows or cc < 0 or cc >= grid.cols:
            continue

        if (cr, cc) in visited:
            continue

        if grid.board[cr][cc] != color:
            continue

        visited.add((cr, cc))
        component.append((cr, cc))

        for nr, nc in GraphADT.neighbors(cr, cc):
            if (nr, nc) not in visited:
                stack.append((nr, nc))

def get_component(grid, r, c):
    """Get connected component"""
    if r < 0 or r >= grid.rows or c < 0 or c >= grid.cols:
        return []

    if grid.board[r][c] is None:
        return []

    visited = set()
    component = []
    dfs(grid, r, c, grid.board[r][c], visited, component)
    return component

def get_all_components(grid):
    """Get all valid components (size > 1)"""
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
# GRAVITY (STACK-BASED)
# ==========================================================
def apply_gravity(grid):
    """Apply vertical and horizontal gravity"""
    # Vertical gravity (stack-based)
    for c in range(grid.cols):
        stack = []
        for r in range(grid.rows):
            if grid.board[r][c] is not None:
                stack.append(grid.board[r][c])

        for r in range(grid.rows - 1, -1, -1):
            grid.board[r][c] = stack.pop() if stack else None

    # Horizontal shift
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

def is_game_over(grid):
    """Check if any valid moves remain"""
    return len(get_all_components(grid)) == 0

def is_board_empty(grid):
    """Check if board is completely empty"""
    return all(cell is None for row in grid.board for cell in row)

# ==========================================================
# MERGE SORT FOR GREEDY STRATEGY
# ==========================================================
def merge_sort_components(components):
    """Sort components by score using merge sort"""
    if len(components) <= 1:
        return components

    mid = len(components) // 2
    left = merge_sort_components(components[:mid])
    right = merge_sort_components(components[mid:])

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
# GREEDY STRATEGY (Used for CPU opponent)
# ==========================================================
def greedy_strategy(grid):
    """
    Greedy Strategy: Always select the largest component
    Uses merge sort for academic demonstration
    """
    components = get_all_components(grid)

    if not components:
        return None

    # Score each component
    scored_components = [(len(comp) ** 2, comp) for comp in components]

    # Sort by score using merge sort (academic demonstration)
    sorted_components = merge_sort_components(scored_components)

    # Return the highest-scoring component
    return sorted_components[0][1]

# ==========================================================
# DIVIDE & CONQUER + DYNAMIC PROGRAMMING (DC + DP)
# ==========================================================

# ==========================================================
# DIVIDE BOARD INTO INDEPENDENT REGIONS (Divide Phase)
# ==========================================================
def divide_board_regions(grid):
    """
    Divide the board into independent regions based on empty columns.
    Each region is a contiguous set of columns that contain blocks.
    """
    regions = []
    current = []

    for c in range(grid.cols):
        column_has_block = any(
            grid.board[r][c] is not None
            for r in range(grid.rows)
        )

        if column_has_block:
            current.append(c)
        else:
            if current:
                regions.append(current)
                current = []

    if current:
        regions.append(current)

    return regions

# ==========================================================
# DP SOLVER FOR OPTIMAL SCORE (Memoized)
# ==========================================================
dp_memo = {}

def dp_max_score(grid, depth=0):
    """
    Dynamic Programming solver for Same Game (single player)
    Returns maximum possible total score from current board state
    Includes search statistics for advanced demo
    """
    global search_stats
    search_stats['nodes_visited'] += 1
    search_stats['max_depth'] = max(search_stats['max_depth'], depth)
    
    # Create hashable board representation
    board_tuple = tuple(tuple(row) for row in grid.board)

    # Check memoization cache
    if board_tuple in dp_memo:
        search_stats['pruned_branches'] += 1
        return dp_memo[board_tuple]

    # Get all possible moves
    components = get_all_components(grid)
    
    # Sort by size for better pruning (optional but helpful)
    components.sort(key=len, reverse=True)

    # Base case: no moves left
    if not components:
        return 0

    best = 0

    # Try each possible move
    for comp in components:
        # Create simulation grid
        sim = grid.copy()

        # Remove the component
        for r, c in comp:
            sim.board[r][c] = None

        # Apply gravity
        apply_gravity(sim)

        # Calculate score: immediate gain + future optimal score
        gain = len(comp) ** 2
        future = dp_max_score(sim, depth + 1)
        total = gain + future

        # Update best score
        if total > best:
            best = total

    # Cache and return result
    dp_memo[board_tuple] = best
    return best

# ==========================================================
# CONQUER REGION USING DP
# ==========================================================
def conquer_region(grid, region_cols):
    """
    Solve a specific region using DP.
    Only considers components that are fully inside the region.
    """
    components = get_all_components(grid)

    best_move = None
    best_value = -1

    for comp in components:
        # Only consider components fully inside region
        if not all(c in region_cols for r, c in comp):
            continue

        sim = grid.copy()

        for r, c in comp:
            sim.board[r][c] = None

        apply_gravity(sim)

        gain = len(comp) ** 2
        future = dp_max_score(sim)
        total = gain + future

        if total > best_value:
            best_value = total
            best_move = comp

    return best_move, best_value

# ==========================================================
# DC + DP OPTIMAL STRATEGY
# ==========================================================
def optimal_strategy(grid):
    """
    Optimal Strategy using Divide & Conquer + Dynamic Programming
    Returns the best move for the current player
    """
    global dp_memo
    # Note: dp_memo is NOT cleared here to maintain memoization across moves
    # It's cleared once at the start of analysis in the comparison function

    # -------- DIVIDE --------
    regions = divide_board_regions(grid)

    if not regions:
        return None

    results = []

    # -------- CONQUER --------
    for region in regions:
        move, value = conquer_region(grid, region)

        if move:
            results.append((move, value))

    # -------- COMBINE --------
    best_move = None
    best_value = -1

    for move, value in results:
        if value > best_value:
            best_value = value
            best_move = move

    return best_move

# ==========================================================
# EXHAUSTIVE STRATEGY (BACKTRACKING WITH MEMOIZATION)
# ==========================================================
backtrack_memo_cache = {}

def backtrack_memo(grid, depth=0):
    """
    Backtracking with memoization for optimal score
    Returns the maximum possible total score from this state
    Includes search statistics for advanced demo
    """
    global search_stats
    search_stats['nodes_visited'] += 1
    search_stats['max_depth'] = max(search_stats['max_depth'], depth)
    
    board_tuple = tuple(tuple(row) for row in grid.board)

    if board_tuple in backtrack_memo_cache:
        search_stats['pruned_branches'] += 1
        return backtrack_memo_cache[board_tuple]

    components = get_all_components(grid)

    if not components:
        return 0

    # Sort components by size for better performance
    components.sort(key=len, reverse=True)

    best = 0
    for comp in components:
        sim = grid.copy()
        for r, c in comp:
            sim.board[r][c] = None
        apply_gravity(sim)

        gain = len(comp) ** 2
        future = backtrack_memo(sim, depth + 1)
        total = gain + future

        if total > best:
            best = total

    backtrack_memo_cache[board_tuple] = best
    return best

def exhaustive_strategy(grid):
    """
    Exhaustive Strategy: Backtracking with memoization
    Returns the best move (component) for the current player
    """
    global backtrack_memo_cache
    backtrack_memo_cache.clear()

    components = get_all_components(grid)

    if not components:
        return None

    # Sort components by size for better exploration order
    components.sort(key=len, reverse=True)

    best_score = -1
    best_move = None

    for comp in components:
        sim = grid.copy()
        for r, c in comp:
            sim.board[r][c] = None
        apply_gravity(sim)

        gain = len(comp) ** 2
        future = backtrack_memo(sim)
        total = gain + future

        if total > best_score:
            best_score = total
            best_move = comp

    return best_move

# ==========================================================
# PURE BACKTRACKING (NO MEMOIZATION)
# ==========================================================

def backtrack_pure(grid, depth=0):
    """
    Pure Backtracking (NO memoization)
    Returns the maximum possible total score from this state
    Includes search statistics for advanced demo
    """
    global search_stats
    search_stats['nodes_visited'] += 1
    search_stats['max_depth'] = max(search_stats['max_depth'], depth)
    
    components = get_all_components(grid)

    if not components:
        return 0

    # Sort components by size for better performance
    components.sort(key=len, reverse=True)

    best = 0
    for comp in components:
        sim = grid.copy()
        for r, c in comp:
            sim.board[r][c] = None
        apply_gravity(sim)

        gain = len(comp) ** 2
        future = backtrack_pure(sim, depth + 1)
        total = gain + future

        if total > best:
            best = total

    return best

def exhaustive_strategy_pure(grid):
    """
    Pure Exhaustive Strategy: Backtracking WITHOUT memoization
    Returns the best move (component) for the current player
    """
    components = get_all_components(grid)

    if not components:
        return None

    # Sort components by size for better exploration order
    components.sort(key=len, reverse=True)

    best_score = -1
    best_move = None

    for comp in components:
        sim = grid.copy()
        for r, c in comp:
            sim.board[r][c] = None
        apply_gravity(sim)

        gain = len(comp) ** 2
        future = backtrack_pure(sim)
        total = gain + future

        if total > best_score:
            best_score = total
            best_move = comp

    return best_move

# ==========================================================
# SAME GAME GUI
# ==========================================================
class SameGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Same Game - ADT & DSA Edition")
        self.root.geometry("1300x800")
        self.root.configure(bg=BG_COLOR)

        # Game state
        self.rows = 6
        self.cols = 6
        self.grid = None
        self.original_grid = None
        self.score = 0
        self.cpu_score = 0
        self.game_mode = None
        self.selected_component = []
        self.is_animating = False
        self.game_over = False
        self.algorithm_running = False
        self.visualization_speed = 0.5

        # Cell size
        self.cell_size = 60

        # Create UI
        self.setup_ui()

        # Show main menu
        self.show_menu()

    def setup_ui(self):
        """Setup the main UI structure"""
        self.main_container = tk.Frame(self.root, bg=BG_COLOR)
        self.main_container.pack(fill='both', expand=True)

    def clear_screen(self):
        """Clear all widgets from main container"""
        for widget in self.main_container.winfo_children():
            widget.destroy()

    # ================= MENU =================
    def show_menu(self):
        self.clear_screen()

        center_frame = tk.Frame(self.main_container, bg=BG_COLOR)
        center_frame.place(relx=0.5, rely=0.5, anchor='center')

        title_frame = tk.Frame(center_frame, bg=BG_COLOR)
        title_frame.pack(pady=20)

        for symbol in ["⚡", "🎮", "⚡"]:
            tk.Label(title_frame, text=symbol, 
                    font=('Arial', 48), 
                    fg=ACCENT_COLOR, bg=BG_COLOR).pack(side='left', padx=5)

        tk.Label(center_frame, text="SAME GAME", 
                font=('Arial', 48, 'bold'), 
                fg=ACCENT_COLOR, bg=BG_COLOR).pack()

        tk.Label(center_frame, text="Data Structures & Algorithms Edition", 
                font=('Arial', 14), 
                fg='#94a3b8', bg=BG_COLOR).pack(pady=10)

        btn_frame = tk.Frame(center_frame, bg=BG_COLOR)
        btn_frame.pack(pady=30)

        buttons = [
            ("👤 Single Player", '#22c55e', lambda: self.start_game('single')),
            ("🤖 vs CPU", '#3b82f6', lambda: self.start_game('multiplayer')),
            ("🧠 Algorithm Analysis", '#a855f7', self.show_algorithm_menu),
            ("⚙️ Settings", '#64748b', self.show_settings),
            ("📖 Instructions", '#64748b', self.show_instructions)
        ]

        for text, color, command in buttons:
            btn = tk.Button(btn_frame, text=text,
                          font=('Arial', 14, 'bold'),
                          bg=color, fg='white',
                          width=25, height=2,
                          bd=0, cursor='hand2',
                          command=command)
            btn.pack(pady=5)

            btn.bind('<Enter>', lambda e, b=btn, c=color: b.config(bg=self.lighten_color(c)))
            btn.bind('<Leave>', lambda e, b=btn, c=color: b.config(bg=c))

        tk.Label(center_frame, text=f"Current Board: {self.rows} × {self.cols}", 
                font=('Arial', 11), 
                fg='#94a3b8', bg=BG_COLOR).pack(pady=20)

    def lighten_color(self, color):
        if color.startswith('#'):
            r = min(255, int(color[1:3], 16) + 30)
            g = min(255, int(color[3:5], 16) + 30)
            b = min(255, int(color[5:7], 16) + 30)
            return f'#{r:02x}{g:02x}{b:02x}'
        return color

    # ================= ALGORITHM ANALYSIS MENU =================
    def show_algorithm_menu(self):
        if not self.original_grid and self.grid:
            self.original_grid = self.grid.copy()

        if not self.original_grid:
            messagebox.showinfo("No Game", "Please start a game first!")
            self.show_menu()
            return

        self.clear_screen()

        center_frame = tk.Frame(self.main_container, bg=BG_COLOR)
        center_frame.place(relx=0.5, rely=0.5, anchor='center')

        tk.Label(center_frame, text="🧠 ALGORITHM ANALYSIS", 
                font=('Arial', 36, 'bold'), 
                fg='#a855f7', bg=BG_COLOR).pack(pady=20)

        tk.Label(center_frame, text=f"Analyzing {self.rows}×{self.cols} Board", 
                font=('Arial', 14), 
                fg='#94a3b8', bg=BG_COLOR).pack(pady=10)

        speed_frame = tk.Frame(center_frame, bg=BG_COLOR)
        speed_frame.pack(pady=10)

        tk.Label(speed_frame, text="Visualization Speed:", 
                font=('Arial', 11), 
                fg='white', bg=BG_COLOR).pack(side='left', padx=5)

        self.speed_var = tk.DoubleVar(value=0.5)
        speed_scale = tk.Scale(speed_frame, from_=0.1, to=1.0, resolution=0.1,
                              orient='horizontal', length=200,
                              variable=self.speed_var,
                              bg=BG_COLOR, fg='white',
                              highlightbackground=BG_COLOR)
        speed_scale.pack(side='left', padx=5)

        tk.Label(speed_frame, text="(Faster ← → Slower)", 
                font=('Arial', 9), 
                fg='#94a3b8', bg=BG_COLOR).pack(side='left', padx=5)

        btn_frame = tk.Frame(center_frame, bg=BG_COLOR)
        btn_frame.pack(pady=20)

        algorithm_buttons = [
            ("🟢 Greedy Strategy", '#22c55e', 1),
            ("🟡 DC + DP Optimal Strategy", '#eab308', 2),
            ("🔴 Exhaustive (Backtracking + Memo)", '#ef4444', 3),
            ("🟠 Exhaustive (Pure Backtracking)", '#f97316', 4),
        ]

        for text, color, difficulty in algorithm_buttons:
            btn = tk.Button(btn_frame, text=text,
                          font=('Arial', 12, 'bold'),
                          bg=color, fg='white' if difficulty != 2 else 'black',
                          width=45, height=2,
                          bd=0, cursor='hand2',
                          command=lambda d=difficulty: self.run_live_algorithm_analysis(d))
            btn.pack(pady=3)

        tk.Button(btn_frame, text="📊 Compare All Algorithms", 
                 font=('Arial', 12, 'bold'),
                 bg='#a855f7', fg='white',
                 width=45, height=2,
                 bd=0, cursor='hand2',
                 command=self.compare_algorithms).pack(pady=10)

        tk.Button(center_frame, text="← Back to Menu",
                 font=('Arial', 12),
                 bg='#64748b', fg='white',
                 width=20, height=2,
                 bd=0, cursor='hand2',
                 command=self.show_menu).pack(pady=20)

    # ================= LIVE ALGORITHM ANALYSIS =================
    def run_live_algorithm_analysis(self, difficulty):
        if self.algorithm_running:
            messagebox.showwarning("Algorithm Busy", "Algorithm analysis is already running!")
            return

        # Show warning for pure backtracking on large boards
        if difficulty == 4 and self.rows > 6:
            if not messagebox.askyesno("Warning", 
                "Pure backtracking on large boards may be very slow.\n\n"
                f"Board size: {self.rows}×{self.cols}\n"
                "This could take several minutes.\n\n"
                "Do you want to continue?"):
                return

        self.algorithm_running = True

        analysis_window = tk.Toplevel(self.root)
        analysis_window.title("Live Algorithm Analysis")
        analysis_window.geometry("1000x700")
        analysis_window.configure(bg=BG_COLOR)
        analysis_window.transient(self.root)

        difficulties = {
            1: "GREEDY STRATEGY - Local Heuristic", 
            2: "DC + DP OPTIMAL STRATEGY - Divide & Conquer + Dynamic Programming", 
            3: "EXHAUSTIVE STRATEGY - Backtracking + Memoization",
            4: "EXHAUSTIVE STRATEGY - Pure Backtracking (No Memo)"
        }
        colors = {1: '#22c55e', 2: '#eab308', 3: '#ef4444', 4: '#f97316'}

        title_frame = tk.Frame(analysis_window, bg=BG_COLOR)
        title_frame.pack(pady=10)

        tk.Label(title_frame, text="🧠", font=('Arial', 24), 
                fg=colors[difficulty], bg=BG_COLOR).pack(side='left', padx=5)
        tk.Label(title_frame, text=difficulties[difficulty], 
                font=('Arial', 18, 'bold'), 
                fg=colors[difficulty], bg=BG_COLOR).pack(side='left')

        control_frame = tk.Frame(analysis_window, bg=BG_COLOR)
        control_frame.pack(pady=5)

        self.analysis_paused = False

        tk.Button(control_frame, text="⏸️ Pause", 
                 font=('Arial', 10),
                 bg='#64748b', fg='white',
                 bd=0, cursor='hand2',
                 command=self.toggle_pause).pack(side='left', padx=5)

        tk.Button(control_frame, text="⏹️ Stop", 
                 font=('Arial', 10),
                 bg='#ef4444', fg='white',
                 bd=0, cursor='hand2',
                 command=lambda: self.stop_analysis(analysis_window)).pack(side='left', padx=5)

        board_frame = tk.Frame(analysis_window, bg=PANEL_COLOR, padx=20, pady=20)
        board_frame.pack(pady=10)

        canvas_width = self.cols * self.cell_size
        canvas_height = self.rows * self.cell_size

        self.analysis_canvas = tk.Canvas(board_frame,
                                        width=canvas_width,
                                        height=canvas_height,
                                        bg=BG_COLOR,
                                        highlightthickness=2,
                                        highlightbackground=colors[difficulty])
        self.analysis_canvas.pack()
        
        # Draw initial board immediately
        self.draw_analysis_board(self.original_grid)

        info_frame = tk.Frame(analysis_window, bg=PANEL_COLOR, padx=20, pady=10)
        info_frame.pack(fill='x', padx=20, pady=5)

        self.move_label = tk.Label(info_frame, text="Move: 0", 
                                  font=('Arial', 12, 'bold'),
                                  fg='white', bg=PANEL_COLOR)
        self.move_label.pack(side='left', padx=10)

        self.score_label = tk.Label(info_frame, text="Score: 0", 
                                   font=('Arial', 12, 'bold'),
                                   fg=ACCENT_COLOR, bg=PANEL_COLOR)
        self.score_label.pack(side='left', padx=10)

        self.status_label = tk.Label(info_frame, text="Status: Algorithm evaluating...", 
                                     font=('Arial', 12),
                                     fg='#94a3b8', bg=PANEL_COLOR)
        self.status_label.pack(side='right', padx=10)

        log_frame = tk.Frame(analysis_window, bg=PANEL_COLOR, padx=20, pady=10)
        log_frame.pack(fill='both', expand=True, padx=20, pady=10)

        tk.Label(log_frame, text="Analysis Log:", 
                font=('Arial', 11, 'bold'),
                fg='white', bg=PANEL_COLOR).pack(anchor='w')

        self.log_text = tk.Text(log_frame, 
                                font=('Consolas', 10),
                                bg=BG_COLOR, fg='#e2e8f0',
                                height=8,
                                wrap='word')
        self.log_text.pack(fill='both', expand=True, pady=5)

        scrollbar = tk.Scrollbar(self.log_text)
        scrollbar.pack(side='right', fill='y')
        self.log_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.log_text.yview)

        thread = threading.Thread(
            target=self._live_analysis_thread,
            args=(difficulty, analysis_window)
        )
        thread.daemon = True
        thread.start()

    def toggle_pause(self):
        self.analysis_paused = not self.analysis_paused

    def stop_analysis(self, window):
        self.algorithm_running = False
        window.destroy()

    def _live_analysis_thread(self, difficulty, window):
        try:
            grid_to_analyze = self.original_grid.copy()
            score = 0
            move_count = 0

            algo_names = {
                1: "GREEDY",
                2: "DC + DP OPTIMAL", 
                3: "EXHAUSTIVE (Memo)",
                4: "EXHAUSTIVE (Pure)"
            }
            
            self.log_message(f"Starting {algo_names[difficulty]} Strategy Analysis...")
            self.log_message("="*50)

            start_time = time.time()

            while not is_game_over(grid_to_analyze) and self.algorithm_running:
                while self.analysis_paused and self.algorithm_running:
                    time.sleep(0.1)

                if not self.algorithm_running:
                    break

                move_count += 1

                # Fix lambda closure for move counter
                self.root.after(0, lambda m=move_count: self.move_label.config(text=f"Move: {m}"))

                if difficulty == 1:
                    move = greedy_strategy(grid_to_analyze)
                elif difficulty == 2:
                    move = optimal_strategy(grid_to_analyze)
                elif difficulty == 3:
                    move = exhaustive_strategy(grid_to_analyze)
                else:
                    move = exhaustive_strategy_pure(grid_to_analyze)

                move = list(move) if move else None

                if move is None:
                    self.log_message("No valid moves available!")
                    break

                self.root.after(0, lambda m=move: self.highlight_move(m))
                time.sleep(self.speed_var.get() / 2)

                for r, c in move:
                    grid_to_analyze.board[r][c] = None

                gain = len(move) ** 2
                score += gain

                # Fix lambda closure for score
                self.root.after(0, lambda s=score: self.score_label.config(text=f"Score: {s}"))

                self.log_message(f"Move {move_count}: Removed {len(move)} blocks at {move[0]} → +{gain} points")

                apply_gravity(grid_to_analyze)

                self.root.after(0, lambda g=grid_to_analyze: self.draw_analysis_board(g))

                time.sleep(self.speed_var.get())

            elapsed = time.time() - start_time

            self.log_message("="*50)
            self.log_message(f"Analysis Complete!")
            self.log_message(f"Final Score: {score}")
            self.log_message(f"Total Moves: {move_count}")
            self.log_message(f"Execution Time: {elapsed:.2f} seconds")
            
            # Algorithm-specific statistics
            if difficulty == 2:  # DC + DP Strategy
                regions = divide_board_regions(grid_to_analyze)
                self.log_message(f"Regions Analyzed: {len(regions)}")
                self.log_message(f"DP States Stored: {len(dp_memo)}")
            elif difficulty == 3:  # Exhaustive with Memo
                self.log_message(f"Backtracking Cache Size: {len(backtrack_memo_cache)}")
            elif difficulty == 4:  # Pure Backtracking
                self.log_message(f"Note: Pure backtracking uses no cache")
                self.log_message(f"Performance may be significantly slower on larger boards")

            self.root.after(0, lambda: self.status_label.config(text="Status: Complete"))

        except Exception as e:
            self.log_message(f"Error: {str(e)}")
        finally:
            self.algorithm_running = False

    def highlight_move(self, component):
        if hasattr(self, 'analysis_canvas'):
            self.analysis_canvas.delete('highlight')

            for r, c in component:
                x1 = c * self.cell_size
                y1 = r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                self.analysis_canvas.create_rectangle(
                    x1 + 2, y1 + 2, x2 - 2, y2 - 2,
                    outline=HIGHLIGHT_COLOR,
                    width=4,
                    tags='highlight'
                )

    def draw_analysis_board(self, grid):
        if not hasattr(self, 'analysis_canvas'):
            return

        self.analysis_canvas.delete('all')

        for r in range(grid.rows):
            for c in range(grid.cols):
                x1 = c * self.cell_size
                y1 = r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                cell = grid.board[r][c]

                if cell:
                    color = COLOR_MAP[cell]

                    self.analysis_canvas.create_rectangle(
                        x1 + 2, y1 + 2, x2 - 2, y2 - 2,
                        fill=color,
                        outline=color,
                        width=1
                    )

                    self.analysis_canvas.create_text(
                        x1 + self.cell_size//2,
                        y1 + self.cell_size//2,
                        text=cell,
                        fill='white',
                        font=('Arial', self.cell_size//3, 'bold')
                    )
                else:
                    self.analysis_canvas.create_rectangle(
                        x1 + 2, y1 + 2, x2 - 2, y2 - 2,
                        fill=BG_COLOR,
                        outline=PANEL_COLOR,
                        width=1
                    )

    def log_message(self, message):
        if hasattr(self, 'log_text'):
            self.root.after(0, lambda: self.log_text.insert(tk.END, message + "\n"))
            self.root.after(0, lambda: self.log_text.see(tk.END))

    # ================= COMPARE ALGORITHMS =================
    def compare_algorithms(self):
        if self.algorithm_running:
            messagebox.showwarning("Analysis Busy", "Algorithm analysis is already running!")
            return

        self.algorithm_running = True

        comp_window = tk.Toplevel(self.root)
        comp_window.title("Algorithm Comparison")
        comp_window.geometry("1000x750")
        comp_window.configure(bg=BG_COLOR)
        comp_window.transient(self.root)

        tk.Label(comp_window, text="📊 ALGORITHM COMPARISON", 
                font=('Arial', 20, 'bold'), 
                fg=ACCENT_COLOR, bg=BG_COLOR).pack(pady=10)

        output_frame = tk.Frame(comp_window, bg=PANEL_COLOR, padx=20, pady=20)
        output_frame.pack(fill='both', expand=True, padx=20, pady=10)

        output_text = tk.Text(output_frame, 
                              font=('Consolas', 10),
                              bg=BG_COLOR, fg='#e2e8f0',
                              wrap='word',
                              height=25)
        output_text.pack(side='left', fill='both', expand=True)

        scrollbar = tk.Scrollbar(output_frame, command=output_text.yview)
        scrollbar.pack(side='right', fill='y')
        output_text.config(yscrollcommand=scrollbar.set)

        progress_label = tk.Label(comp_window, text="Running all algorithms...", 
                                  font=('Arial', 10), 
                                  fg='#94a3b8', bg=BG_COLOR)
        progress_label.pack(pady=5)

        tk.Button(comp_window, text="Close",
                 font=('Arial', 12),
                 bg='#64748b', fg='white',
                 width=15, height=1,
                 bd=0, cursor='hand2',
                 command=lambda: [comp_window.destroy(), setattr(self, 'algorithm_running', False)]).pack(pady=10)

        thread = threading.Thread(
            target=self._compare_algorithms_thread,
            args=(output_text, progress_label)
        )
        thread.daemon = True
        thread.start()

    def _compare_algorithms_thread(self, output_text, progress_label):
        try:
            grid_to_analyze = self.original_grid.copy()

            self.root.after(0, lambda: output_text.insert(tk.END, "="*90 + "\n"))
            self.root.after(0, lambda: output_text.insert(tk.END, "ALGORITHM COMPARISON BENCHMARK\n"))
            self.root.after(0, lambda: output_text.insert(tk.END, f"Board: {self.rows}×{self.cols}\n"))
            self.root.after(0, lambda: output_text.insert(tk.END, "="*90 + "\n\n"))
            self.root.after(0, lambda: output_text.see(tk.END))

            results = []
            algorithms = [
                (1, "GREEDY STRATEGY", greedy_strategy),
                (2, "DC + DP OPTIMAL STRATEGY", optimal_strategy),
                (3, "EXHAUSTIVE (Backtracking + Memo)", exhaustive_strategy),
                (4, "EXHAUSTIVE (Pure Backtracking)", exhaustive_strategy_pure)
            ]

            for diff, name, algo_func in algorithms:
                self.root.after(0, lambda n=name: output_text.insert(tk.END, f"\n▶ Testing {n}...\n"))
                self.root.after(0, lambda: output_text.see(tk.END))

                # Clear caches and reset statistics before each algorithm
                global dp_memo, backtrack_memo_cache, search_stats
                dp_memo.clear()
                backtrack_memo_cache.clear()
                reset_search_stats()
                
                # Safer copy for comparison mode
                sim = GridADT.__new__(GridADT)
                sim.rows = grid_to_analyze.rows
                sim.cols = grid_to_analyze.cols
                sim.board = [row[:] for row in grid_to_analyze.board]
                
                score = 0
                move_count = 0

                start = time.time()

                while not is_game_over(sim):
                    move_count += 1
                    move = algo_func(sim)

                    if move is None:
                        break

                    score += len(move) ** 2

                    for r, c in move:
                        sim.board[r][c] = None
                    apply_gravity(sim)

                elapsed = time.time() - start
                
                # Add cache/region statistics
                if diff == 2:
                    cache_size = len(dp_memo)
                    regions = divide_board_regions(grid_to_analyze)
                    region_info = f", Regions: {len(regions)}"
                    search_info = f", Nodes: {search_stats['nodes_visited']}, Pruned: {search_stats['pruned_branches']}"
                elif diff == 3:
                    cache_size = len(backtrack_memo_cache)
                    region_info = ""
                    search_info = f", Nodes: {search_stats['nodes_visited']}, Pruned: {search_stats['pruned_branches']}"
                elif diff == 4:
                    cache_size = 0
                    region_info = " (No cache)"
                    search_info = f", Nodes: {search_stats['nodes_visited']}, Pruned: 0"
                else:
                    cache_size = 0
                    region_info = ""
                    search_info = ""
                    
                results.append((name, score, move_count, elapsed, cache_size, region_info, search_info))

                self.root.after(0, lambda s=score: output_text.insert(tk.END, f"  ✓ Score: {s}\n"))
                self.root.after(0, lambda m=move_count: output_text.insert(tk.END, f"  ✓ Moves: {m}\n"))
                self.root.after(0, lambda e=elapsed: output_text.insert(tk.END, f"  ✓ Time: {e:.2f}s\n"))
                if diff in [2, 3, 4]:
                    self.root.after(0, lambda c=cache_size, r=region_info, s=search_info: 
                                   output_text.insert(tk.END, f"  ✓ Cache Size: {c}{r}{s}\n"))
                if diff in [2, 3]:
                    self.root.after(0, lambda: output_text.insert(tk.END, f"  ✓ Max Depth: {search_stats['max_depth']}\n"))
                self.root.after(0, lambda: output_text.see(tk.END))

            self.root.after(0, lambda: output_text.insert(tk.END, "\n" + "="*90 + "\n"))
            self.root.after(0, lambda: output_text.insert(tk.END, "📊 COMPARISON RESULTS\n"))
            self.root.after(0, lambda: output_text.insert(tk.END, "="*90 + "\n"))
            self.root.after(0, lambda: output_text.insert(tk.END, f"{'Algorithm':<50} {'Score':>10} {'Moves':>8} {'Time (s)':>10}\n"))
            self.root.after(0, lambda: output_text.insert(tk.END, "-"*90 + "\n"))

            for name, score, moves, elapsed, cache, region_info, search_info in results:
                self.root.after(0, lambda n=name, s=score, m=moves, e=elapsed: 
                               output_text.insert(tk.END, f"{n:<50} {s:>10} {m:>8} {e:>10.2f}\n"))

            best_score = max(results, key=lambda x: x[1])
            fastest = min(results, key=lambda x: x[3])

            self.root.after(0, lambda: output_text.insert(tk.END, "\n" + "="*90 + "\n"))
            self.root.after(0, lambda: output_text.insert(tk.END, f"🏆 Best Score: {best_score[0]} with {best_score[1]} points\n"))
            self.root.after(0, lambda: output_text.insert(tk.END, f"⚡ Fastest: {fastest[0]} in {fastest[3]:.2f} seconds\n"))
            
            # Add performance comparison note for backtracking versions
            if len(results) >= 4:
                memo_time = results[2][3]  # Backtracking + Memo time
                pure_time = results[3][3]   # Pure Backtracking time
                if pure_time > 0 and memo_time > 0:
                    speedup = pure_time / memo_time
                    self.root.after(0, lambda: output_text.insert(tk.END, f"\n📈 Memoization Speedup: {speedup:.1f}x faster\n"))
                    self.root.after(0, lambda: output_text.insert(tk.END, f"   (Pure backtracking takes {pure_time:.2f}s vs {memo_time:.2f}s with memoization)\n"))
            
            # Add search tree statistics summary
            self.root.after(0, lambda: output_text.insert(tk.END, "\n" + "="*90 + "\n"))
            self.root.after(0, lambda: output_text.insert(tk.END, "🔍 SEARCH TREE STATISTICS\n"))
            self.root.after(0, lambda: output_text.insert(tk.END, "="*90 + "\n"))
            self.root.after(0, lambda: output_text.insert(tk.END, "• DP + Memoization: Significant pruning through caching\n"))
            self.root.after(0, lambda: output_text.insert(tk.END, "• Backtracking + Memo: Reuses computed results\n"))
            self.root.after(0, lambda: output_text.insert(tk.END, "• Pure Backtracking: Explores entire search space\n"))
            self.root.after(0, lambda: output_text.insert(tk.END, "="*90 + "\n"))

            self.root.after(0, lambda: progress_label.config(text="Comparison complete!"))

        except Exception as e:
            self.root.after(0, lambda: output_text.insert(tk.END, f"\n❌ Error: {str(e)}\n"))
        finally:
            self.algorithm_running = False

    # ================= SETTINGS =================
    def show_settings(self):
        self.clear_screen()

        center_frame = tk.Frame(self.main_container, bg=BG_COLOR)
        center_frame.place(relx=0.5, rely=0.5, anchor='center')

        tk.Label(center_frame, text="⚙️ SETTINGS", 
                font=('Arial', 36, 'bold'), 
                fg=ACCENT_COLOR, bg=BG_COLOR).pack(pady=20)

        sizes = [
            (6, 6, "Small (6×6) - Fast"),
            (8, 8, "Medium (8×8) - Balanced"),
            (10, 10, "Large (10×10) - Challenging")
        ]

        for r, c, label in sizes:
            is_current = (self.rows == r and self.cols == c)
            btn_color = ACCENT_COLOR if is_current else BUTTON_COLOR

            btn = tk.Button(center_frame, text=label,
                          font=('Arial', 14, 'bold'),
                          bg=btn_color, fg='black' if is_current else 'white',
                          width=25, height=2,
                          bd=0, cursor='hand2',
                          command=lambda r=r, c=c: self.set_board_size(r, c))
            btn.pack(pady=5)

        tk.Button(center_frame, text="← Back to Menu",
                 font=('Arial', 14),
                 bg='#64748b', fg='white',
                 width=25, height=2,
                 bd=0, cursor='hand2',
                 command=self.show_menu).pack(pady=30)

    def set_board_size(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.cell_size = min(60, 500 // max(rows, cols))
        self.show_menu()

    # ================= INSTRUCTIONS =================
    def show_instructions(self):
        self.clear_screen()

        center_frame = tk.Frame(self.main_container, bg=BG_COLOR)
        center_frame.place(relx=0.5, rely=0.5, anchor='center')

        tk.Label(center_frame, text="📖 HOW TO PLAY", 
                font=('Arial', 36, 'bold'), 
                fg=ACCENT_COLOR, bg=BG_COLOR).pack(pady=20)

        instructions = [
            "🎯 Click on connected blocks of the same color",
            "📦 Minimum 2 blocks required to remove them",
            "🏆 Score = (Number of Blocks Removed)²",
            "",
            "⬇️ GRAVITY MECHANICS:",
            "   • Blocks fall down to fill empty spaces",
            "   • Columns shift left when completely empty",
            "",
            "🤖 CPU OPPONENT:",
            "   • Uses Greedy Strategy (always picks largest component)",
            "   • Fast but not optimal - good for practice",
            "",
            "🧠 ALGORITHM ANALYSIS:",
            "   • Greedy Strategy: Local heuristic optimization (fast)",
            "   • DC + DP Optimal Strategy: Divide board → Solve regions → Combine (optimal, fast)",
            "   • Exhaustive (Memo): Backtracking with memoization (optimal, fast)",
            "   • Exhaustive (Pure): Backtracking without memoization (optimal, slow)",
            "   • Watch algorithms solve the board in real-time!",
            "   • Compare search tree statistics to see pruning benefits",
            "",
            "🎮 GAME MODES:",
            "   • Single Player: Play at your own pace",
            "   • vs CPU: Challenge the greedy CPU opponent",
            "   • Algorithm Analysis: Watch strategies in action",
            "",
            "🏁 Game ends when no more moves are possible"
        ]

        for inst in instructions:
            if inst == "":
                tk.Label(center_frame, text="", bg=BG_COLOR).pack()
            elif inst.startswith("   "):
                tk.Label(center_frame, text=inst,
                        font=('Arial', 11),
                        fg='#94a3b8', bg=BG_COLOR,
                        justify='left').pack(anchor='w')
            else:
                tk.Label(center_frame, text=inst,
                        font=('Arial', 12, 'bold'),
                        fg='#e2e8f0', bg=BG_COLOR,
                        justify='left').pack(anchor='w', pady=2)

        tk.Button(center_frame, text="← Back to Menu",
                 font=('Arial', 14, 'bold'),
                 bg='#3b82f6', fg='white',
                 width=20, height=2,
                 bd=0, cursor='hand2',
                 command=self.show_menu).pack(pady=30)

    # ================= START GAME =================
    def start_game(self, mode):
        self.game_mode = mode
        self.grid = GridADT(self.rows, self.cols)
        self.original_grid = self.grid.copy()
        self.score = 0
        self.cpu_score = 0
        self.game_over = False
        self.selected_component = []
        self.show_game()

    # ================= GAME SCREEN =================
    def show_game(self):
        self.clear_screen()

        main_frame = tk.Frame(self.main_container, bg=BG_COLOR)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        header = tk.Frame(main_frame, bg=PANEL_COLOR, height=80)
        header.pack(fill='x', pady=(0, 20))
        header.pack_propagate(False)

        tk.Button(header, text="🏠 MENU",
                 font=('Arial', 12, 'bold'),
                 bg=BUTTON_COLOR, fg='white',
                 bd=0, cursor='hand2',
                 command=self.confirm_exit).pack(side='left', padx=10, pady=20)

        tk.Label(header, text="SAME GAME",
                font=('Arial', 24, 'bold'),
                fg='white', bg=PANEL_COLOR).pack(side='left', padx=20)

        self.score_frame = tk.Frame(header, bg=PANEL_COLOR)
        self.score_frame.pack(side='right', padx=20)

        tk.Button(header, text="🧠 ALGORITHM ANALYSIS",
                 font=('Arial', 12, 'bold'),
                 bg='#a855f7', fg='white',
                 bd=0, cursor='hand2',
                 command=self.show_algorithm_menu).pack(side='right', padx=10)

        game_area = tk.Frame(main_frame, bg=BG_COLOR)
        game_area.pack(expand=True)

        board_frame = tk.Frame(game_area, bg=PANEL_COLOR, padx=20, pady=20)
        board_frame.pack()

        canvas_width = self.cols * self.cell_size
        canvas_height = self.rows * self.cell_size

        self.canvas = tk.Canvas(board_frame,
                               width=canvas_width,
                               height=canvas_height,
                               bg=BG_COLOR,
                               highlightthickness=2,
                               highlightbackground=BUTTON_COLOR)
        self.canvas.pack()

        self.info_label = tk.Label(game_area,
                                   text="Click on connected blocks to remove them",
                                   font=('Arial', 12),
                                   fg='#94a3b8', bg=BG_COLOR,
                                   height=2)
        self.info_label.pack(pady=10)

        self.draw_board()
        self.update_scores()

        self.canvas.bind('<Button-1>', self.handle_canvas_click)

    def draw_board(self):
        self.canvas.delete('all')

        for r in range(self.rows):
            for c in range(self.cols):
                x1 = c * self.cell_size
                y1 = r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                cell = self.grid.board[r][c]

                if cell:
                    color = COLOR_MAP[cell]
                    is_selected = (r, c) in self.selected_component

                    self.canvas.create_rectangle(
                        x1 + 2, y1 + 2, x2 - 2, y2 - 2,
                        fill=color,
                        outline=HIGHLIGHT_COLOR if is_selected else color,
                        width=3 if is_selected else 1,
                        tags=f'cell_{r}_{c}'
                    )

                    self.canvas.create_text(
                        x1 + self.cell_size//2,
                        y1 + self.cell_size//2,
                        text=cell,
                        fill='white',
                        font=('Arial', self.cell_size//3, 'bold')
                    )
                else:
                    self.canvas.create_rectangle(
                        x1 + 2, y1 + 2, x2 - 2, y2 - 2,
                        fill=BG_COLOR,
                        outline=PANEL_COLOR,
                        width=1
                    )

    def handle_canvas_click(self, event):
        if self.is_animating or self.game_over:
            return

        col = event.x // self.cell_size
        row = event.y // self.cell_size

        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.handle_click(row, col)

    def handle_click(self, r, c):
        if self.is_animating or self.game_over:
            return

        comp = get_component(self.grid, r, c)

        if len(comp) < 2:
            self.info_label.config(text="❌ Need at least 2 connected blocks!")
            return

        self.selected_component = comp
        points = len(comp) ** 2
        self.info_label.config(text=f"✨ {len(comp)} blocks = {points} points")
        self.draw_board()

        self.root.after(300, lambda: self.remove_component(comp))

    def remove_component(self, comp):
        self.is_animating = True

        for r, c in comp:
            self.grid.board[r][c] = None

        self.score += len(comp) ** 2
        self.selected_component = []
        self.draw_board()

        self.root.after(200, self.apply_gravity)

    def apply_gravity(self):
        apply_gravity(self.grid)
        self.draw_board()
        self.is_animating = False
        self.info_label.config(text="Click on connected blocks to remove them")
        self.update_scores()

        if is_game_over(self.grid):
            self.game_over = True
            self.show_game_over()
        elif self.game_mode == 'multiplayer':
            self.root.after(500, self.cpu_turn)

    def cpu_turn(self):
        if self.game_over:
            return

        self.is_animating = True
        self.info_label.config(text="🤖 CPU is thinking...")

        cpu_comp = greedy_strategy(self.grid)

        if cpu_comp:
            self.root.after(500, lambda: self.cpu_remove(cpu_comp))
        else:
            self.is_animating = False
            self.info_label.config(text="Click on connected blocks to remove them")
            self.check_game_over()

    def cpu_remove(self, comp):
        for r, c in comp:
            self.grid.board[r][c] = None

        self.cpu_score += len(comp) ** 2
        self.draw_board()

        self.root.after(200, self.cpu_gravity)

    def cpu_gravity(self):
        apply_gravity(self.grid)
        self.draw_board()
        self.is_animating = False
        self.info_label.config(text="Click on connected blocks to remove them")
        self.update_scores()
        self.check_game_over()

    def check_game_over(self):
        if is_game_over(self.grid):
            self.game_over = True
            self.show_game_over()

    def show_game_over(self):
        if self.game_mode == 'multiplayer':
            if self.score > self.cpu_score:
                winner = "🏆 HUMAN WINS!"
                winner_color = '#22c55e'
            elif self.cpu_score > self.score:
                winner = "🤖 CPU WINS!"
                winner_color = '#3b82f6'
            else:
                winner = "🤝 IT'S A TIE!"
                winner_color = '#94a3b8'

            msg = f"{winner}\n\nHuman: {self.score}\nCPU: {self.cpu_score}"
        else:
            if is_board_empty(self.grid):
                msg = f"🎉 PERFECT GAME!\n\nFinal Score: {self.score}"
            else:
                msg = f"🏆 Game Over!\n\nFinal Score: {self.score}"

        go_window = tk.Toplevel(self.root)
        go_window.title("Game Over")
        go_window.geometry("400x350")
        go_window.configure(bg=BG_COLOR)
        go_window.transient(self.root)
        go_window.grab_set()

        go_window.update_idletasks()
        x = (go_window.winfo_screenwidth() // 2) - (400 // 2)
        y = (go_window.winfo_screenheight() // 2) - (350 // 2)
        go_window.geometry(f'400x350+{x}+{y}')

        tk.Label(go_window, text="GAME OVER", 
                font=('Arial', 24, 'bold'), 
                fg=ACCENT_COLOR, bg=BG_COLOR).pack(pady=20)

        if self.game_mode == 'multiplayer':
            tk.Label(go_window, text=winner, 
                    font=('Arial', 18, 'bold'), 
                    fg=winner_color, bg=BG_COLOR).pack(pady=10)

        tk.Label(go_window, text=msg, 
                font=('Arial', 14), 
                fg='white', bg=BG_COLOR).pack(pady=20)

        btn_frame = tk.Frame(go_window, bg=BG_COLOR)
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Play Again",
                 font=('Arial', 12, 'bold'),
                 bg='#22c55e', fg='white',
                 width=12, height=1,
                 bd=0, cursor='hand2',
                 command=lambda: [go_window.destroy(), self.start_game(self.game_mode)]).pack(side='left', padx=5)

        tk.Button(btn_frame, text="Main Menu",
                 font=('Arial', 12, 'bold'),
                 bg='#64748b', fg='white',
                 width=12, height=1,
                 bd=0, cursor='hand2',
                 command=lambda: [go_window.destroy(), self.show_menu()]).pack(side='left', padx=5)

        tk.Button(btn_frame, text="Algorithm Analysis",
                 font=('Arial', 12, 'bold'),
                 bg='#a855f7', fg='white',
                 width=15, height=1,
                 bd=0, cursor='hand2',
                 command=lambda: [go_window.destroy(), self.show_algorithm_menu()]).pack(side='left', padx=5)

    def confirm_exit(self):
        if messagebox.askokcancel("Exit", "Return to main menu?"):
            self.show_menu()

    def update_scores(self):
        for widget in self.score_frame.winfo_children():
            widget.destroy()

        if self.game_mode == 'multiplayer':
            tk.Label(self.score_frame,
                    text=f"👤 {self.score}",
                    font=('Arial', 16, 'bold'),
                    fg='#22c55e', bg=PANEL_COLOR).pack(side='left', padx=10)

            tk.Label(self.score_frame,
                    text="vs",
                    font=('Arial', 14),
                    fg='#94a3b8', bg=PANEL_COLOR).pack(side='left', padx=5)

            tk.Label(self.score_frame,
                    text=f"🤖 {self.cpu_score}",
                    font=('Arial', 16, 'bold'),
                    fg='#3b82f6', bg=PANEL_COLOR).pack(side='left', padx=10)
        else:
            tk.Label(self.score_frame,
                    text=f"🏆 {self.score}",
                    font=('Arial', 18, 'bold'),
                    fg=ACCENT_COLOR, bg=PANEL_COLOR).pack(padx=10)

# ==========================================================
# MAIN
# ==========================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = SameGameGUI(root)
    root.mainloop()
