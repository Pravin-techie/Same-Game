==========================================================
SAME GAME – ADT & DSA BASED IMPLEMENTATION
==========================================================

Project Type   : Data Structures & Algorithms Mini Project
Language       : Python
Game Type      : Console Based Puzzle Game
Paradigm       : ADT + Algorithmic Design
Author         : Pravin R
==========================================================


----------------------------------------------------------
1. PROJECT DESCRIPTION
----------------------------------------------------------
This project is a console-based implementation of the
classic "Same Game" using Data Structures and Algorithms.

The objective of the game is to remove connected blocks
of the same color from a grid to score points. The game
ends when no more valid moves exist.

This implementation focuses on:
• Abstract Data Types (ADT)
• Graph Traversal (DFS)
• Stack usage
• Greedy Algorithm
• Game Logic Design


----------------------------------------------------------
2. GAME MODES
----------------------------------------------------------
1. Single Player Mode
   - Player plays alone
   - Final score displayed at the end

2. Multiplayer Mode (Human vs CPU)
   - Human and CPU play alternately
   - CPU uses a Greedy Algorithm
   - Winner is decided based on score


----------------------------------------------------------
3. DATA STRUCTURES USED (ADT)
----------------------------------------------------------

1. Grid ADT
   - Implemented using 2D List
   - Represents the game board

2. Graph ADT
   - Implicit Grid Graph
   - Each cell is a node
   - Neighbors: Up, Down, Left, Right

3. Stack ADT
   - Used in gravity simulation
   - Used indirectly in DFS recursion

4. Set ADT
   - Used to store visited nodes in DFS

5. List ADT
   - Stores connected components (clusters)

6. Greedy ADT
   - CPU selects the move with maximum score


----------------------------------------------------------
4. ALGORITHMS USED
----------------------------------------------------------

• Depth First Search (DFS)
  - Finds connected components of same color
  - Uses backtracking

• Greedy Algorithm
  - CPU chooses the move with maximum (blocks^2) score

• Gravity Algorithm
  - Blocks fall down after removal using stack logic


----------------------------------------------------------
5. GAME RULES
----------------------------------------------------------
1. Player selects a cell using row and column
2. Only connected blocks of the same color are removed
3. Minimum 2 connected blocks required for a valid move
4. Score Formula:
      Score = (Number of blocks removed)²
5. After removal, gravity is applied
6. Game ends when no valid moves remain


----------------------------------------------------------
6. BOARD SIZE OPTIONS
----------------------------------------------------------
The player can choose from the following board sizes:

1. 5 x 5
2. 10 x 5
3. 15 x 10
4. 20 x 5

Default size is 5 x 5 if an invalid choice is given.


----------------------------------------------------------
7. HOW TO RUN THE PROGRAM
----------------------------------------------------------
1. Ensure Python 3 is installed
2. Save the program file (example: same_game.py)
3. Open terminal or command prompt
4. Run the command:

   python same_game.py

5. Follow on-screen menu instructions


----------------------------------------------------------
8. INPUT FORMAT
----------------------------------------------------------
• Row and Column numbers are zero-indexed
• Example:
     Row: 2
     Column: 3

Invalid moves (single blocks) are rejected.


----------------------------------------------------------
9. OUTPUT DETAILS
----------------------------------------------------------
• Board displayed after every move
• Scores updated dynamically
• CPU move is automatically executed in multiplayer
• Final scores and winner displayed at game end


----------------------------------------------------------
10. KEY FEATURES
----------------------------------------------------------
✔ Menu Driven Interface
✔ Clean ADT-based Design
✔ Graph Traversal using DFS
✔ Stack-based Gravity Logic
✔ Greedy CPU Intelligence
✔ Fully Commented Code
✔ Beginner-friendly Implementation


----------------------------------------------------------
11. LIMITATIONS
----------------------------------------------------------
• Console-based interface only
• No diagonal connections
• No graphical UI
• CPU strategy is greedy (not optimal AI)


----------------------------------------------------------
12. FUTURE ENHANCEMENTS
----------------------------------------------------------
• GUI using Tkinter or Pygame
• Advanced AI using Minimax
• Time-based scoring
• Save & Load game state
• Color themes and animations


----------------------------------------------------------
13. CONCLUSION
----------------------------------------------------------
This project successfully demonstrates how real-world
games can be modeled using Data Structures and Algorithms.
It clearly shows the application of Graphs, DFS, Stack,
and Greedy techniques in an interactive manner.

----------------------------------------------------------
END OF README
----------------------------------------------------------
