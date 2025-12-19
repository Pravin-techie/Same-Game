import tkinter as tk
from tkinter import messagebox
import random

# ==========================================================
# SAME GAME - GUI VERSION WITH ADT & DSA
# ==========================================================

# Global variables
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
        """Create a random color grid"""
        return [[random.choice(COLORS) for _ in range(self.cols)]
                for _ in range(self.rows)]

# ==========================================================
# GRAPH ADT
# ==========================================================
class GraphADT:
    """Provides neighbors of a grid cell"""
    
    @staticmethod
    def neighbors(r, c):
        return [(r+1, c), (r-1, c), (r, c+1), (r, c-1)]

# ==========================================================
# SAME GAME GUI APPLICATION
# ==========================================================
class SameGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Same Game - ADT & DSA Edition")
        self.root.geometry("900x700")
        self.root.configure(bg='#1e293b')
        
        # Game state
        self.rows = 8
        self.cols = 8
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
    
    # ==========================================================
    # MENU SCREEN
    # ==========================================================
    def show_menu(self):
        self.clear_screen()
        
        menu_frame = tk.Frame(self.root, bg='#1e293b')
        menu_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Title
        title = tk.Label(
            menu_frame,
            text="✨ SAME GAME ✨",
            font=('Arial', 48, 'bold'),
            fg='#fbbf24',
            bg='#1e293b'
        )
        title.pack(pady=20)
        
        subtitle = tk.Label(
            menu_frame,
            text="Match & Remove Connected Blocks",
            font=('Arial', 16),
            fg='#94a3b8',
            bg='#1e293b'
        )
        subtitle.pack(pady=10)
        
        # Buttons
        btn_style = {
            'font': ('Arial', 16, 'bold'),
            'width': 20,
            'height': 2,
            'bd': 0,
            'cursor': 'hand2'
        }
        
        single_btn = tk.Button(
            menu_frame,
            text="👤 Single Player",
            bg='#22c55e',
            fg='white',
            command=lambda: self.start_game('single'),
            **btn_style
        )
        single_btn.pack(pady=10)
        
        multi_btn = tk.Button(
            menu_frame,
            text="🤖 vs CPU",
            bg='#3b82f6',
            fg='white',
            command=lambda: self.start_game('multiplayer'),
            **btn_style
        )
        multi_btn.pack(pady=10)
        
        settings_btn = tk.Button(
            menu_frame,
            text="⚙️ Board Size",
            bg='#64748b',
            fg='white',
            command=self.show_settings,
            **btn_style
        )
        settings_btn.pack(pady=10)
        
        rules_btn = tk.Button(
            menu_frame,
            text="📖 How to Play",
            bg='#64748b',
            fg='white',
            command=self.show_instructions,
            **btn_style
        )
        rules_btn.pack(pady=10)
        
        # Board size display
        size_label = tk.Label(
            menu_frame,
            text=f"Current Board: {self.rows} × {self.cols}",
            font=('Arial', 12),
            fg='#94a3b8',
            bg='#1e293b'
        )
        size_label.pack(pady=20)
    
    # ==========================================================
    # SETTINGS SCREEN
    # ==========================================================
    def show_settings(self):
        self.clear_screen()
        
        settings_frame = tk.Frame(self.root, bg='#1e293b')
        settings_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        title = tk.Label(
            settings_frame,
            text="⚙️ Board Size",
            font=('Arial', 36, 'bold'),
            fg='#fbbf24',
            bg='#1e293b'
        )
        title.pack(pady=20)
        
        sizes = [
            (6, 6, "Small (6×6)"),
            (8, 8, "Medium (8×8)"),
            (10, 10, "Large (10×10)"),
            (12, 8, "Wide (12×8)")
        ]
        
        for r, c, label in sizes:
            is_current = (self.rows == r and self.cols == c)
            btn = tk.Button(
                settings_frame,
                text=label,
                font=('Arial', 16, 'bold'),
                width=20,
                height=2,
                bg='#eab308' if is_current else '#475569',
                fg='white',
                bd=0,
                cursor='hand2',
                command=lambda r=r, c=c: self.set_board_size(r, c)
            )
            btn.pack(pady=5)
        
        back_btn = tk.Button(
            settings_frame,
            text="← Back",
            font=('Arial', 14),
            bg='#64748b',
            fg='white',
            bd=0,
            cursor='hand2',
            command=self.show_menu
        )
        back_btn.pack(pady=20)
    
    def set_board_size(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.show_menu()
    
    # ==========================================================
    # INSTRUCTIONS SCREEN
    # ==========================================================
    def show_instructions(self):
        self.clear_screen()
        
        inst_frame = tk.Frame(self.root, bg='#1e293b')
        inst_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        title = tk.Label(
            inst_frame,
            text="📖 How to Play",
            font=('Arial', 36, 'bold'),
            fg='#fbbf24',
            bg='#1e293b'
        )
        title.pack(pady=20)
        
        instructions = [
            "🎯 Click blocks to select connected same-color groups",
            "🎮 Minimum 2 blocks required to remove",
            "🏆 Score = (Blocks Removed)²",
            "⬇️ Gravity pulls remaining blocks down",
            "🤖 CPU uses Greedy Algorithm (largest group)",
            "🏁 Game ends when no valid moves remain"
        ]
        
        for inst in instructions:
            label = tk.Label(
                inst_frame,
                text=inst,
                font=('Arial', 14),
                fg='#e2e8f0',
                bg='#1e293b',
                justify='left'
            )
            label.pack(pady=5, anchor='w')
        
        back_btn = tk.Button(
            inst_frame,
            text="← Back to Menu",
            font=('Arial', 14, 'bold'),
            bg='#3b82f6',
            fg='white',
            width=20,
            height=2,
            bd=0,
            cursor='hand2',
            command=self.show_menu
        )
        back_btn.pack(pady=30)
    
    # ==========================================================
    # START GAME
    # ==========================================================
    def start_game(self, mode):
        self.game_mode = mode
        self.grid = GridADT(self.rows, self.cols)
        self.score = 0
        self.cpu_score = 0
        self.game_over = False
        self.selected_component = []
        self.show_game()
    
    # ==========================================================
    # GAME SCREEN
    # ==========================================================
    def show_game(self):
        self.clear_screen()
        
        # Main container
        game_frame = tk.Frame(self.root, bg='#1e293b')
        game_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header
        header = tk.Frame(game_frame, bg='#334155', height=80)
        header.pack(fill='x', pady=(0, 10))
        
        # Home button
        home_btn = tk.Button(
            header,
            text="🏠",
            font=('Arial', 20),
            bg='#475569',
            fg='white',
            bd=0,
            cursor='hand2',
            command=self.confirm_exit
        )
        home_btn.pack(side='left', padx=10, pady=10)
        
        title_label = tk.Label(
            header,
            text="SAME GAME",
            font=('Arial', 24, 'bold'),
            fg='white',
            bg='#334155'
        )
        title_label.pack(side='left', padx=10)
        
        # Score display
        score_frame = tk.Frame(header, bg='#334155')
        score_frame.pack(side='right', padx=10)
        
        if self.game_mode == 'multiplayer':
            tk.Label(
                score_frame,
                text=f"👤 Human: {self.score}",
                font=('Arial', 16, 'bold'),
                fg='#22c55e',
                bg='#334155'
            ).pack(side='left', padx=10)
            
            tk.Label(
                score_frame,
                text="vs",
                font=('Arial', 14),
                fg='#94a3b8',
                bg='#334155'
            ).pack(side='left', padx=5)
            
            tk.Label(
                score_frame,
                text=f"🤖 CPU: {self.cpu_score}",
                font=('Arial', 16, 'bold'),
                fg='#3b82f6',
                bg='#334155'
            ).pack(side='left', padx=10)
        else:
            tk.Label(
                score_frame,
                text=f"🏆 Score: {self.score}",
                font=('Arial', 18, 'bold'),
                fg='#fbbf24',
                bg='#334155'
            ).pack(padx=10)
        
        # Board container
        board_container = tk.Frame(game_frame, bg='#334155')
        board_container.pack(pady=10)
        
        # Create canvas for board
        canvas_width = self.cols * self.cell_size
        canvas_height = self.rows * self.cell_size
        
        self.canvas = tk.Canvas(
            board_container,
            width=canvas_width,
            height=canvas_height,
            bg='#1e293b',
            highlightthickness=0
        )
        self.canvas.pack(padx=20, pady=20)
        
        self.draw_board()
        
        # Info label
        self.info_label = tk.Label(
            game_frame,
            text="",
            font=('Arial', 14, 'bold'),
            fg='#fbbf24',
            bg='#1e293b'
        )
        self.info_label.pack(pady=10)
    
    # ==========================================================
    # DRAW BOARD
    # ==========================================================
    def draw_board(self):
        self.canvas.delete('all')
        self.cell_buttons = {}
        
        for r in range(self.rows):
            for c in range(self.cols):
                x1 = c * self.cell_size
                y1 = r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                cell = self.grid.board[r][c]
                
                if cell:
                    color = COLOR_MAP[cell]
                    
                    # Check if selected
                    is_selected = (r, c) in self.selected_component
                    
                    rect = self.canvas.create_rectangle(
                        x1 + 2, y1 + 2, x2 - 2, y2 - 2,
                        fill=color,
                        outline='white' if is_selected else color,
                        width=4 if is_selected else 1,
                        tags=f'cell_{r}_{c}'
                    )
                    
                    self.canvas.tag_bind(
                        f'cell_{r}_{c}',
                        '<Button-1>',
                        lambda e, r=r, c=c: self.handle_click(r, c)
                    )
                else:
                    self.canvas.create_rectangle(
                        x1 + 2, y1 + 2, x2 - 2, y2 - 2,
                        fill='#0f172a',
                        outline='#1e293b',
                        width=1
                    )
    
    # ==========================================================
    # DFS FOR CONNECTED COMPONENT
    # ==========================================================
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
        component = []
        color = self.grid.board[r][c]
        self.dfs(r, c, color, visited, component)
        return component
    
    # ==========================================================
    # HANDLE CLICK
    # ==========================================================
    def handle_click(self, r, c):
        if self.is_animating or self.game_over:
            return
        
        component = self.get_component(r, c)
        
        if len(component) < 2:
            self.info_label.config(text="❌ Invalid move! Need 2+ blocks")
            return
        
        self.selected_component = component
        points = len(component) ** 2
        self.info_label.config(
            text=f"✨ {len(component)} blocks = {points} points"
        )
        self.draw_board()
        
        # Remove after delay
        self.root.after(300, lambda: self.remove_component(component))
    
    # ==========================================================
    # REMOVE COMPONENT
    # ==========================================================
    def remove_component(self, component):
        self.is_animating = True
        
        # Remove blocks
        for r, c in component:
            self.grid.board[r][c] = None
        
        points = len(component) ** 2
        self.score += points
        
        self.selected_component = []
        self.draw_board()
        
        # Apply gravity
        self.root.after(200, self.apply_gravity)
    
    # ==========================================================
    # GRAVITY USING STACK
    # ==========================================================
    def apply_gravity(self):
        for c in range(self.cols):
            stack = []
            
            for r in range(self.rows):
                if self.grid.board[r][c]:
                    stack.append(self.grid.board[r][c])
            
            for r in range(self.rows - 1, -1, -1):
                self.grid.board[r][c] = stack.pop() if stack else None
        
        self.draw_board()
        self.is_animating = False
        self.info_label.config(text="")
        
        # Update score display
        self.show_game()
        
        if self.game_mode == 'multiplayer':
            self.root.after(500, self.cpu_turn)
        else:
            self.check_game_over()
    
    # ==========================================================
    # CPU TURN (GREEDY ALGORITHM)
    # ==========================================================
    def cpu_turn(self):
        if self.game_over:
            return
        
        self.is_animating = True
        best_component = []
        best_score = 0
        
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid.board[r][c]:
                    comp = self.get_component(r, c)
                    score = len(comp) ** 2
                    if score > best_score:
                        best_score = score
                        best_component = comp
        
        if len(best_component) > 1:
            self.selected_component = best_component
            self.draw_board()
            self.info_label.config(text="🤖 CPU is thinking...")
            
            self.root.after(800, lambda: self.cpu_remove(best_component))
        else:
            self.check_game_over()
    
    def cpu_remove(self, component):
        for r, c in component:
            self.grid.board[r][c] = None
        
        points = len(component) ** 2
        self.cpu_score += points
        
        self.selected_component = []
        self.draw_board()
        
        self.root.after(200, self.cpu_gravity)
    
    def cpu_gravity(self):
        for c in range(self.cols):
            stack = []
            
            for r in range(self.rows):
                if self.grid.board[r][c]:
                    stack.append(self.grid.board[r][c])
            
            for r in range(self.rows - 1, -1, -1):
                self.grid.board[r][c] = stack.pop() if stack else None
        
        self.draw_board()
        self.is_animating = False
        self.info_label.config(text="")
        self.show_game()
        self.check_game_over()
    
    # ==========================================================
    # CHECK GAME OVER
    # ==========================================================
    def check_game_over(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid.board[r][c]:
                    if len(self.get_component(r, c)) > 1:
                        return
        
        self.game_over = True
        self.show_game_over()
    
    # ==========================================================
    # GAME OVER DIALOG
    # ==========================================================
    def show_game_over(self):
        if self.game_mode == 'multiplayer':
            if self.score > self.cpu_score:
                winner = "🎉 Human Wins!"
            elif self.cpu_score > self.score:
                winner = "🤖 CPU Wins!"
            else:
                winner = "🤝 It's a Tie!"
            
            message = f"{winner}\n\nHuman: {self.score}\nCPU: {self.cpu_score}"
        else:
            message = f"🏆 Game Over!\n\nFinal Score: {self.score}"
        
        result = messagebox.askquestion(
            "Game Over",
            f"{message}\n\nPlay again?",
            icon='question'
        )
        
        if result == 'yes':
            self.start_game(self.game_mode)
        else:
            self.show_menu()
    
    # ==========================================================
    # UTILITIES
    # ==========================================================
    def confirm_exit(self):
        if messagebox.askokcancel("Exit", "Return to main menu?"):
            self.show_menu()
    
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# ==========================================================
# MAIN PROGRAM
# ==========================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = SameGameGUI(root)
    root.mainloop()