import tkinter as tk
from tkinter import messagebox
import random
import os
import sys
import time

sys.setrecursionlimit(10000)

# ==========================================================
# SAME GAME - DP + MERGE SORT VISUALIZATION (CPU NOW OPTIMAL)
# ==========================================================

COLORS = ['R', 'G', 'B', 'Y']
COLOR_MAP = {
    'R': '#ef4444',  # Red
    'G': '#22c55e',  # Green
    'B': '#3b82f6',  # Blue
    'Y': '#eab308',  # Yellow
}

HIGH_SCORE_FILE = "samegame_highscore.txt"

# ---------- DP memoization (global) ----------
memo = {}
move_memo = {}  # New: Store best move for each state

# ---------- Helper for hover effects ----------
def on_enter(e, btn, color):
    btn['background'] = color

def on_leave(e, btn, color):
    btn['background'] = color

# ---------- Enhanced Tooltip class with safe bbox handling ----------
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        widget.bind('<Enter>', self.show_tip)
        widget.bind('<Leave>', self.hide_tip)

    def show_tip(self, event=None):
        try:
            x, y, _, _ = self.widget.bbox("insert")
            x += self.widget.winfo_rootx() + 25
            y += self.widget.winfo_rooty() + 25
        except:
            x = self.widget.winfo_rootx() + 25
            y = self.widget.winfo_rooty() + 25
            
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("Segoe UI", 10))
        label.pack()

    def hide_tip(self, event=None):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None

# ==========================================================
# GRID ADT
# ==========================================================
class GridADT:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.board = [[random.choice(COLORS) for _ in range(cols)]
                      for _ in range(rows)]

# ==========================================================
# GRAPH ADT
# ==========================================================
class GraphADT:
    @staticmethod
    def neighbors(r, c):
        return [(r+1, c), (r-1, c), (r, c+1), (r, c-1)]

# ==========================================================
# DFS (CONNECTED COMPONENT) - operates on board list
# ==========================================================
def dfs(board, r, c, color, visited, component):
    rows = len(board)
    cols = len(board[0])
    if r < 0 or r >= rows or c < 0 or c >= cols:
        return
    if (r, c) in visited:
        return
    if board[r][c] != color:
        return

    visited.add((r, c))
    component.append((r, c))

    for nr, nc in GraphADT.neighbors(r, c):
        dfs(board, nr, nc, color, visited, component)

def get_component(board, r, c):
    if board[r][c] is None:
        return []
    visited = set()
    component = []
    dfs(board, r, c, board[r][c], visited, component)
    return component

def get_all_components(board):
    """Get all valid components (size > 1) from the board"""
    rows = len(board)
    cols = len(board[0])
    components = []
    visited = set()
    
    for r in range(rows):
        for c in range(cols):
            if board[r][c] and (r, c) not in visited:
                comp = get_component(board, r, c)
                for cell in comp:
                    visited.add(cell)
                if len(comp) > 1:
                    components.append(comp)
    
    return components

# ==========================================================
# REMOVE COMPONENT, GRAVITY, SHIFT LEFT (board operations)
# ==========================================================
def remove_component(board, component):
    for r, c in component:
        board[r][c] = None

def apply_gravity(board):
    rows = len(board)
    cols = len(board[0])
    for c in range(cols):
        stack = []
        for r in range(rows):
            if board[r][c]:
                stack.append(board[r][c])
        for r in range(rows-1, -1, -1):
            board[r][c] = stack.pop() if stack else None

def shift_left(board):
    rows = len(board)
    cols = len(board[0])
    columns = [[board[r][c] for r in range(rows)] for c in range(cols)]
    columns = [col for col in columns if any(cell is not None for cell in col)]
    while len(columns) < cols:
        columns.append([None] * rows)
    for c in range(cols):
        for r in range(rows):
            board[r][c] = columns[c][r]

def apply_gravity_and_shift(board):
    apply_gravity(board)
    shift_left(board)

# ==========================================================
# GAME OVER CHECK (board)
# ==========================================================
def is_game_over(board):
    return len(get_all_components(board)) == 0

# ==========================================================
# MERGE SORT (sorts components by score descending)
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
# ENHANCED DYNAMIC PROGRAMMING (stores both score AND best move)
# ==========================================================
def board_to_tuple(board):
    """Convert board to immutable tuple for memoization"""
    return tuple(tuple(row) for row in board)

def copy_board(board):
    """Create a deep copy of the board"""
    return [row[:] for row in board]

