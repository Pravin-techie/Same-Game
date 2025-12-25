import tkinter as tk
from tkinter import messagebox
import random

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
# SAME GAME GUI
# ==========================================================
class SameGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Same Game - ADT & DSA Edition")
        self.root.geometry("1000x700")
        self.root.configure(bg='#1e293b')
        
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
        
        # Cell size
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
        
        tk.Label(frame, text="Match & Remove Connected Blocks", 
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
                 command=lambda: self.start_game('multiplayer'),
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
    
    # ================= SETTINGS =================
    def show_settings(self):
        self.clear_screen()
        
        frame = tk.Frame(self.root, bg='#1e293b')
        frame.place(relx=0.5, rely=0.5, anchor='center')
        
        tk.Label(frame, text="⚙️ Board Size", 
                font=('Arial', 36, 'bold'), 
                fg='#fbbf24', bg='#1e293b').pack(pady=20)
        
        # Removed the (12, 8) wide option
        sizes = [
            (6, 6, "Small (6×6)"),
            (8, 8, "Medium (8×8)"),
            (10, 10, "Large (10×10)")
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
            "⬇️ Gravity pulls remaining blocks down",
            "🤖 CPU uses Greedy Algorithm (largest group)",
            "🏁 Game ends when no valid moves remain"
        ]
        
        for inst in instructions:
            tk.Label(frame, text=inst,
                    font=('Arial', 14),
                    fg='#e2e8f0', bg='#1e293b',
                    justify='left').pack(pady=5, anchor='w')
        
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
        self.show_game()
    
    # ================= GAME SCREEN =================
    def show_game(self):
        self.clear_screen()
        
        self.game_frame = tk.Frame(self.root, bg='#1e293b')
        self.game_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header
        header = tk.Frame(self.game_frame, bg='#334155', height=80)
        header.pack(fill='x', pady=(0, 10))
        
        tk.Button(header, text="🏠",
                 font=('Arial', 20),
                 bg='#475569', fg='white',
                 bd=0, cursor='hand2',
                 command=self.confirm_exit).pack(side='left', padx=10, pady=10)
        
        tk.Label(header, text="SAME GAME",
                font=('Arial', 24, 'bold'),
                fg='white', bg='#334155').pack(side='left', padx=10)
        
        self.score_frame = tk.Frame(header, bg='#334155')
        self.score_frame.pack(side='right', padx=10)
        
        # Board
        self.board_container = tk.Frame(self.game_frame, bg='#334155')
        self.board_container.pack(pady=10)
        
        canvas_width = self.cols * self.cell_size
        canvas_height = self.rows * self.cell_size
        
        self.canvas = tk.Canvas(self.board_container,
                               width=canvas_width,
                               height=canvas_height,
                               bg='#1e293b',
                               highlightthickness=0)
        self.canvas.pack(padx=20, pady=20)
        
        self.info_label = tk.Label(self.game_frame,
                                   text="",
                                   font=('Arial', 14, 'bold'),
                                   fg='#fbbf24', bg='#1e293b')
        self.info_label.pack(pady=10)
        
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
                    
                    self.canvas.create_rectangle(
                        x1 + 2, y1 + 2, x2 - 2, y2 - 2,
                        fill=color,
                        outline='white' if is_selected else color,
                        width=4 if is_selected else 1,
                        tags=f'cell_{r}_{c}'
                    )
                    
                    self.canvas.tag_bind(f'cell_{r}_{c}', '<Button-1>',
                                        lambda e, r=r, c=c: self.handle_click(r, c))
                else:
                    self.canvas.create_rectangle(
                        x1 + 2, y1 + 2, x2 - 2, y2 - 2,
                        fill='#0f172a',
                        outline='#1e293b',
                        width=1
                    )
    
    # ================= DFS =================
    def dfs(self, r, c, color, visited, component):
        if r < 0 or r >= self.rows or c < 0 or c >= self.cols:
            return
        if (r, c) in visited:
            return
        if self.grid.board[r][c] != color:
            return
        
        visited.add((r, c))
        component.append((r, c))
        
        for nr, nc in GraphADT.neighbors(r, c):
            self.dfs(nr, nc, color, visited, component)
    
    def get_component(self, r, c):
        if not self.grid.board[r][c]:
            return []
        
        visited = set()
        comp = []
        self.dfs(r, c, self.grid.board[r][c], visited, comp)
        return comp
    
    # ================= HANDLE CLICK =================
    def handle_click(self, r, c):
        if self.is_animating or self.game_over:
            return
        
        comp = self.get_component(r, c)
        
        if len(comp) < 2:
            self.info_label.config(text="❌ Invalid move! Need 2+ blocks")
            return
        
        self.selected_component = comp
        points = len(comp) ** 2
        self.info_label.config(text=f"✨ {len(comp)} blocks = {points} points")
        self.draw_board()
        
        self.root.after(300, lambda: self.remove_component(comp))
    
    # ================= REMOVE COMPONENT =================
    def remove_component(self, comp):
        self.is_animating = True
        
        for r, c in comp:
            self.grid.board[r][c] = None
        
        self.score += len(comp) ** 2
        self.selected_component = []
        self.draw_board()
        
        self.root.after(200, self.apply_gravity)
    
    # ================= GRAVITY =================
    def apply_gravity(self):
        # Apply gravity using stack (same as base code)
        for c in range(self.cols):
            stack = []
            for r in range(self.rows):
                if self.grid.board[r][c]:
                    stack.append(self.grid.board[r][c])
            
            for r in range(self.rows - 1, -1, -1):
                self.grid.board[r][c] = stack.pop() if stack else None
        
        self.shift_left()
        self.draw_board()
        self.is_animating = False
        self.info_label.config(text="")
        self.update_scores()
        
        if self.game_mode == 'multiplayer':
            self.root.after(500, self.cpu_turn)
        else:
            self.check_game_over()
    
    # ================= SHIFT LEFT =================
    def shift_left(self):
        # Remove empty columns
        columns = [[self.grid.board[r][c] for r in range(self.rows)]
                   for c in range(self.cols)]
        
        columns = [col for col in columns if any(cell is not None for cell in col)]
        
        while len(columns) < self.cols:
            columns.append([None] * self.rows)
        
        for c in range(self.cols):
            for r in range(self.rows):
                self.grid.board[r][c] = columns[c][r]
    
    # ================= CPU TURN =================
    def cpu_turn(self):
        if self.game_over:
            return
        
        self.is_animating = True
        self.info_label.config(text="🤖 CPU is thinking...")
        
        # Find all valid components
        components = []
        visited_global = set()
        
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid.board[r][c] and (r, c) not in visited_global:
                    comp = self.get_component(r, c)
                    if len(comp) > 1:
                        components.append(comp)
                        visited_global.update(comp)
        
        if not components:
            self.check_game_over()
            return
        
        # Greedy: Choose largest component
        components.sort(key=lambda x: len(x), reverse=True)
        self.root.after(300, lambda: self.cpu_remove(components[0]))
    
    def cpu_remove(self, comp):
        for r, c in comp:
            self.grid.board[r][c] = None
        
        self.cpu_score += len(comp) ** 2
        self.selected_component = []
        self.draw_board()
        
        self.root.after(200, self.cpu_gravity)
    
    def cpu_gravity(self):
        # Apply gravity for CPU
        for c in range(self.cols):
            stack = []
            for r in range(self.rows):
                if self.grid.board[r][c]:
                    stack.append(self.grid.board[r][c])
            
            for r in range(self.rows - 1, -1, -1):
                self.grid.board[r][c] = stack.pop() if stack else None
        
        self.shift_left()
        self.draw_board()
        self.is_animating = False
        self.info_label.config(text="")
        self.update_scores()
        self.check_game_over()
    
    # ================= GAME OVER =================
    def check_game_over(self):
        # Check if any valid moves remain
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid.board[r][c] and len(self.get_component(r, c)) > 1:
                    return
        
        self.game_over = True
        self.show_game_over()
    
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

# ================= MAIN =================
if __name__ == "__main__":
    root = tk.Tk()
    app = SameGameGUI(root)
    root.mainloop()
