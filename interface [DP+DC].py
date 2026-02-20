import tkinter as tk
from tkinter import messagebox
import time
import random
from functools import lru_cache
import math

# ==========================================================
# SAME GAME - PERFECT CPU STRATEGY
# Complete Implementation for Optimal Play
# ==========================================================

COLORS = ['R', 'G', 'B', 'Y']
COLOR_MAP = {
    'R': '#ef4444',  # Red
    'G': '#22c55e',  # Green
    'B': '#3b82f6',  # Blue
    'Y': '#eab308',  # Yellow
}

# ==========================================================
# OPTIMAL GRID ADT WITH HASHING
# ==========================================================
class OptimalGrid:
    __slots__ = ['rows', 'cols', 'board']
    
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.board = [[random.choice(COLORS) for _ in range(cols)]
                      for _ in range(rows)]
    
    def copy(self):
        new_grid = OptimalGrid(self.rows, self.cols)
        new_grid.board = [row[:] for row in self.board]
        return new_grid
    
    def get_state_key(self):
        """Fast hashable representation for memoization"""
        return tuple(tuple(row) for row in self.board)
    
    def is_empty(self):
        return all(cell is None for row in self.board for cell in row)
    
    def get_all_cells(self):
        """Get all non-empty cells with their positions"""
        cells = []
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c]:
                    cells.append((r, c, self.board[r][c]))
        return cells
    
    def get_column_blocks(self, col):
        """Get count of blocks in a column"""
        return sum(1 for r in range(self.rows) if self.board[r][c] for c in [col])

# ==========================================================
# COMPONENT DETECTION (FAST DFS)
# ==========================================================
class ComponentFinder:
    @staticmethod
    def get_component(grid, start_r, start_c):
        """Get connected component starting at position"""
        if not grid.board[start_r][start_c]:
            return []
        
        color = grid.board[start_r][start_c]
        rows, cols = grid.rows, grid.cols
        visited = set()
        stack = [(start_r, start_c)]
        component = []
        
        while stack:
            r, c = stack.pop()
            if (r, c) in visited:
                continue
            if r < 0 or r >= rows or c < 0 or c >= cols:
                continue
            if grid.board[r][c] != color:
                continue
            
            visited.add((r, c))
            component.append((r, c))
            
            # Add neighbors
            stack.append((r+1, c))
            stack.append((r-1, c))
            stack.append((r, c+1))
            stack.append((r, c-1))
        
        return component
    
    @staticmethod
    def get_all_components(grid):
        """Get all valid components (size >= 2)"""
        rows, cols = grid.rows, grid.cols
        visited = [[False] * cols for _ in range(rows)]
        components = []
        
        for r in range(rows):
            for c in range(cols):
                if grid.board[r][c] and not visited[r][c]:
                    # Get component using BFS/DFS
                    color = grid.board[r][c]
                    stack = [(r, c)]
                    comp = []
                    
                    while stack:
                        cr, cc = stack.pop()
                        if cr < 0 or cr >= rows or cc < 0 or cc >= cols:
                            continue
                        if visited[cr][cc] or grid.board[cr][cc] != color:
                            continue
                        
                        visited[cr][cc] = True
                        comp.append((cr, cc))
                        
                        stack.append((cr+1, cc))
                        stack.append((cr-1, cc))
                        stack.append((cr, cc+1))
                        stack.append((cr, cc-1))
                    
                    if len(comp) >= 2:
                        components.append(comp)
        
        return components