def dp_best_score_and_move(board):
    """
    ENHANCED: Returns (max_score, best_component) for current board state
    This ensures we know WHICH move leads to the best score
    """
    global memo, move_memo
    state = board_to_tuple(board)
    
    # Check memo
    if state in memo and state in move_memo:
        return memo[state], move_memo[state]

    # Get all valid moves
    components = get_all_components(board)
    
    # Base case: no moves left
    if not components:
        memo[state] = 0
        move_memo[state] = []
        return 0, []

    # Try each possible move and find the best
    best_score = -1
    best_component = None
    
    for comp in components:
        # Create new board after this move
        temp = copy_board(board)
        remove_component(temp, comp)
        apply_gravity_and_shift(temp)
        
        # Calculate score: current move score + best future score
        current_score = len(comp) ** 2
        future_score, _ = dp_best_score_and_move(temp)
        total_score = current_score + future_score
        
        if total_score > best_score:
            best_score = total_score
            best_component = comp

    memo[state] = best_score
    move_memo[state] = best_component
    return best_score, best_component

def dp_best_score(board):
    """Wrapper for backward compatibility"""
    score, _ = dp_best_score_and_move(board)
    return score

# ==========================================================
# ENHANCED CPU BEST MOVE (Now truly optimal)
# ==========================================================
def cpu_best_move(board):
    """
    ENHANCED: Returns (best_component, sorted_components_list)
    Uses DP to find the truly optimal first move
    """
    # Get the optimal first move from DP
    _, best_component = dp_best_score_and_move(board)
    
    if not best_component:
        return [], []

    # For display purposes, evaluate all moves
    components = get_all_components(board)
    move_scores = []
    
    for comp in components:
        temp = copy_board(board)
        remove_component(temp, comp)
        apply_gravity_and_shift(temp)
        
        current_score = len(comp) ** 2
        future_score = dp_best_score(temp)
        total_score = current_score + future_score
        
        move_scores.append((total_score, comp))
    
    # Sort by total score descending using merge sort
    sorted_moves = merge_sort_components(move_scores)
    
    return best_component, sorted_moves

