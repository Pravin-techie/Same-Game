==========================================================
SAME GAME – ADT & DSA BASED IMPLEMENTATION
Advanced Algorithmic Puzzle Game
==========================================================

Project Type : Data Structures & Algorithms Mini Project
Language     : Python
Interface    : GUI (Tkinter) + Console Version
Paradigm     : Abstract Data Types + Algorithmic Design

Team Members :
Pravin R
Vidhyadharan RP
Srijith S
Vijay Sathappan T


==========================================================
1. PROJECT DESCRIPTION
==========================================================

This project is an implementation of the classic puzzle
game "Same Game" using Data Structures and Algorithms.

The goal of the game is to remove connected groups of
same-colored blocks from a grid to maximize score.

The project demonstrates the practical use of several
advanced algorithmic techniques including:

• Graph Traversal (DFS)
• Greedy Algorithms
• Divide & Conquer
• Dynamic Programming
• Backtracking with Memoization
• Sorting Algorithms
• Abstract Data Types

The system includes two versions:

1. GUI Version (Tkinter based)
2. Console Based Version

Both versions implement the same core algorithms but
provide different interfaces.


==========================================================
2. GAME OBJECTIVE
==========================================================

The objective of Same Game is to maximize the score by
removing connected groups of blocks.

Rules:

1. Blocks must be connected horizontally or vertically
2. Minimum 2 blocks required for removal
3. Score Formula:

   Score = (Number of Blocks Removed)^2

4. After removal:
   - Blocks fall down due to gravity
   - Empty columns shift left

5. The game ends when no valid moves remain.


==========================================================
3. IMPLEMENTATION TYPES
==========================================================

----------------------------------
A. GUI VERSION (Tkinter)
----------------------------------

The GUI version provides a visual interface with:

• Interactive board
• Animated block removal
• Real-time score updates
• AI visualization system
• Algorithm comparison tools
• Adjustable board sizes

Game Modes:

• Single Player
• Human vs CPU
• AI Analysis Mode

Additional Features:

• Live algorithm visualization
• Step-by-step AI moves
• Adjustable analysis speed
• Algorithm benchmarking


----------------------------------
B. CONSOLE VERSION
----------------------------------

The console version focuses on demonstrating the
algorithmic strategies used in the game.

Features:

• Menu-driven interface
• Strategy selection
• Optimal hint system
• Benchmark testing
• CPU strategy switching


==========================================================
4. ABSTRACT DATA TYPES USED
==========================================================

1. Grid ADT
-----------

Implementation: 2D List

Represents the game board.

Example Board:

R G B Y
R R B Y
G G Y Y

Operations:

• Board creation
• Board copying
• Displaying board


----------------------------------------------------------

2. Graph ADT
------------

The grid is modeled as an implicit graph.

Each cell represents a node.

Edges exist between neighboring cells:

Up
Down
Left
Right

Used for connected component detection.


----------------------------------------------------------

3. Stack ADT
------------

Used in:

• Iterative DFS traversal
• Gravity simulation

Stack temporarily stores blocks during gravity.


----------------------------------------------------------

4. Set ADT
----------

Used to track visited nodes during DFS traversal.


----------------------------------------------------------

5. List ADT
-----------

Used for:

• Storing connected components
• Storing possible moves
• Tracking board states


----------------------------------------------------------

6. Dictionary ADT
-----------------

Used for memoization in:

• Dynamic Programming
• Backtracking algorithms

Stores previously evaluated board states.


==========================================================
5. ALGORITHMS IMPLEMENTED
==========================================================

The system implements three major AI strategies.


----------------------------------------------------------
5.1 GREEDY ALGORITHM (Easy AI)
----------------------------------------------------------

Idea:

Always remove the largest available block group.

Steps:

1. Find all connected components
2. Compute score for each component
3. Sort components using Merge Sort
4. Select the largest component

Complexity:

DFS: O(N × M)
Sorting: O(K log K)

Advantages:

• Very fast
• Simple implementation

Disadvantages:

• Only locally optimal
• May miss better long-term moves


----------------------------------------------------------
5.2 DIVIDE & CONQUER + DYNAMIC PROGRAMMING (Medium AI)
----------------------------------------------------------

This is the core algorithmic strategy used for the CPU.

The algorithm operates in three phases.

PHASE 1 – DIVIDE

The board is divided into independent column regions.
Columns separated by empty columns form separate regions.

PHASE 2 – CONQUER

Each region is evaluated using Dynamic Programming.

DP recursively evaluates future game states.

Score evaluation formula:

score = gain − opponent_future_score

Memoization stores previously computed states.

PHASE 3 – COMBINE

