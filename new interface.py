import tkinter as tk
from tkinter import messagebox, ttk
import random
import time
from functools import lru_cache

# ==========================================================
# SAME GAME - GUI VERSION WITH ADT & DSA
# ==========================================================

COLORS = ['R', 'G', 'B', 'Y']
COLOR_MAP = {
    'R': '#ef4444',  # Red
    'G': '#22c55e',  # Green
    'B': '#3b82f6',  # Blue
    'Y': '#eab308',  # Yellow
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
    
    def display(self):
        """Console display for debugging"""
        print("\nBoard:")
        for r in range(self.rows):
            for c in range(self.cols):
                print(self.board[r][c] if self.board[r][c] else '.', end=' ')
            print()

# ==========================================================
# GRAPH ADT (IMPLICIT GRID GRAPH)
# ==========================================================
class GraphADT:
    @staticmethod
    def neighbors(r, c):
        return [(r+1, c), (r-1, c), (r, c+1), (r, c-1)]

# ==========================================================
# DFS (CONNECTED COMPONENT)
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

def get_component(grid, r, c):
    """Get connected component at position (r,c)"""
    if r < 0 or r >= grid.rows or c < 0 or c >= grid.cols:
        return []
    if grid.board[r][c] is None:
        return []
    
    visited = set()
    component = []
    dfs(grid, r, c, grid.board[r][c], visited, component)
    return component

def get_all_components(grid):
    """Returns list of all connected components (size > 1)"""
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
                components.append(comp)
    
    return components

# ==========================================================
# GRAVITY USING STACK ADT
# ==========================================================
def apply_gravity(grid):
    """Apply gravity to the board"""
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

def copy_grid(grid):
    """Create a deep copy of the grid"""
    new_grid = GridADT.__new__(GridADT)
    new_grid.rows = grid.rows
    new_grid.cols = grid.cols
    new_grid.board = [row[:] for row in grid.board]
    return new_grid

# ==========================================================
# STRATEGY 1: GREEDY
# ==========================================================
def greedy_best_move(grid):
    """Greedy Strategy: Pick largest component"""
    visited = set()
    best_component = None
    best_size = 0
    
    for r in range(grid.rows):
        for c in range(grid.cols):
            if (r, c) in visited or grid.board[r][c] is None:
                continue
            
            comp = []
            dfs(grid, r, c, grid.board[r][c], visited, comp)
            
            if len(comp) > 1 and len(comp) > best_size:
                best_size = len(comp)
                best_component = comp
    
    return best_component

# ==========================================================
# STRATEGY 2: DIVIDE & CONQUER + DP
# ==========================================================
def dp_score_difference(grid, memo, is_cpu_turn):
    """Returns maximum score difference from this state"""
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
            for r, c in comp:
                sim.board[r][c] = None
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
            for r, c in comp:
                sim.board[r][c] = None
            apply_gravity(sim)
            
            gain = len(comp) ** 2
            future = dp_score_difference(sim, memo, True)
            worst = min(worst, future - gain)
        
        memo[state] = worst
        return worst

def divide_board_regions(grid):
    """Split board into independent column regions"""
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

def conquer_region(grid, region_cols, memo):
    """Evaluate best move inside one independent region"""
    best_component = None
    best_value = float('-inf')
    
    components = get_all_components(grid)
    region_components = [
        comp for comp in components
        if all(c in region_cols for _, c in comp)
    ]
    
    for comp in region_components:
        sim = copy_grid(grid)
        for r, c in comp:
            sim.board[r][c] = None
        apply_gravity(sim)
        
        gain = len(comp) ** 2
        future = dp_score_difference(sim, memo, False)
        value = gain - future
        
        if value > best_value:
            best_value = value
            best_component = comp
    
    return best_component, best_value

def cpu_best_move_dc_dp(grid):
    """CPU move using Divide & Conquer + DP"""
    memo = {}
    regions = divide_board_regions(grid)
    
    if not regions:
        return None
    
    results = []
    for region_cols in regions:
        comp, value = conquer_region(grid, region_cols, memo)
        results.append((comp, value))
    
    # Combine results
    best_component = None
    best_value = float('-inf')
    
    for comp, value in results:
        if comp is not None and value > best_value:
            best_value = value
            best_component = comp
    
    return best_component

# ==========================================================
# STRATEGY 3: BACKTRACKING + MEMOIZATION
# ==========================================================
backtrack_cache = {}

def backtracking_score(grid):
    """Recursive backtracking to find maximum possible score"""
    state = tuple(tuple(row) for row in grid.board)
    
    if state in backtrack_cache:
        return backtrack_cache[state]
    
    components = get_all_components(grid)
    
    if not components:
        return 0
    
    best = 0
    for comp in components:
        sim = copy_grid(grid)
        for r, c in comp:
            sim.board[r][c] = None
        apply_gravity(sim)
        
        gain = len(comp) ** 2
        total = gain + backtracking_score(sim)
        best = max(best, total)
    
    backtrack_cache[state] = best
    return best

def backtracking_best_move(grid):
    """Backtracking Strategy with memoization"""
    global backtrack_cache
    backtrack_cache = {}
    
    components = get_all_components(grid)
    
    if not components:
        return None
    
    best_component = None
    best_total = -1
    
    for comp in components:
        sim = copy_grid(grid)
        for r, c in comp:
            sim.board[r][c] = None
        apply_gravity(sim)
        
        total = len(comp) ** 2 + backtracking_score(sim)
        
        if total > best_total:
            best_total = total
            best_component = comp
    
    return best_component

# ==========================================================
# HINT STRATEGY
# ==========================================================
def get_optimal_hint(grid):
    """Provide optimal hint for human player"""
    memo = {}
    components = get_all_components(grid)
    
    if not components:
        return None, 0
    
    best_component = None
    best_total = -1
    
    for comp in components:
        sim = copy_grid(grid)
        for r, c in comp:
            sim.board[r][c] = None
        apply_gravity(sim)
        
        future = -dp_score_difference(sim, memo, False)
        total = len(comp) ** 2 + future
        
        if total > best_total:
            best_total = total
            best_component = comp
    
    if best_component is None:
        return None, 0
    
    return best_component[0], len(best_component) ** 2

# ==========================================================
# SAME GAME GUI
# ==========================================================
class SameGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Same Game - ADT & DSA Edition")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1e293b')
        
        # Game state
        self.rows = 6
        self.cols = 6
        self.grid = None
        self.score = 0
        self.cpu_score = 0
        self.game_mode = None
        self.cpu_strategy = "greedy"
        self.selected_component = []
        self.is_animating = False
        self.game_over = False
        self.hint_mode = False
        
        # Cell size (dynamic based on board size)
        self.cell_size = 60
        
        self.show_menu()
    
    # ================= MENU =================
    def show_menu(self):
        self.clear_screen()
        
        frame = tk.Frame(self.root, bg='#1e293b')
        frame.place(relx=0.5, rely=0.5, anchor='center')
        
        tk.Label(frame, text="✨ SAME GAME ✨", 
                font=('Arial', 48, 'bold'), 
                fg='#fbbf24', bg='#1e293b').pack(pady=20)
        
        tk.Label(frame, text="ADT & DSA Implementation", 
                font=('Arial', 16), 
                fg='#94a3b8', bg='#1e293b').pack(pady=10)
        
        btn_style = {
            'font': ('Arial', 16, 'bold'),
            'width': 20,
            'height': 2,
            'bd': 0,
            'cursor': 'hand2'
        }
        
        tk.Button(frame, text="👤 Single Player", 
                 bg='#22c55e', fg='white',
                 command=lambda: self.start_game('single'),
                 **btn_style).pack(pady=10)
        
        tk.Button(frame, text="🤖 vs CPU", 
                 bg='#3b82f6', fg='white',
                 command=self.show_cpu_menu,
                 **btn_style).pack(pady=10)
        
        tk.Button(frame, text="⚙️ Board Size", 
                 bg='#64748b', fg='white',
                 command=self.show_settings,
                 **btn_style).pack(pady=10)
        
        tk.Button(frame, text="📖 How to Play", 
                 bg='#64748b', fg='white',
                 command=self.show_instructions,
                 **btn_style).pack(pady=10)
        
        tk.Label(frame, text=f"Current Board: {self.rows} × {self.cols}", 
                font=('Arial', 12), 
                fg='#94a3b8', bg='#1e293b').pack(pady=20)
    
    def show_cpu_menu(self):
        self.clear_screen()
        
        frame = tk.Frame(self.root, bg='#1e293b')
        frame.place(relx=0.5, rely=0.5, anchor='center')
        
        tk.Label(frame, text="🤖 Select CPU Strategy", 
                font=('Arial', 36, 'bold'), 
                fg='#fbbf24', bg='#1e293b').pack(pady=20)
        
        strategies = [
            ("greedy", "Greedy (Largest Component)", "#22c55e"),
            ("dc_dp", "Divide & Conquer + DP", "#3b82f6"),
            ("backtracking", "Backtracking + Memoization", "#eab308")
        ]
        
        for strategy, label, color in strategies:
            tk.Button(frame, text=label,
                     font=('Arial', 16, 'bold'),
                     width=25, height=2,
                     bg=color, fg='white',
                     bd=0, cursor='hand2',
                     command=lambda s=strategy: self.start_game_with_strategy(s)).pack(pady=8)
        
        tk.Button(frame, text="← Back",
                 font=('Arial', 14),
                 bg='#64748b', fg='white',
                 bd=0, cursor='hand2',
                 command=self.show_menu).pack(pady=20)
    
    def start_game_with_strategy(self, strategy):
        self.cpu_strategy = strategy
        self.start_game('multiplayer')
    
    # ================= SETTINGS =================
    def show_settings(self):
        self.clear_screen()
        
        frame = tk.Frame(self.root, bg='#1e293b')
        frame.place(relx=0.5, rely=0.5, anchor='center')
        
        tk.Label(frame, text="⚙️ Board Size", 
                font=('Arial', 36, 'bold'), 
                fg='#fbbf24', bg='#1e293b').pack(pady=20)
        
        sizes = [
            (6, 6, "Small (6×6)"),
            (8, 8, "Medium (8×8)"),
            (10, 10, "Large (10×10)"),
            (12, 8, "Wide (12×8)")
        ]
        
        for r, c, label in sizes:
            is_current = (self.rows == r and self.cols == c)
            tk.Button(frame, text=label,
                     font=('Arial', 16, 'bold'),
                     width=20, height=2,
                     bg='#eab308' if is_current else '#475569',
                     fg='white', bd=0, cursor='hand2',
                     command=lambda r=r, c=c: self.set_board_size(r, c)).pack(pady=5)
        
        tk.Button(frame, text="← Back",
                 font=('Arial', 14),
                 bg='#64748b', fg='white',
                 bd=0, cursor='hand2',
                 command=self.show_menu).pack(pady=20)
    
    def set_board_size(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.cell_size = min(600 // cols, 80)  # Dynamic cell sizing
        self.show_menu()
    
    # ================= INSTRUCTIONS =================
    def show_instructions(self):
        self.clear_screen()
        
        frame = tk.Frame(self.root, bg='#1e293b')
        frame.place(relx=0.5, rely=0.5, anchor='center')
        
        tk.Label(frame, text="📖 How to Play", 
                font=('Arial', 36, 'bold'), 
                fg='#fbbf24', bg='#1e293b').pack(pady=20)
        
        instructions = [
            "🎯 Click blocks to select connected same-color groups",
            "🎮 Minimum 2 blocks required to remove",
            "🏆 Score = (Blocks Removed)²",
            "⬇️ Gravity pulls remaining blocks down & shifts left",
            "🤖 CPU Strategies Available:",
            "   • Greedy: Largest component only",
            "   • Divide & Conquer + DP: Optimal region-based",
            "   • Backtracking: Exhaustive search with memoization",
            "💡 Press 'H' during game for optimal hint",
            "🏁 Game ends when no valid moves remain"
        ]
        
        for inst in instructions:
            tk.Label(frame, text=inst,
                    font=('Arial', 12),
                    fg='#e2e8f0', bg='#1e293b',
                    justify='left').pack(pady=2, anchor='w')
        
        tk.Button(frame, text="← Back to Menu",
                 font=('Arial', 14, 'bold'),
                 bg='#3b82f6', fg='white',
                 width=20, height=2,
                 bd=0, cursor='hand2',
                 command=self.show_menu).pack(pady=30)
    
    # ================= START GAME =================
    def start_game(self, mode):
        self.game_mode = mode
        self.grid = GridADT(self.rows, self.cols)
        self.score = 0
        self.cpu_score = 0
        self.game_over = False
        self.selected_component = []
        self.hint_mode = False
        self.show_game()
    
    # ================= GAME SCREEN =================
    def show_game(self):
        self.clear_screen()
        
        # Main container
        self.game_frame = tk.Frame(self.root, bg='#1e293b')
        self.game_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header
        header = tk.Frame(self.game_frame, bg='#334155', height=80)
        header.pack(fill='x', pady=(0, 10))
        
        # Back button
        tk.Button(header, text="🏠",
                 font=('Arial', 20),
                 bg='#475569', fg='white',
                 bd=0, cursor='hand2',
                 command=self.confirm_exit).pack(side='left', padx=10, pady=10)
        
        # Strategy info
        if self.game_mode == 'multiplayer':
            strategy_text = {
                'greedy': 'Greedy',
                'dc_dp': 'DC + DP',
                'backtracking': 'Backtracking'
            }.get(self.cpu_strategy, 'Unknown')
            
            tk.Label(header, text=f"🤖 CPU: {strategy_text}",
                    font=('Arial', 14, 'bold'),
                    fg='#94a3b8', bg='#334155').pack(side='left', padx=10)
        
        # Hint button
        tk.Button(header, text="💡 Hint",
                 font=('Arial', 14, 'bold'),
                 bg='#eab308', fg='black',
                 bd=0, cursor='hand2',
                 command=self.show_hint).pack(side='left', padx=10)
        
        # Scores
        self.score_frame = tk.Frame(header, bg='#334155')
        self.score_frame.pack(side='right', padx=10)
        
        # Board container with scroll if needed
        board_container = tk.Frame(self.game_frame, bg='#334155')
        board_container.pack(pady=10, expand=True, fill='both')
        
        # Canvas with dynamic sizing
        canvas_width = self.cols * self.cell_size
        canvas_height = self.rows * self.cell_size
        
        # Add scrollbars for large boards
        if canvas_width > 800 or canvas_height > 600:
            # Create canvas with scrollbars
            h_scroll = tk.Scrollbar(board_container, orient='horizontal')
            v_scroll = tk.Scrollbar(board_container, orient='vertical')
            
            self.canvas = tk.Canvas(board_container,
                                   width=min(canvas_width, 800),
                                   height=min(canvas_height, 600),
                                   bg='#1e293b',
                                   highlightthickness=0,
                                   xscrollcommand=h_scroll.set,
                                   yscrollcommand=v_scroll.set)
            
            h_scroll.config(command=self.canvas.xview)
            v_scroll.config(command=self.canvas.yview)
            
            # Grid layout
            self.canvas.grid(row=0, column=0, sticky='nsew')
            v_scroll.grid(row=0, column=1, sticky='ns')
            h_scroll.grid(row=1, column=0, sticky='ew')
            
            board_container.grid_rowconfigure(0, weight=1)
            board_container.grid_columnconfigure(0, weight=1)
            
            # Set scroll region
            self.canvas.config(scrollregion=(0, 0, canvas_width, canvas_height))
        else:
            self.canvas = tk.Canvas(board_container,
                                   width=canvas_width,
                                   height=canvas_height,
                                   bg='#1e293b',
                                   highlightthickness=0)
            self.canvas.pack(padx=20, pady=20)
        
        # Info label
        self.info_label = tk.Label(self.game_frame,
                                   text="",
                                   font=('Arial', 14, 'bold'),
                                   fg='#fbbf24', bg='#1e293b')
        self.info_label.pack(pady=10)
        
        # Bind keyboard for hints
        self.root.bind('<h>', lambda e: self.show_hint())
        self.root.bind('<H>', lambda e: self.show_hint())
        
        self.draw_board()
        self.update_scores()
    
    # ================= DRAW BOARD =================
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
                    
                    # Create cell with border
                    rect = self.canvas.create_rectangle(
                        x1 + 2, y1 + 2, x2 - 2, y2 - 2,
                        fill=color,
                        outline='white' if is_selected else '#1e293b',
                        width=3 if is_selected else 1,
                        tags=f'cell_{r}_{c}'
                    )
                    
                    # Add text label
                    self.canvas.create_text(
                        x1 + self.cell_size//2,
                        y1 + self.cell_size//2,
                        text=cell,
                        fill='white',
                        font=('Arial', self.cell_size//3, 'bold'),
                        tags=f'text_{r}_{c}'
                    )
                    
                    # Bind click event
                    self.canvas.tag_bind(f'cell_{r}_{c}', '<Button-1>',
                                        lambda e, r=r, c=c: self.handle_click(r, c))
                    self.canvas.tag_bind(f'text_{r}_{c}', '<Button-1>',
                                        lambda e, r=r, c=c: self.handle_click(r, c))
                else:
                    # Empty cell
                    self.canvas.create_rectangle(
                        x1 + 2, y1 + 2, x2 - 2, y2 - 2,
                        fill='#0f172a',
                        outline='#1e293b',
                        width=1
                    )
    
    # ================= HANDLE CLICK =================
    def handle_click(self, r, c):
        if self.is_animating or self.game_over:
            return
        
        comp = get_component(self.grid, r, c)
        
        if len(comp) < 2:
            self.info_label.config(text="❌ Need 2+ blocks to remove!")
            return
        
        self.selected_component = comp
        points = len(comp) ** 2
        self.info_label.config(text=f"✨ {len(comp)} blocks = {points} points")
        self.draw_board()
        
        # Auto-remove after selection
        self.root.after(300, lambda: self.remove_component(comp))
    
    # ================= REMOVE COMPONENT =================
    def remove_component(self, comp):
        self.is_animating = True
        
        # Remove blocks
        for r, c in comp:
            self.grid.board[r][c] = None
        
        # Update score
        self.score += len(comp) ** 2
        self.selected_component = []
        self.draw_board()
        
        # Apply gravity after short delay
        self.root.after(200, self.apply_gravity)
    
    # ================= GRAVITY =================
    def apply_gravity(self):
        apply_gravity(self.grid)
        self.draw_board()
        self.is_animating = False
        self.info_label.config(text="")
        self.update_scores()
        
        # Check game over
        if self.check_game_over():
            return
        
        # CPU turn in multiplayer
        if self.game_mode == 'multiplayer':
            self.root.after(500, self.cpu_turn)
    
    # ================= CPU TURN =================
    def cpu_turn(self):
        if self.game_over or self.is_animating:
            return
        
        self.is_animating = True
        self.info_label.config(text="🤖 CPU thinking...")
        self.draw_board()
        
        # Use selected strategy
        start_time = time.time()
        
        if self.cpu_strategy == "greedy":
            move = greedy_best_move(self.grid)
        elif self.cpu_strategy == "dc_dp":
            move = cpu_best_move_dc_dp(self.grid)
        elif self.cpu_strategy == "backtracking":
            move = backtracking_best_move(self.grid)
        else:
            move = greedy_best_move(self.grid)
        
        end_time = time.time()
        
        if not move:
            self.is_animating = False
            self.check_game_over()
            return
        
        # Show thinking time
        self.info_label.config(
            text=f"🤖 CPU found {len(move)} blocks in {end_time-start_time:.2f}s"
        )
        
        self.root.after(500, lambda: self.cpu_remove(move))
    
    def cpu_remove(self, comp):
        # Remove blocks
        for r, c in comp:
            self.grid.board[r][c] = None
        
        self.cpu_score += len(comp) ** 2
        self.draw_board()
        
        self.root.after(200, self.cpu_gravity)
    
    def cpu_gravity(self):
        apply_gravity(self.grid)
        self.draw_board()
        self.is_animating = False
        self.info_label.config(text="")
        self.update_scores()
        self.check_game_over()
    
    # ================= HINT =================
    def show_hint(self):
        if self.is_animating or self.game_over:
            return
        
        self.info_label.config(text="💡 Calculating optimal hint...")
        self.root.update()
        
        start_time = time.time()
        hint_cell, hint_score = get_optimal_hint(self.grid)
        end_time = time.time()
        
        if hint_cell:
            r, c = hint_cell
            self.info_label.config(
                text=f"💡 Hint: Click ({r}, {c}) for {hint_score} points "
                     f"(calc: {end_time-start_time:.2f}s)"
            )
            
            # Highlight hint cell
            self.selected_component = [hint_cell]
            self.draw_board()
            self.root.after(2000, self.clear_hint)
        else:
            self.info_label.config(text="❌ No valid moves available!")
    
    def clear_hint(self):
        self.selected_component = []
        self.draw_board()
        self.info_label.config(text="")
    
    # ================= GAME OVER CHECK =================
    def check_game_over(self):
        components = get_all_components(self.grid)
        
        if not components:
            self.game_over = True
            self.show_game_over()
            return True
        return False
    
    def show_game_over(self):
        if self.game_mode == 'multiplayer':
            if self.score > self.cpu_score:
                winner = "🎉 Human Wins!"
            elif self.cpu_score > self.score:
                winner = "🤖 CPU Wins!"
            else:
                winner = "🤝 It's a Tie!"
            
            msg = f"{winner}\n\nHuman: {self.score}\nCPU: {self.cpu_score}"
        else:
            msg = f"🏆 Game Over!\n\nFinal Score: {self.score}"
        
        res = messagebox.askquestion("Game Over",
                                     f"{msg}\n\nPlay again?",
                                     icon='question')
        
        if res == 'yes':
            self.start_game(self.game_mode)
        else:
            self.show_menu()
    
    # ================= UTILITIES =================
    def confirm_exit(self):
        if messagebox.askokcancel("Exit", "Return to main menu?"):
            self.root.unbind('<h>')
            self.root.unbind('<H>')
            self.show_menu()
    
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def update_scores(self):
        for widget in self.score_frame.winfo_children():
            widget.destroy()
        
        if self.game_mode == 'multiplayer':
            tk.Label(self.score_frame,
                    text=f"👤 Human: {self.score}",
                    font=('Arial', 16, 'bold'),
                    fg='#22c55e', bg='#334155').pack(side='left', padx=10)
            
            tk.Label(self.score_frame,
                    text="vs",
                    font=('Arial', 14),
                    fg='#94a3b8', bg='#334155').pack(side='left', padx=5)
            
            tk.Label(self.score_frame,
                    text=f"🤖 CPU: {self.cpu_score}",
                    font=('Arial', 16, 'bold'),
                    fg='#3b82f6', bg='#334155').pack(side='left', padx=10)
        else:
            tk.Label(self.score_frame,
                    text=f"🏆 Score: {self.score}",
                    font=('Arial', 18, 'bold'),
                    fg='#fbbf24', bg='#334155').pack(padx=10)

# ==========================================================
# BENCHMARK WINDOW
# ==========================================================
class BenchmarkWindow:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Strategy Benchmark")
        self.window.geometry("600x500")
        self.window.configure(bg='#1e293b')
        
        self.setup_ui()
    
    def setup_ui(self):
        tk.Label(self.window, text="📊 Strategy Benchmark",
                font=('Arial', 24, 'bold'),
                fg='#fbbf24', bg='#1e293b').pack(pady=20)
        
        # Board selection
        frame = tk.Frame(self.window, bg='#1e293b')
        frame.pack(pady=10)
        
        tk.Label(frame, text="Board Size:",
                font=('Arial', 12),
                fg='white', bg='#1e293b').pack(side='left', padx=5)
        
        self.size_var = tk.StringVar(value="6x6")
        sizes = ["6x6", "8x8", "10x10"]
        
        for size in sizes:
            tk.Radiobutton(frame, text=size, variable=self.size_var, value=size,
                          bg='#1e293b', fg='white', selectcolor='#1e293b',
                          font=('Arial', 10)).pack(side='left', padx=5)
        
        # Run button
        tk.Button(self.window, text="Run Benchmark",
                 font=('Arial', 14, 'bold'),
                 bg='#3b82f6', fg='white',
                 command=self.run_benchmark).pack(pady=20)
        
        # Results text
        self.results_text = tk.Text(self.window,
                                    height=15,
                                    width=60,
                                    bg='#0f172a',
                                    fg='#e2e8f0',
                                    font=('Courier', 10))
        self.results_text.pack(pady=10, padx=20)
    
    def run_benchmark(self):
        self.results_text.delete(1.0, tk.END)
        
        # Parse board size
        size_str = self.size_var.get()
        rows, cols = map(int, size_str.split('x'))
        
        # Create fixed board for fair comparison
        random.seed(42)
        grid = GridADT(rows, cols)
        
        self.results_text.insert(tk.END, f"Benchmark on {rows}×{cols} board\n")
        self.results_text.insert(tk.END, "="*50 + "\n\n")
        
        strategies = [
            ("Greedy", greedy_best_move),
            ("DC+DP", cpu_best_move_dc_dp),
            ("Backtracking", backtracking_best_move)
        ]
        
        for name, strategy in strategies:
            self.results_text.insert(tk.END, f"Testing {name}...\n")
            self.window.update()
            
            # Copy grid
            test_grid = copy_grid(grid)
            score = 0
            moves = 0
            
            start_time = time.time()
            
            while True:
                move = strategy(test_grid)
                if not move:
                    break
                
                for r, c in move:
                    test_grid.board[r][c] = None
                apply_gravity(test_grid)
                
                score += len(move) ** 2
                moves += 1
            
            end_time = time.time()
            
            self.results_text.insert(tk.END,
                f"{name:12} Score: {score:<6} Moves: {moves:<4} Time: {end_time-start_time:.3f}s\n")
            self.window.update()
        
        self.results_text.insert(tk.END, "\n" + "="*50 + "\n")

# ================= MAIN =================
if __name__ == "__main__":
    root = tk.Tk()
    app = SameGameGUI(root)
    root.mainloop()