# ==========================================================
# PERFECT CPU STRATEGY - FIXED VERSION
# ==========================================================
class PerfectCPU:
    def __init__(self, difficulty="hard"):
        self.difficulty = difficulty
        self.memo = {}
        self.nodes_evaluated = 0
        self.max_depth = self._get_max_depth()
        self.time_limit = self._get_time_limit()
        
    def _get_max_depth(self):
        """Get search depth based on difficulty"""
        return {
            "easy": 4,
            "medium": 6,
            "hard": 10
        }.get(self.difficulty, 6)
    
    def _get_time_limit(self):
        """Time limit per move in seconds"""
        return {
            "easy": 0.5,
            "medium": 1.0,
            "hard": 2.0
        }.get(self.difficulty, 1.0)
    
    def divide_into_regions(self, grid):
        """
        Divide board into independent column regions
        Returns list of column ranges that are isolated by empty columns
        """
        regions = []
        current_region = []
        
        for c in range(grid.cols):
            # Check if column has any blocks
            has_blocks = any(grid.board[r][c] for r in range(grid.rows))
            
            if has_blocks:
                current_region.append(c)
            else:
                if current_region:
                    regions.append(current_region)
                    current_region = []
        
        if current_region:
            regions.append(current_region)
        
        return regions
    
    def evaluate_position(self, grid):
        """
        Advanced heuristic evaluation
        Returns score from CPU's perspective (higher is better for CPU)
        """
        if grid.is_empty():
            return 10000  # Win
        
        components = ComponentFinder.get_all_components(grid)
        if not components:
            return -10000  # Loss
        
        # Heuristic 1: Number of possible moves
        num_moves = len(components)
        
        # Heuristic 2: Average component size
        avg_size = sum(len(c) for c in components) / num_moves if num_moves > 0 else 0
        
        # Heuristic 3: Color distribution
        color_count = {'R': 0, 'G': 0, 'B': 0, 'Y': 0}
        for r in range(grid.rows):
            for c in range(grid.cols):
                if grid.board[r][c]:
                    color_count[grid.board[r][c]] += 1
        
        # Calculate color balance
        counts = [v for v in color_count.values() if v > 0]
        if len(counts) > 1:
            color_balance = -abs(max(counts) - min(counts)) / (grid.rows * grid.cols)
        else:
            color_balance = 0
        
        # Heuristic 4: Future potential
        empty_spaces = sum(1 for r in range(grid.rows) for c in range(grid.cols) 
                          if grid.board[r][c] is None)
        potential = empty_spaces / (grid.rows * grid.cols)
        
        # Heuristic 5: Clustering penalty
        clustering_penalty = -num_moves * 5
        
        # Heuristic 6: Large components bonus
        large_component_bonus = sum(len(c) ** 2 for c in components) / 10
        
        # Combined score
        score = (num_moves * 50) + (avg_size * 30) + (color_balance * 100) + (potential * 200) + clustering_penalty + large_component_bonus
        
        return score
    
    def apply_move(self, grid, component):
        """Apply a move and return new grid with gravity applied"""
        new_grid = grid.copy()
        
        # Remove component
        for r, c in component:
            new_grid.board[r][c] = None
        
        # Apply gravity and column shift
        self._apply_gravity(new_grid)
        
        return new_grid
    
    def _apply_gravity(self, grid):
        """Apply vertical gravity and horizontal column shift"""
        rows, cols = grid.rows, grid.cols
        
        # Vertical gravity
        for c in range(cols):
            # Collect non-empty cells from bottom to top
            column = []
            for r in range(rows-1, -1, -1):
                if grid.board[r][c]:
                    column.append(grid.board[r][c])
            
            # Fill from bottom
            for r in range(rows-1, -1, -1):
                if column:
                    grid.board[r][c] = column.pop(0)
                else:
                    grid.board[r][c] = None
        
        # Horizontal shift (move columns left)
        non_empty_cols = []
        for c in range(cols):
            if any(grid.board[r][c] for r in range(rows)):
                non_empty_cols.append(c)
        
        # Create new shifted board
        new_board = [[None] * cols for _ in range(rows)]
        for new_c, old_c in enumerate(non_empty_cols):
            for r in range(rows):
                new_board[r][new_c] = grid.board[r][old_c]
        
        grid.board = new_board
    
    def minimax(self, grid, depth, alpha, beta, is_cpu_turn, start_time):
        """
        Optimal minimax with alpha-beta pruning
        Returns (best_score, best_move)
        """
        self.nodes_evaluated += 1
        
        # Time limit check
        if time.time() - start_time > self.time_limit:
            return self.evaluate_position(grid), None
        
        # Check memoization cache
        state_key = (grid.get_state_key(), depth, is_cpu_turn)
        if state_key in self.memo:
            return self.memo[state_key]
        
        # Get all possible moves
        components = ComponentFinder.get_all_components(grid)
        
        # Terminal node
        if depth == 0 or not components:
            score = self.evaluate_position(grid)
            self.memo[state_key] = (score, None)
            return score, None
        
        if is_cpu_turn:  # Maximizing player (CPU)
            max_score = float('-inf')
            best_move = None
            
            # Sort moves for better pruning (largest components first)
            components.sort(key=len, reverse=True)
            
            for comp in components:
                # Apply move
                new_grid = self.apply_move(grid, comp)
                
                # Immediate gain
                immediate_gain = len(comp) ** 2
                
                # Recurse
                score, _ = self.minimax(new_grid, depth - 1, alpha, beta, False, start_time)
                total_score = immediate_gain + score
                
                if total_score > max_score:
                    max_score = total_score
                    best_move = comp
                
                alpha = max(alpha, total_score)
                if beta <= alpha:
                    break  # Beta cutoff
            
            self.memo[state_key] = (max_score, best_move)
            return max_score, best_move
        
        else:  # Minimizing player (Human)
            min_score = float('inf')
            best_move = None
            
            # Sort moves for better pruning
            components.sort(key=len, reverse=True)
            
            for comp in components:
                # Apply move
                new_grid = self.apply_move(grid, comp)
                
                # Human gain is negative for CPU
                human_gain = len(comp) ** 2
                
                # Recurse
                score, _ = self.minimax(new_grid, depth - 1, alpha, beta, True, start_time)
                total_score = score - human_gain  # Subtract human's gain
                
                if total_score < min_score:
                    min_score = total_score
                    best_move = comp
                
                beta = min(beta, total_score)
                if beta <= alpha:
                    break  # Alpha cutoff
            
            self.memo[state_key] = (min_score, best_move)
            return min_score, best_move
    
    def get_best_move(self, grid):
        """
        MAIN ALGORITHM - FIXED VERSION
        Prioritizes larger components while still considering strategy
        """
        start_time = time.time()
        self.nodes_evaluated = 0
        self.memo.clear()
        
        # Get all components
        all_components = ComponentFinder.get_all_components(grid)
        
        if not all_components:
            return None
        
        # Sort components by size (largest first) for initial consideration
        all_components.sort(key=len, reverse=True)
        
        # If board is small, use full minimax
        total_cells = grid.rows * grid.cols
        if total_cells <= 36:  # 6x6 or smaller
            depth = min(self.max_depth, 8)
            _, best_move = self.minimax(grid, depth, float('-inf'), float('inf'), True, start_time)
            return best_move
        
        # DIVIDE PHASE - Get regions
        regions = self.divide_into_regions(grid)
        
        # CONQUER PHASE - Evaluate top moves from each region
        candidate_moves = []
        
        # Consider top components by size (at least top 5 or all if less)
        top_components = all_components[:min(5, len(all_components))]
        
        for comp in top_components:
            # Calculate immediate gain
            immediate_gain = len(comp) ** 2
            
            # Quick future evaluation with limited depth
            new_grid = self.apply_move(grid, comp)
            future_components = ComponentFinder.get_all_components(new_grid)
            
            if future_components:
                # Look at best possible future move
                best_future = max(len(fc) for fc in future_components)
                future_potential = best_future ** 2 * 0.5  # Weight future less than immediate
            else:
                future_potential = 1000  # Winning move bonus
            
            # Also consider if this move creates good opportunities
            # Check if it creates a larger component after gravity
            strategic_bonus = 0
            for fc in future_components[:min(3, len(future_components))]:
                if len(fc) >= len(comp):  # Future component is as large or larger
                    strategic_bonus += len(fc) ** 2 * 0.3
            
            # Total score with heavy weight on immediate gain
            total_score = (immediate_gain * 2.0) + future_potential + strategic_bonus
            
            candidate_moves.append((comp, total_score))
        
        # Also check region-based moves for completeness
        for region_cols in regions:
            region_components = [comp for comp in all_components 
                               if all(c in region_cols for _, c in comp)]
            
            if region_components:
                # Take the largest component from this region
                best_in_region = max(region_components, key=len)
                
                # Check if we already have it
                if not any(best_in_region == cm[0] for cm in candidate_moves):
                    immediate_gain = len(best_in_region) ** 2
                    new_grid = self.apply_move(grid, best_in_region)
                    future_components = ComponentFinder.get_all_components(new_grid)
                    
                    if future_components:
                        best_future = max(len(fc) for fc in future_components)
                        future_potential = best_future ** 2 * 0.5
                    else:
                        future_potential = 1000
                    
                    total_score = (immediate_gain * 2.0) + future_potential
                    candidate_moves.append((best_in_region, total_score))
        
        # Sort by total score and pick the best
        if candidate_moves:
            candidate_moves.sort(key=lambda x: x[1], reverse=True)
            best_move = candidate_moves[0][0]
            
            # Debug info (can be removed)
            print(f"Selected move: {len(best_move)} blocks, score: {candidate_moves[0][1]:.2f}")
            if len(candidate_moves) > 1:
                print(f"Runner up: {len(candidate_moves[1][0])} blocks, score: {candidate_moves[1][1]:.2f}")
            
            return best_move
        
        # Ultimate fallback - just take the largest component
        return max(all_components, key=len)
    
    def _greedy_move(self, grid):
        """Greedy fallback (largest component)"""
        components = ComponentFinder.get_all_components(grid)
        if not components:
            return None
        return max(components, key=len)