Best moves from each region are compared to select the
optimal move.

Advantages:

• Efficient state exploration
• Reduces computational complexity
• Produces near-optimal gameplay


----------------------------------------------------------
5.3 BACKTRACKING + MEMOIZATION (Hard AI)
----------------------------------------------------------

This strategy performs exhaustive search.

Steps:

1. Try every possible move
2. Recursively explore future states
3. Compute total achievable score
4. Use memoization to avoid recomputation

Formula:

Total Score = current_score + best_future_score

Advantages:

• Finds globally optimal solution

Disadvantages:

• Computationally expensive
• Slower on larger boards


==========================================================
6. GRAPH TRAVERSAL (DFS)
==========================================================

Depth First Search is used to detect connected
components.

Process:

1. Start from selected cell
2. Visit all same-colored neighbors
3. Continue recursively until component is complete

Time Complexity:

O(N × M)


==========================================================
7. GRAVITY ALGORITHM
==========================================================

After removing blocks, gravity is applied.

Vertical Gravity

Blocks fall downward to fill empty spaces.

Horizontal Shift

Empty columns shift to the left.


==========================================================
8. AI ANALYSIS SYSTEM (GUI)
==========================================================

The GUI version includes a real-time AI visualization
system.

Features:

• Live board visualization
• Highlighted AI moves
• Step-by-step algorithm execution
• Adjustable speed control

Displays:

• Move number
• Score updates
• Algorithm log
• Execution time


==========================================================
9. ALGORITHM COMPARISON SYSTEM
==========================================================

The program includes a benchmarking tool that compares
all algorithms.

Metrics measured:

• Final Score
• Number of Moves
• Execution Time

Example Output:

Strategy        Score    Moves    Time
Greedy          450      12       0.03s
DC + DP         520      11       0.45s
Backtracking    540      10       2.12s


==========================================================
10. GAME MODES
==========================================================

Single Player Mode

Player solves the board independently.

Final score displayed when the game ends.


----------------------------------------------------------

Multiplayer Mode (Human vs CPU)

Player competes against CPU.

CPU uses Divide & Conquer + Dynamic Programming.

Winner determined by final score.


----------------------------------------------------------

AI Analysis Mode (GUI)

Allows visualization of algorithms solving the board.

Algorithms available:

Easy   : Greedy
Medium : Divide & Conquer + DP
Hard   : Backtracking + Memoization


==========================================================
11. BOARD SIZE OPTIONS
==========================================================

Console Version

1. 5 x 5
2. 10 x 5
3. 15 x 10
4. 20 x 5

GUI Version

1. 6 x 6
2. 8 x 8
3. 10 x 10

Larger boards increase computational complexity.


==========================================================
12. HOW TO RUN THE PROGRAM
==========================================================

Run GUI Version

python same_game_gui.py

Requirements:

Python 3.x
Tkinter


----------------------------------------------------------

Run Console Version

python same_game_console.py

Follow the on-screen menu instructions.


==========================================================
13. INPUT FORMAT
==========================================================

Row and column inputs are zero-indexed.

Example:

Row: 2
Column: 3

Invalid moves (single blocks) are rejected.


==========================================================
14. OUTPUT
==========================================================

The program displays:

• Board state after each move
• Player and CPU scores
• CPU decision process
• Algorithm execution logs
• Final winner


==========================================================
15. KEY FEATURES
==========================================================

✔ ADT-based design
✔ Graph representation of board
✔ DFS traversal for connected components
✔ Stack-based gravity simulation
✔ Greedy algorithm implementation
✔ Divide & Conquer optimization
✔ Dynamic Programming with memoization
✔ Backtracking search strategy
✔ AI visualization system
✔ Algorithm benchmarking tools
✔ Interactive GUI with animations


==========================================================
16. LEARNING OUTCOMES
==========================================================

This project demonstrates practical applications of:

• Graph Theory
• Depth First Search
• Divide & Conquer algorithms
• Dynamic Programming
• Backtracking techniques
• Memoization
• Sorting algorithms
• Algorithm performance analysis


==========================================================
17. CONCLUSION
==========================================================

The Same Game project demonstrates how a simple puzzle
game can be transformed into a complex demonstration of
advanced Data Structures and Algorithms.

By integrating multiple algorithmic strategies including
Greedy, Divide & Conquer with Dynamic Programming, and
Backtracking, the system allows comparison between
different approaches to solving the same problem.

The inclusion of GUI visualization and benchmarking
further highlights the behavior and performance of
different algorithms.

This project successfully connects theoretical algorithm
design with practical implementation.


==========================================================
END OF README
==========================================================