# ==========================================================
# SAME GAME GUI (ENHANCED + OPTIMAL CPU)
# ==========================================================
class SameGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Same Game - Optimal CPU (Always Wins)")
        self.root.geometry("1400x850")
        self.root.configure(bg='#0b1120')
        
        # Game state
        self.rows = 6
        self.cols = 6
        self.grid = None
        self.score = 0
        self.cpu_score = 0
        self.high_score = self.load_high_score()
        self.game_mode = None
        self.selected_component = []
        self.is_animating = False
        self.game_over = False
        self.dp_analysis_running = False
        
        # Stats tracking
        self.human_wins = 0
        self.cpu_wins = 0
        self.games_played = 0
        
        # Cell size
        self.cell_size = 70
        self.corner_radius = 10
        
        # Colors for hover effects
        self.btn_colors = {
            'single': '#22c55e',
            'cpu': '#3b82f6',
            'settings': '#64748b',
            'howto': '#64748b',
            'back': '#64748b',
            'home': '#475569',
            'hint': '#f59e0b',
            'newgame': '#10b981',
            'analyze': '#8b5cf6',
        }
        
        self.show_menu()
    
    # ---------- Utility: Clear screen ----------
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    # ---------- Hover setup for buttons ----------
    def add_hover(self, widget, color_key):
        normal = self.btn_colors.get(color_key, '#64748b')
        r = int(normal[1:3], 16)
        g = int(normal[3:5], 16)
        b = int(normal[5:7], 16)
        r = min(255, r + 40)
        g = min(255, g + 40)
        b = min(255, b + 40)
        hover = f'#{r:02x}{g:02x}{b:02x}'
        widget.bind("<Enter>", lambda e, btn=widget, col=hover: on_enter(e, btn, col))
        widget.bind("<Leave>", lambda e, btn=widget, col=normal: on_leave(e, btn, col))
    
    # ---------- Load/save high score ----------
    def load_high_score(self):
        if os.path.exists(HIGH_SCORE_FILE):
            try:
                with open(HIGH_SCORE_FILE, 'r') as f:
                    return int(f.read())
            except:
                return 0
        return 0
    
    def save_high_score(self, score):
        if score > self.high_score:
            self.high_score = score
            with open(HIGH_SCORE_FILE, 'w') as f:
                f.write(str(score))
    
    # ================= MENU =================
    def show_menu(self):
        self.clear_screen()
        
        frame = tk.Frame(self.root, bg='#1e293b', bd=2, relief='flat')
        frame.place(relx=0.5, rely=0.5, anchor='center', width=600, height=650)
        
        tk.Label(frame, text="✨ SAME GAME ✨", 
                font=('Segoe UI', 48, 'bold'), 
                fg='#fbbf24', bg='#1e293b').pack(pady=(40,10))
        
        tk.Label(frame, text="Match & Remove Connected Blocks", 
                font=('Segoe UI', 16), 
                fg='#94a3b8', bg='#1e293b').pack(pady=10)
        
        btn_style = {
            'font': ('Segoe UI', 16, 'bold'),
            'width': 20,
            'height': 2,
            'bd': 0,
            'cursor': 'hand2',
            'relief': 'flat'
        }
        
        # Single Player
        btn_single = tk.Button(frame, text="👤 Single Player", 
                               bg='#22c55e', fg='white',
                               command=lambda: self.start_game('single'),
                               **btn_style)
        btn_single.pack(pady=10)
        self.add_hover(btn_single, 'single')
        ToolTip(btn_single, "Play alone – try to beat the high score!")
        
        # vs CPU
        btn_cpu = tk.Button(frame, text="🤖 vs CPU (Optimal DP)", 
                            bg='#3b82f6', fg='white',
                            command=lambda: self.start_game('multiplayer'),
                            **btn_style)
        btn_cpu.pack(pady=10)
        self.add_hover(btn_cpu, 'cpu')
        ToolTip(btn_cpu, "Challenge the computer (Now truly optimal!)")
        
        # Board Size
        btn_settings = tk.Button(frame, text="⚙️ Board Size", 
                                 bg='#64748b', fg='white',
                                 command=self.show_settings,
                                 **btn_style)
        btn_settings.pack(pady=10)
        self.add_hover(btn_settings, 'settings')
        ToolTip(btn_settings, "Change the board dimensions")
        
        # How to Play
        btn_howto = tk.Button(frame, text="📖 How to Play", 
                              bg='#64748b', fg='white',
                              command=self.show_instructions,
                              **btn_style)
        btn_howto.pack(pady=10)
        self.add_hover(btn_howto, 'howto')
        ToolTip(btn_howto, "Learn the rules")
        
        # Stats display
        stats_frame = tk.Frame(frame, bg='#1e293b')
        stats_frame.pack(pady=20)
        
        win_rate = 0
        if self.games_played > 0:
            win_rate = (self.cpu_wins / self.games_played) * 100
        
        tk.Label(stats_frame, 
                text=f"CPU Wins: {self.cpu_wins} | Human Wins: {self.human_wins}",
                font=('Segoe UI', 12), 
                fg='#94a3b8', bg='#1e293b').pack()
        
        tk.Label(stats_frame, 
                text=f"CPU Win Rate: {win_rate:.1f}%",
                font=('Segoe UI', 12, 'bold'), 
                fg='#fbbf24' if win_rate > 50 else '#ef4444', 
                bg='#1e293b').pack()
        
        # High score display
        high_score_text = f"High Score: {self.high_score}" if self.high_score > 0 else "No high score yet"
        tk.Label(frame, text=high_score_text, 
                font=('Segoe UI', 12, 'bold'), 
                fg='#fbbf24', bg='#1e293b').pack(pady=10)
        
        tk.Label(frame, text=f"Current Board: {self.rows} × {self.cols}", 
                font=('Segoe UI', 12), 
                fg='#94a3b8', bg='#1e293b').pack(pady=5)
    
    # ================= SETTINGS =================
    def show_settings(self):
        self.clear_screen()
        
        frame = tk.Frame(self.root, bg='#1e293b', bd=2, relief='flat')
        frame.place(relx=0.5, rely=0.5, anchor='center', width=500, height=500)
        
        tk.Label(frame, text="⚙️ Board Size", 
                font=('Segoe UI', 36, 'bold'), 
                fg='#fbbf24', bg='#1e293b').pack(pady=40)
        
        sizes = [
            (6, 6, "Small (6×6)"),
            (8, 8, "Medium (8×8)"),
            (10, 10, "Large (10×10)")
        ]
        
        for r, c, label in sizes:
            is_current = (self.rows == r and self.cols == c)
            btn = tk.Button(frame, text=label,
                           font=('Segoe UI', 16, 'bold'),
                           width=20, height=2,
                           bg='#eab308' if is_current else '#475569',
                           fg='white', bd=0, cursor='hand2',
                           command=lambda r=r, c=c: self.set_board_size(r, c))
            btn.pack(pady=5)
            if not is_current:
                self.add_hover(btn, 'settings')
            ToolTip(btn, f"{r}×{c} board")
        
        btn_back = tk.Button(frame, text="← Back",
                            font=('Segoe UI', 14),
                            bg='#64748b', fg='white',
                            bd=0, cursor='hand2',
                            command=self.show_menu)
        btn_back.pack(pady=20)
        self.add_hover(btn_back, 'back')
        ToolTip(btn_back, "Return to main menu")
    
    def set_board_size(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.cell_size = min(70, 800 // max(rows, cols))
        self.show_menu()
    
    # ================= INSTRUCTIONS =================
    def show_instructions(self):
        self.clear_screen()
        
        frame = tk.Frame(self.root, bg='#1e293b', bd=2, relief='flat')
        frame.place(relx=0.5, rely=0.5, anchor='center', width=700, height=500)
        
        tk.Label(frame, text="📖 How to Play", 
                font=('Segoe UI', 36, 'bold'), 
                fg='#fbbf24', bg='#1e293b').pack(pady=30)
        
        instructions = [
            "🎯 Click blocks to select connected same-color groups",
            "🎮 Minimum 2 blocks required to remove",
            "🏆 Score = (Blocks Removed)²",
            "⬇️ Gravity pulls blocks down, then shifts left",
            "🤖 CPU uses Optimal Dynamic Programming",
            "   - Evaluates ALL possible sequences recursively",
            "   - Always chooses the move leading to maximum total score",
            "   - This makes the CPU virtually unbeatable!",
            "📊 Right panel shows top moves from DP analysis",
            "🏁 Game ends when no valid moves remain"
        ]
        
        for inst in instructions:
            tk.Label(frame, text=inst,
                    font=('Segoe UI', 14),
                    fg='#e2e8f0', bg='#1e293b',
                    justify='left').pack(pady=5, anchor='w', padx=40)
        
        btn_back = tk.Button(frame, text="← Back to Menu",
                            font=('Segoe UI', 14, 'bold'),
                            bg='#3b82f6', fg='white',
                            width=20, height=2,
                            bd=0, cursor='hand2',
                            command=self.show_menu)
        btn_back.pack(pady=30)
        self.add_hover(btn_back, 'cpu')
        ToolTip(btn_back, "Return to main menu")
    
    # ================= START GAME =================
    def start_game(self, mode):
        global memo, move_memo
        memo = {}  # Reset DP memoization
        move_memo = {}  # Reset move memoization
        
        self.game_mode = mode
        self.grid = GridADT(self.rows, self.cols)
        self.score = 0
        self.cpu_score = 0
        self.game_over = False
        self.selected_component = []
        self.dp_analysis_running = False
        self.show_game()
    
    # ================= GAME SCREEN =================
    def show_game(self):
        self.clear_screen()
        
        # Main horizontal container: left for game, right for DP visualization
        main_container = tk.Frame(self.root, bg='#0b1120')
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Left frame (game) - store as self.game_frame for overlay/popup
        left_frame = tk.Frame(main_container, bg='#0b1120')
        left_frame.pack(side='left', fill='both', expand=True)
        self.game_frame = left_frame
        
        # Right frame (DP visualization)
        right_frame = tk.Frame(main_container, bg='#1e293b', width=300)
        right_frame.pack(side='right', fill='y', padx=(10,0))
        right_frame.pack_propagate(False)
        
        # Title for right panel
        tk.Label(right_frame, text="📊 Optimal DP Analysis", 
                font=('Segoe UI', 16, 'bold'),
                fg='#fbbf24', bg='#1e293b').pack(pady=10)
        
        # Text widget to show sorted components
        self.dp_text = tk.Text(right_frame, height=20, width=30,
                               bg='#0f172a', fg='#e2e8f0',
                               font=('Consolas', 10), wrap=tk.WORD)
        self.dp_text.pack(padx=10, pady=10, fill='both', expand=True)
        
        # Analyze button
        btn_analyze = tk.Button(right_frame, text="🔍 Analyze Current Board",
                                font=('Segoe UI', 12),
                                bg='#8b5cf6', fg='white',
                                bd=0, cursor='hand2',
                                command=self.analyze_board)
        btn_analyze.pack(pady=10)
        self.add_hover(btn_analyze, 'analyze')
        ToolTip(btn_analyze, "Run Optimal DP analysis")
        
        # ----- Game area (left_frame) -----
        # Header
        header_bg = '#1e293b'
        header = tk.Frame(left_frame, bg=header_bg, height=80)
        header.pack(fill='x', pady=(0, 20))
        header.pack_propagate(False)
        
        # Home button
        btn_home = tk.Button(header, text="🏠",
                            font=('Segoe UI', 20),
                            bg='#475569', fg='white',
                            bd=0, cursor='hand2',
                            command=self.confirm_exit)
        btn_home.pack(side='left', padx=15, pady=15)
        self.add_hover(btn_home, 'home')
        ToolTip(btn_home, "Return to main menu")
        
        # Title
        tk.Label(header, text="SAME GAME",
                font=('Segoe UI', 24, 'bold'),
                fg='white', bg=header_bg).pack(side='left', padx=10)
        
        # Hint and New Game buttons
        btn_hint = tk.Button(header, text="💡 Hint",
                            font=('Segoe UI', 14),
                            bg='#f59e0b', fg='white',
                            bd=0, cursor='hand2',
                            command=self.show_hint)
        btn_hint.pack(side='right', padx=10, pady=15)
        self.add_hover(btn_hint, 'hint')
        ToolTip(btn_hint, "Highlight the optimal move")
        
        btn_new = tk.Button(header, text="🔄 New Game",
                           font=('Segoe UI', 14),
                           bg='#10b981', fg='white',
                           bd=0, cursor='hand2',
                           command=self.restart_game)
        btn_new.pack(side='right', padx=10, pady=15)
        self.add_hover(btn_new, 'newgame')
        ToolTip(btn_new, "Start a new game")
        
        # Score frame
        self.score_frame = tk.Frame(header, bg=header_bg)
        self.score_frame.pack(side='right', padx=20)
        
        # Board container with shadow
        board_shadow = tk.Frame(left_frame, bg='#000000', bd=0)
        board_shadow.pack(pady=10)
        self.board_container = tk.Frame(board_shadow, bg='#1e293b', padx=10, pady=10)
        self.board_container.pack()
        
        # Canvas
        canvas_width = self.cols * self.cell_size
        canvas_height = self.rows * self.cell_size
        self.canvas = tk.Canvas(self.board_container,
                                width=canvas_width,
                                height=canvas_height,
                                bg='#0f172a',
                                highlightthickness=2,
                                highlightbackground='#334155')
        self.canvas.pack()
        
        # Bind hover for cell highlighting
        self.canvas.bind("<Motion>", self.on_cell_hover)
        self.hover_cell = None
        
        # Info label
        self.info_label = tk.Label(left_frame,
                                   text="",
                                   font=('Segoe UI', 14, 'bold'),
                                   fg='#fbbf24', bg='#0b1120')
        self.info_label.pack(pady=10)
        
        # Status bar
        self.status_bar = tk.Label(left_frame,
                                   text="Ready",
                                   font=('Segoe UI', 10),
                                   fg='#94a3b8', bg='#0b1120',
                                   anchor='w')
        self.status_bar.pack(fill='x', padx=10, pady=(0,10))
        
        self.draw_board()
        self.update_scores()
    
    # ================= ROUNDED RECTANGLE =================
    def create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        points = [x1+radius, y1,
                  x2-radius, y1,
                  x2, y1,
                  x2, y1+radius,
                  x2, y2-radius,
                  x2, y2,
                  x2-radius, y2,
                  x1+radius, y2,
                  x1, y2,
                  x1, y2-radius,
                  x1, y1+radius,
                  x1, y1]
        return self.canvas.create_polygon(points, smooth=True, **kwargs)
    
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
                    
                    # Shadow
                    self.create_rounded_rect(
                        x1+4, y1+4, x2, y2,
                        self.corner_radius,
                        fill='#000000', outline='', tags='shadow'
                    )
                    
                    # Main cell
                    outline_color = 'white' if is_selected else color
                    outline_width = 4 if is_selected else 1
                    self.create_rounded_rect(
                        x1+2, y1+2, x2-2, y2-2,
                        self.corner_radius,
                        fill=color,
                        outline=outline_color,
                        width=outline_width,
                        tags=f'cell_{r}_{c}'
                    )
                    
                    self.canvas.tag_bind(f'cell_{r}_{c}', '<Button-1>',
                                        lambda e, r=r, c=c: self.handle_click(r, c))
                else:
                    self.create_rounded_rect(
                        x1+2, y1+2, x2-2, y2-2,
                        self.corner_radius,
                        fill='#0f172a',
                        outline='#1e293b',
                        width=1
                    )
    
    # ================= CELL HOVER HIGHLIGHT =================
    def on_cell_hover(self, event):
        if self.is_animating or self.game_over or self.dp_analysis_running:
            return
        c = event.x // self.cell_size
        r = event.y // self.cell_size
        if 0 <= r < self.rows and 0 <= c < self.cols and self.grid.board[r][c]:
            if self.hover_cell != (r, c):
                if self.hover_cell:
                    hr, hc = self.hover_cell
                    self.canvas.itemconfig(f'cell_{hr}_{hc}', width=1, outline=COLOR_MAP[self.grid.board[hr][hc]])
                self.canvas.itemconfig(f'cell_{r}_{c}', width=3, outline='white')
                self.hover_cell = (r, c)
        else:
            if self.hover_cell:
                hr, hc = self.hover_cell
                self.canvas.itemconfig(f'cell_{hr}_{hc}', width=1, outline=COLOR_MAP[self.grid.board[hr][hc]])
                self.hover_cell = None
    
    # ================= DFS (using board) =================
    def get_component(self, r, c):
        if not self.grid.board[r][c]:
            return []
        visited = set()
        comp = []
        dfs(self.grid.board, r, c, self.grid.board[r][c], visited, comp)
        return comp
    
    # ================= HANDLE CLICK =================
    def handle_click(self, r, c):
        if self.is_animating or self.game_over or self.dp_analysis_running:
            return
        
        comp = self.get_component(r, c)
        
        if len(comp) < 2:
            self.info_label.config(text="❌ Invalid move! Need 2+ blocks")
            self.status_bar.config(text="Select a group of 2 or more same-colored blocks")
            return
        
        self.selected_component = comp
        points = len(comp) ** 2
        self.info_label.config(text=f"✨ {len(comp)} blocks = {points} points")
        self.draw_board()
        
        self.show_points_popup(points, r, c)
        
        self.root.after(300, lambda: self.remove_component(comp))
    
    def show_points_popup(self, points, r, c):
        x = c * self.cell_size + self.cell_size//2
        y = r * self.cell_size + self.cell_size//2
        popup = self.canvas.create_text(x, y, text=f"+{points}", 
                                        fill='white', font=('Segoe UI', 16, 'bold'),
                                        tags='popup')
        def animate_popup(step=0):
            if step < 20:
                self.canvas.move(popup, 0, -2)
                self.canvas.itemconfig(popup, fill=f'#ffff{255-step*12:02x}')
                self.root.after(30, lambda: animate_popup(step+1))
            else:
                self.canvas.delete(popup)
        animate_popup()
    
    # ================= REMOVE COMPONENT WITH FADE =================
    def remove_component(self, comp):
        self.is_animating = True
        
        def fade_step(step=0):
            if step < 10:
                for r, c in comp:
                    self.canvas.itemconfig(f'cell_{r}_{c}', fill='#ffffff')
                self.root.after(30, lambda: fade_step(step+1))
            else:
                for r, c in comp:
                    self.grid.board[r][c] = None
                self.score += len(comp) ** 2
                self.selected_component = []
                self.draw_board()
                self.root.after(200, self.apply_gravity)
        fade_step()
    
    # ================= GRAVITY WITH ANIMATION =================
    def apply_gravity(self):
        def gravity_step():
            moved = False
            for c in range(self.cols):
                for r in range(self.rows-1, 0, -1):
                    if self.grid.board[r][c] is None and self.grid.board[r-1][c] is not None:
                        self.grid.board[r][c], self.grid.board[r-1][c] = self.grid.board[r-1][c], None
                        moved = True
            if moved:
                self.draw_board()
                self.root.after(50, gravity_step)
            else:
                self.shift_left()
                self.draw_board()
                self.is_animating = False
                self.info_label.config(text="")
                self.update_scores()
                
                if self.game_mode == 'multiplayer':
                    self.root.after(500, self.cpu_turn)
                else:
                    self.check_game_over()
        gravity_step()
    
    # ================= SHIFT LEFT =================
    def shift_left(self):
        columns = [[self.grid.board[r][c] for r in range(self.rows)]
                   for c in range(self.cols)]
        columns = [col for col in columns if any(cell is not None for cell in col)]
        while len(columns) < self.cols:
            columns.append([None] * self.rows)
        for c in range(self.cols):
            for r in range(self.rows):
                self.grid.board[r][c] = columns[c][r]
    
    # ================= OPTIMAL CPU TURN =================
    def cpu_turn(self):
        if self.game_over:
            return
        
        self.is_animating = True
        self.dp_analysis_running = True
        self.info_label.config(text="🤖 CPU finding optimal move...")
        self.status_bar.config(text="CPU analyzing all possible sequences...")
        self.root.update()
        
        # Use after to prevent UI freezing
        self.root.after(100, self._execute_cpu_turn)
    
    def _execute_cpu_turn(self):
        # Run optimal DP analysis
        best_comp, sorted_moves = cpu_best_move(self.grid.board)
        
        # Display sorted components in right panel
        self.display_dp_analysis(sorted_moves)
        
        if not best_comp:
            self.dp_analysis_running = False
            self.check_game_over()
            return
        
        # Highlight CPU's optimal move
        self.selected_component = best_comp
        self.draw_board()
        self.dp_analysis_running = False
        self.root.after(500, lambda: self.cpu_remove_animate(best_comp))
    
    def cpu_remove_animate(self, comp):
        def fade_step(step=0):
            if step < 10:
                for r, c in comp:
                    self.canvas.itemconfig(f'cell_{r}_{c}', fill='#ffffff')
                self.root.after(30, lambda: fade_step(step+1))
            else:
                for r, c in comp:
                    self.grid.board[r][c] = None
                self.cpu_score += len(comp) ** 2
                self.selected_component = []
                self.draw_board()
                self.root.after(200, self.cpu_gravity)
        fade_step()
    
    def cpu_gravity(self):
        def gravity_step():
            moved = False
            for c in range(self.cols):
                for r in range(self.rows-1, 0, -1):
                    if self.grid.board[r][c] is None and self.grid.board[r-1][c] is not None:
                        self.grid.board[r][c], self.grid.board[r-1][c] = self.grid.board[r-1][c], None
                        moved = True
            if moved:
                self.draw_board()
                self.root.after(50, gravity_step)
            else:
                self.shift_left()
                self.draw_board()
                self.is_animating = False
                self.info_label.config(text="")
                self.status_bar.config(text="CPU played optimal move")
                self.update_scores()
                self.check_game_over()
        gravity_step()
    
    # ================= DP ANALYSIS DISPLAY =================
    def display_dp_analysis(self, sorted_moves):
        self.dp_text.delete(1.0, tk.END)
        if not sorted_moves:
            self.dp_text.insert(tk.END, "No valid moves.")
            return
        
        self.dp_text.insert(tk.END, "📊 OPTIMAL DP ANALYSIS\n")
        self.dp_text.insert(tk.END, "="*35 + "\n\n")
        self.dp_text.insert(tk.END, "All possible moves (total score):\n\n")
        
        for i, (score, comp) in enumerate(sorted_moves[:5]):  # show top 5
            # Mark the optimal move
            prefix = "⭐ OPTIMAL" if i == 0 else "   "
            self.dp_text.insert(tk.END, f"{prefix} {i+1}. Score: {score}\n")
            self.dp_text.insert(tk.END, f"       Blocks: {len(comp)} at {comp[0]}\n\n")
    
    def analyze_board(self):
        if self.is_animating or self.game_over or not self.grid or self.dp_analysis_running:
            return
        
        self.dp_analysis_running = True
        self.info_label.config(text="🔍 Running optimal DP analysis...")
        self.status_bar.config(text="Analyzing all possible sequences (may take a moment)...")
        self.root.update()
        
        # Use after to prevent UI freezing
        self.root.after(100, self._execute_analysis)
    
    def _execute_analysis(self):
        start_time = time.time()
        best_comp, sorted_moves = cpu_best_move(self.grid.board)
        elapsed = time.time() - start_time
        
        self.display_dp_analysis(sorted_moves)
        
        if best_comp:
            self.selected_component = best_comp
            self.draw_board()
            self.info_label.config(text=f"⭐ OPTIMAL MOVE: {len(best_comp)} blocks → {sorted_moves[0][0]} pts")
            self.status_bar.config(text=f"Optimal analysis complete in {elapsed:.2f}s")
        else:
            self.info_label.config(text="⚠️ No valid moves!")
            self.status_bar.config(text="No valid moves available")
        
        self.dp_analysis_running = False
    
    # ================= HINT =================
    def show_hint(self):
        if self.is_animating or self.game_over or self.dp_analysis_running:
            return
        best_comp, _ = cpu_best_move(self.grid.board)
        if best_comp:
            self.selected_component = best_comp
            self.draw_board()
            self.info_label.config(text=f"⭐ OPTIMAL MOVE: {len(best_comp)} blocks")
            self.status_bar.config(text="Hint: This is the optimal move")
        else:
            self.info_label.config(text="⚠️ No valid moves!")
            self.status_bar.config(text="Game over - no moves available")
    
    # ================= GAME OVER =================
    def check_game_over(self):
        if is_game_over(self.grid.board):
            self.game_over = True
            if self.game_mode == 'single':
                self.save_high_score(self.score)
            elif self.game_mode == 'multiplayer':
                self.games_played += 1
                if self.cpu_score > self.score:
                    self.cpu_wins += 1
                elif self.score > self.cpu_score:
                    self.human_wins += 1
            self.show_game_over()
    
    def show_game_over(self):
        # Semi‑transparent overlay
        overlay = tk.Frame(self.game_frame, bg='#000000', bd=0)
        overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        overlay.lower()
        
        # Popup frame
        popup = tk.Frame(self.game_frame, bg='#1e293b', bd=2, relief='raised')
        popup.place(relx=0.5, rely=0.5, anchor='center', width=450, height=400)
        
        if self.game_mode == 'multiplayer':
            if self.score > self.cpu_score:
                winner = "🎉 Human Wins! (Rare victory!)"
                win_color = '#22c55e'
            elif self.cpu_score > self.score:
                winner = "🤖 CPU Wins! (Optimal play prevails)"
                win_color = '#3b82f6'
            else:
                winner = "🤝 It's a Tie!"
                win_color = '#94a3b8'
            
            msg = f"{winner}\n\nHuman: {self.score}\nCPU: {self.cpu_score}"
            
            # Show win rate stats
            win_rate = 0
            if self.games_played > 0:
                win_rate = (self.cpu_wins / self.games_played) * 100
            
            stats = f"\nCPU Win Rate: {win_rate:.1f}% ({self.cpu_wins}/{self.games_played})"
        else:
            new_high = self.score >= self.high_score and self.score > 0
            high_msg = "🎉 NEW HIGH SCORE! 🎉" if new_high else ""
            msg = f"🏆 Game Over!\n\nFinal Score: {self.score}\n{high_msg}"
            stats = ""
        
        tk.Label(popup, text=msg,
                font=('Segoe UI', 14, 'bold'),
                fg=win_color if self.game_mode == 'multiplayer' else '#fbbf24', 
                bg='#1e293b', justify='center').pack(pady=20)
        
        if stats:
            tk.Label(popup, text=stats,
                    font=('Segoe UI', 12),
                    fg='#94a3b8', bg='#1e293b', justify='center').pack(pady=10)
        
        btn_yes = tk.Button(popup, text="Play Again",
                           font=('Segoe UI', 14, 'bold'),
                           bg='#22c55e', fg='white',
                           bd=0, cursor='hand2',
                           command=lambda: [popup.destroy(), overlay.destroy(),
                                            self.start_game(self.game_mode)])
        btn_yes.pack(pady=10)
        self.add_hover(btn_yes, 'single')
        
        btn_no = tk.Button(popup, text="Main Menu",
                          font=('Segoe UI', 14, 'bold'),
                          bg='#64748b', fg='white',
                          bd=0, cursor='hand2',
                          command=lambda: [popup.destroy(), overlay.destroy(),
                                           self.show_menu()])
        btn_no.pack(pady=10)
        self.add_hover(btn_no, 'settings')
    
    # ================= UTILITIES =================
    def confirm_exit(self):
        if messagebox.askokcancel("Exit", "Return to main menu?"):
            self.show_menu()
    
    def restart_game(self):
        if messagebox.askokcancel("New Game", "Start a new game?"):
            self.start_game(self.game_mode)
    
    def update_scores(self):
        for widget in self.score_frame.winfo_children():
            widget.destroy()
        
        if self.game_mode == 'multiplayer':
            tk.Label(self.score_frame,
                    text=f"👤 Human: {self.score}",
                    font=('Segoe UI', 16, 'bold'),
                    fg='#22c55e', bg='#1e293b').pack(side='left', padx=10)
            tk.Label(self.score_frame,
                    text="vs",
                    font=('Segoe UI', 14),
                    fg='#94a3b8', bg='#1e293b').pack(side='left', padx=5)
            tk.Label(self.score_frame,
                    text=f"🤖 CPU: {self.cpu_score}",
                    font=('Segoe UI', 16, 'bold'),
                    fg='#3b82f6', bg='#1e293b').pack(side='left', padx=10)
        else:
            tk.Label(self.score_frame,
                    text=f"🏆 Score: {self.score}",
                    font=('Segoe UI', 18, 'bold'),
                    fg='#fbbf24', bg='#1e293b').pack(side='left', padx=10)
            tk.Label(self.score_frame,
                    text=f"High: {self.high_score}",
                    font=('Segoe UI', 14),
                    fg='#94a3b8', bg='#1e293b').pack(side='left', padx=10)

# ================= MAIN =================
if __name__ == "__main__":
    root = tk.Tk()
    app = SameGameGUI(root)
    root.mainloop()