# ==========================================================
# SAME GAME GUI WITH OPTIMAL CPU
# ==========================================================
class SameGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Same Game")
        self.root.geometry("1000x700")
        self.root.configure(bg='#0f172a')
        
        # Game state
        self.rows = 6
        self.cols = 6
        self.grid = None
        self.score = 0
        self.cpu_score = 0
        self.game_mode = None
        self.selected_component = []
        self.is_animating = False
        self.game_over = False
        
        # CPU player
        self.cpu = PerfectCPU(difficulty="hard")
        
        # Cell size
        self.cell_size = 60
        
        # Bind window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.show_menu()
    
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
    
    # ================= MENU =================
    def show_menu(self):
        self.clear_screen()
        
        # Main frame
        main_frame = tk.Frame(self.root, bg='#0f172a')
        main_frame.pack(expand=True, fill='both')
        
        # Center content
        center = tk.Frame(main_frame, bg='#0f172a')
        center.place(relx=0.5, rely=0.5, anchor='center')
        
        # Title
        title_frame = tk.Frame(center, bg='#0f172a')
        title_frame.pack(pady=20)
        
        tk.Label(title_frame, text="🎮", font=('Arial', 60), 
                fg='#fbbf24', bg='#0f172a').pack(side='left')
        
        tk.Label(title_frame, text="SAME GAME", font=('Arial', 48, 'bold'), 
                fg='#fbbf24', bg='#0f172a').pack(side='left')
        
        tk.Label(title_frame, text="🎮", font=('Arial', 60), 
                fg='#fbbf24', bg='#0f172a').pack(side='left')
        
        # Subtitle
        tk.Label(center, text="Classic Puzzle Game", font=('Arial', 18, 'bold'), 
                fg='#94a3b8', bg='#0f172a').pack(pady=10)
        
        # Buttons
        btn_frame = tk.Frame(center, bg='#0f172a')
        btn_frame.pack(pady=40)
        
        # Single Player
        single_btn = tk.Button(btn_frame, text="👤 SINGLE PLAYER", 
                              font=('Arial', 16, 'bold'),
                              bg='#22c55e', fg='white',
                              width=20, height=2,
                              bd=0, cursor='hand2',
                              command=lambda: self.start_game('single'))
        single_btn.pack(pady=10)
        self.add_hover_effect(single_btn, '#16a34a', '#22c55e')
        
        # VS CPU
        vs_btn = tk.Button(btn_frame, text="🤖 VS CPU", 
                          font=('Arial', 16, 'bold'),
                          bg='#3b82f6', fg='white',
                          width=20, height=2,
                          bd=0, cursor='hand2',
                          command=lambda: self.start_game('multiplayer'))
        vs_btn.pack(pady=10)
        self.add_hover_effect(vs_btn, '#2563eb', '#3b82f6')
        
        # Settings
        settings_btn = tk.Button(btn_frame, text="⚙️ SETTINGS", 
                                font=('Arial', 16, 'bold'),
                                bg='#64748b', fg='white',
                                width=20, height=2,
                                bd=0, cursor='hand2',
                                command=self.show_settings)
        settings_btn.pack(pady=10)
        self.add_hover_effect(settings_btn, '#475569', '#64748b')
        
        # Info
        tk.Label(center, text=f"Current Board: {self.rows} × {self.cols}", 
                font=('Arial', 12), fg='#94a3b8', bg='#0f172a').pack(pady=20)
    
    def add_hover_effect(self, button, hover_color, normal_color):
        def on_enter(e):
            button.config(bg=hover_color)
        def on_leave(e):
            button.config(bg=normal_color)
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    
    # ================= SETTINGS =================
    def show_settings(self):
        self.clear_screen()
        
        frame = tk.Frame(self.root, bg='#0f172a')
        frame.place(relx=0.5, rely=0.5, anchor='center')
        
        tk.Label(frame, text="⚙️ SETTINGS", font=('Arial', 36, 'bold'), 
                fg='#fbbf24', bg='#0f172a').pack(pady=20)
        
        # Board Size
        tk.Label(frame, text="BOARD SIZE:", font=('Arial', 14, 'bold'), 
                fg='white', bg='#0f172a').pack(pady=10)
        
        size_frame = tk.Frame(frame, bg='#0f172a')
        size_frame.pack(pady=10)
        
        sizes = [(6, 6, "6×6"), (8, 8, "8×8"), (10, 10, "10×10")]
        for r, c, label in sizes:
            btn = tk.Button(size_frame, text=label,
                          font=('Arial', 14),
                          bg='#eab308' if (self.rows == r and self.cols == c) else '#334155',
                          fg='white', width=8, height=1,
                          bd=0, cursor='hand2',
                          command=lambda r=r, c=c: self.set_board_size(r, c))
            btn.pack(side='left', padx=5)
            self.add_hover_effect(btn, '#ca8a04', '#eab308' if (self.rows == r and self.cols == c) else '#334155')
        
        # CPU Difficulty
        tk.Label(frame, text="\nCPU DIFFICULTY:", font=('Arial', 14, 'bold'), 
                fg='white', bg='#0f172a').pack(pady=10)
        
        diff_frame = tk.Frame(frame, bg='#0f172a')
        diff_frame.pack(pady=10)
        
        difficulties = [("easy", "😊 EASY"), ("medium", "😐 MEDIUM"), ("hard", "😈 HARD")]
        for diff, label in difficulties:
            btn = tk.Button(diff_frame, text=label,
                          font=('Arial', 14),
                          bg='#eab308' if self.cpu.difficulty == diff else '#334155',
                          fg='white', width=10, height=1,
                          bd=0, cursor='hand2',
                          command=lambda d=diff: self.set_difficulty(d))
            btn.pack(side='left', padx=5)
            self.add_hover_effect(btn, '#ca8a04', '#eab308' if self.cpu.difficulty == diff else '#334155')
        
        # Back button
        back_btn = tk.Button(frame, text="← BACK TO MENU",
                           font=('Arial', 14, 'bold'),
                           bg='#64748b', fg='white',
                           width=20, height=2,
                           bd=0, cursor='hand2',
                           command=self.show_menu)
        back_btn.pack(pady=40)
        self.add_hover_effect(back_btn, '#475569', '#64748b')
    
    def set_board_size(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.show_settings()
    
    def set_difficulty(self, difficulty):
        self.cpu = PerfectCPU(difficulty=difficulty)
        self.show_settings()
    
    # ================= START GAME =================
    def start_game(self, mode):
        self.game_mode = mode
        self.grid = OptimalGrid(self.rows, self.cols)
        self.score = 0
        self.cpu_score = 0
        self.game_over = False
        self.selected_component = []
        self.show_game()
    
    # ================= GAME SCREEN =================
    def show_game(self):
        self.clear_screen()
        
        # Main game frame
        self.game_frame = tk.Frame(self.root, bg='#0f172a')
        self.game_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header
        header = tk.Frame(self.game_frame, bg='#1e293b', height=80)
        header.pack(fill='x', pady=(0, 20))
        
        # Menu button
        menu_btn = tk.Button(header, text="🏠", font=('Arial', 20),
                           bg='#334155', fg='white',
                           bd=0, cursor='hand2',
                           command=self.confirm_exit)
        menu_btn.pack(side='left', padx=10, pady=10)
        self.add_hover_effect(menu_btn, '#475569', '#334155')
        
        # Title
        tk.Label(header, text="SAME GAME", font=('Arial', 24, 'bold'),
                fg='white', bg='#1e293b').pack(side='left', padx=10)
        
        # Score display
        self.score_frame = tk.Frame(header, bg='#1e293b')
        self.score_frame.pack(side='right', padx=20)
        self.update_scores()
        
        # Hint button for multiplayer
        if self.game_mode == 'multiplayer':
            hint_btn = tk.Button(header, text="💡 HINT", 
                                font=('Arial', 14, 'bold'),
                                bg='#eab308', fg='black',
                                bd=0, cursor='hand2',
                                command=self.show_hint)
            hint_btn.pack(side='right', padx=10)
            self.add_hover_effect(hint_btn, '#ca8a04', '#eab308')
        
        # Board container
        board_container = tk.Frame(self.game_frame, bg='#1e293b', padx=20, pady=20)
        board_container.pack(expand=True)
        
        # Canvas for board
        canvas_width = self.cols * self.cell_size
        canvas_height = self.rows * self.cell_size
        
        self.canvas = tk.Canvas(board_container,
                               width=canvas_width,
                               height=canvas_height,
                               bg='#0f172a',
                               highlightthickness=2,
                               highlightbackground='#334155')
        self.canvas.pack()
        
        # Info label
        self.info_label = tk.Label(self.game_frame, text="",
                                   font=('Arial', 14, 'bold'),
                                   fg='#fbbf24', bg='#0f172a')
        self.info_label.pack(pady=10)
        
        self.draw_board()
    
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
                    
                    # Draw cell with 3D effect
                    self.canvas.create_rectangle(
                        x1 + 2, y1 + 2, x2 - 2, y2 - 2,
                        fill=color,
                        outline='white' if is_selected else '#334155',
                        width=3 if is_selected else 1,
                        tags=f'cell_{r}_{c}'
                    )
                    
                    # Add text
                    self.canvas.create_text(
                        x1 + self.cell_size//2,
                        y1 + self.cell_size//2,
                        text=cell,
                        fill='white',
                        font=('Arial', 18, 'bold'),
                        tags=f'text_{r}_{c}'
                    )
                    
                    # Bind click events
                    self.canvas.tag_bind(f'cell_{r}_{c}', '<Button-1>',
                                        lambda e, r=r, c=c: self.handle_click(r, c))
                    self.canvas.tag_bind(f'text_{r}_{c}', '<Button-1>',
                                        lambda e, r=r, c=c: self.handle_click(r, c))
                else:
                    # Empty cell
                    self.canvas.create_rectangle(
                        x1 + 2, y1 + 2, x2 - 2, y2 - 2,
                        fill='#1e293b',
                        outline='#334155',
                        width=1
                    )
    
    # ================= GAME MECHANICS =================
    def handle_click(self, r, c):
        if self.is_animating or self.game_over:
            return
        
        comp = ComponentFinder.get_component(self.grid, r, c)
        
        if len(comp) < 2:
            self.info_label.config(text="❌ Need at least 2 blocks!")
            return
        
        self.selected_component = comp
        points = len(comp) ** 2
        self.info_label.config(text=f"✨ {len(comp)} blocks = {points} points")
        self.draw_board()
        
        self.root.after(300, lambda: self.remove_component(comp))
    
    def remove_component(self, comp):
        self.is_animating = True
        
        # Remove blocks
        for r, c in comp:
            self.grid.board[r][c] = None
        
        self.score += len(comp) ** 2
        self.selected_component = []
        self.draw_board()
        
        self.root.after(200, self.apply_gravity)
    
    def apply_gravity(self):
        """Apply gravity and shift columns"""
        self.cpu._apply_gravity(self.grid)
        self.draw_board()
        self.is_animating = False
        self.info_label.config(text="")
        self.update_scores()
        
        if self.game_mode == 'multiplayer':
            self.root.after(500, self.cpu_turn)
        else:
            self.check_game_over()
    
    # ================= CPU TURN =================
    def cpu_turn(self):
        if self.game_over:
            return
        
        self.is_animating = True
        self.info_label.config(text="🤖 CPU is thinking...")
        self.root.update()
        
        # Get best move from CPU
        best_move = self.cpu.get_best_move(self.grid)
        
        if not best_move:
            self.check_game_over()
            return
        
        self.root.after(500, lambda: self.cpu_remove(best_move))
    
    def cpu_remove(self, comp):
        for r, c in comp:
            self.grid.board[r][c] = None
        
        self.cpu_score += len(comp) ** 2
        self.selected_component = []
        self.draw_board()
        
        self.root.after(200, self.cpu_gravity)
    
    def cpu_gravity(self):
        self.cpu._apply_gravity(self.grid)
        self.draw_board()
        self.is_animating = False
        self.info_label.config(text="")
        self.update_scores()
        self.check_game_over()
    
    # ================= HINT =================
    def show_hint(self):
        """Show optimal move for human player"""
        if self.is_animating or self.game_over:
            return
        
        self.info_label.config(text="💡 Calculating hint...")
        self.root.update()
        
        # Use CPU's algorithm for hint
        hint_cpu = PerfectCPU(difficulty="medium")
        best_move = hint_cpu.get_best_move(self.grid)
        
        if best_move and len(best_move) > 0:
            r, c = best_move[0]
            points = len(best_move) ** 2
            self.info_label.config(text=f"💡 Hint: Try ({r+1}, {c+1}) for {points} points!")
            
            # Highlight hint
            x1 = c * self.cell_size + self.cell_size // 2
            y1 = r * self.cell_size + self.cell_size // 2
            
            hint_id = self.canvas.create_oval(
                x1 - 25, y1 - 25, x1 + 25, y1 + 25,
                outline='#fbbf24', width=3, tags='hint'
            )
            self.root.after(2000, lambda: self.canvas.delete(hint_id))
        else:
            self.info_label.config(text="❌ No valid moves!")
    
    # ================= GAME OVER =================
    def check_game_over(self):
        components = ComponentFinder.get_all_components(self.grid)
        if not components:
            self.game_over = True
            self.show_game_over()
    
    def show_game_over(self):
        if self.game_mode == 'multiplayer':
            if self.score > self.cpu_score:
                winner = "🎉 YOU WIN!"
                winner_color = "#22c55e"
                msg = f"Congratulations! Great strategy!"
            elif self.cpu_score > self.score:
                winner = "🤖 CPU WINS!"
                winner_color = "#ef4444"
                msg = f"The CPU played better this time!"
            else:
                winner = "🤝 IT'S A TIE!"
                winner_color = "#eab308"
                msg = f"A close game!"
            
            final_msg = f"{winner}\n\n👤 You: {self.score}\n🤖 CPU: {self.cpu_score}\n\n{msg}"
        else:
            final_msg = f"🏆 GAME OVER!\n\nFinal Score: {self.score}"
            winner_color = "#fbbf24"
        
        # Create game over dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Game Over")
        dialog.geometry("450x400")
        dialog.configure(bg='#0f172a')
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (dialog.winfo_screenheight() // 2) - (400 // 2)
        dialog.geometry(f'+{x}+{y}')
        
        # Content
        tk.Label(dialog, text="GAME OVER", 
                font=('Arial', 32, 'bold'),
                fg=winner_color, bg='#0f172a').pack(pady=20)
        
        tk.Label(dialog, text=final_msg,
                font=('Arial', 16),
                fg='white', bg='#0f172a',
                justify='center').pack(pady=20)
        
        # Buttons
        btn_frame = tk.Frame(dialog, bg='#0f172a')
        btn_frame.pack(pady=20)
        
        play_again = tk.Button(btn_frame, text="🔄 PLAY AGAIN",
                              font=('Arial', 14, 'bold'),
                              bg='#22c55e', fg='white',
                              width=12, height=2,
                              bd=0, cursor='hand2',
                              command=lambda: [dialog.destroy(), 
                                             self.start_game(self.game_mode)])
        play_again.pack(side='left', padx=5)
        self.add_hover_effect(play_again, '#16a34a', '#22c55e')
        
        menu_btn = tk.Button(btn_frame, text="🏠 MENU",
                            font=('Arial', 14, 'bold'),
                            bg='#3b82f6', fg='white',
                            width=12, height=2,
                            bd=0, cursor='hand2',
                            command=lambda: [dialog.destroy(), 
                                           self.show_menu()])
        menu_btn.pack(side='left', padx=5)
        self.add_hover_effect(menu_btn, '#2563eb', '#3b82f6')
    
    # ================= UTILITIES =================
    def confirm_exit(self):
        if messagebox.askokcancel("Exit", "Return to main menu?"):
            self.show_menu()
    
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def update_scores(self):
        for widget in self.score_frame.winfo_children():
            widget.destroy()
        
        if self.game_mode == 'multiplayer':
            # Player score
            player_frame = tk.Frame(self.score_frame, bg='#1e293b')
            player_frame.pack(side='left', padx=10)
            
            tk.Label(player_frame, text="👤 YOU", 
                    font=('Arial', 12), fg='#94a3b8', bg='#1e293b').pack()
            tk.Label(player_frame, text=str(self.score),
                    font=('Arial', 20, 'bold'), fg='#22c55e', bg='#1e293b').pack()
            
            # VS
            tk.Label(self.score_frame, text="VS",
                    font=('Arial', 14, 'bold'), fg='#fbbf24', bg='#1e293b').pack(side='left', padx=10)
            
            # CPU score
            cpu_frame = tk.Frame(self.score_frame, bg='#1e293b')
            cpu_frame.pack(side='left', padx=10)
            
            difficulty_emoji = {
                "easy": "😊",
                "medium": "😐",
                "hard": "😈"
            }.get(self.cpu.difficulty, "🤖")
            
            tk.Label(cpu_frame, text=f"{difficulty_emoji} CPU", 
                    font=('Arial', 12), fg='#94a3b8', bg='#1e293b').pack()
            tk.Label(cpu_frame, text=str(self.cpu_score),
                    font=('Arial', 20, 'bold'), fg='#ef4444', bg='#1e293b').pack()
        else:
            tk.Label(self.score_frame, text=f"🏆 {self.score}",
                    font=('Arial', 24, 'bold'), fg='#fbbf24', bg='#1e293b').pack()

# ================= MAIN =================
if __name__ == "__main__":
    root = tk.Tk()
    app = SameGameGUI(root)
    root.mainloop()
