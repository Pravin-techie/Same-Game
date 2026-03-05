===============================================================================
                     SAME GAME – ADT & DSA BASED IMPLEMENTATION
                         Advanced Algorithmic Puzzle Game
===============================================================================

Project Type   : Data Structures & Algorithms Mini Project
Language       : Python
Interface      : GUI (Tkinter) + Console Version
Paradigm       : Abstract Data Types + Algorithmic Design

Team Members   :
    • Pravin R
    • Vidhyadharan RP
    • Srijith S
    • Vijay Sathappan T


===============================================================================
1. PROJECT DESCRIPTION
===============================================================================

This project is an implementation of the classic puzzle game "Same Game"
developed using Data Structures and Algorithms.

The objective of the game is to remove connected groups of same-colored
blocks from a grid to maximize the score.

This project demonstrates the application of several advanced algorithmic
techniques such as:

    • Graph Traversal (DFS)
    • Greedy Algorithms
    • Divide & Conquer
    • Dynamic Programming
    • Backtracking with Memoization
    • Sorting Algorithms
    • Abstract Data Types (ADT)

The system contains two implementations:

    1. GUI Version (Tkinter Interface)
    2. Console-Based Version

Both versions share the same core algorithms but provide different
interaction styles.


===============================================================================
2. GAME OBJECTIVE
===============================================================================

The goal of Same Game is to maximize the score by removing connected groups
of blocks from the board.

GAME RULES

    1. Blocks must be connected vertically or horizontally.
    2. Minimum 2 blocks are required to remove a group.
    3. Score Formula:

            Score = (Number of Blocks Removed)^2

    4. After removal:
            • Blocks fall downward due to gravity
            • Empty columns shift to the left

    5. The game ends when no valid moves remain.


===============================================================================
3. IMPLEMENTATION TYPES
===============================================================================

A) GUI VERSION (Tkinter)
-------------------------------------------------------------------------------

The GUI version provides a professional interactive interface with:

    • Visual board display
    • Animated block removal
    • Real-time score updates
    • AI visualization system
    • Algorithm comparison tools
    • Adjustable board sizes

Game Modes:

    • Single Player Mode
    • Human vs CPU Mode
    • AI Analysis Mode

Additional Features:

    • Real-time AI move visualization
    • Algorithm benchmarking
    • Adjustable AI speed


B) CONSOLE VERSION
-------------------------------------------------------------------------------

The console version focuses on demonstrating algorithmic behavior.

Features include:

    • Menu-driven interface
    • CPU strategy selection
    • Optimal hint system
    • Strategy benchmarking
    • Multiplayer gameplay


===============================================================================
4. ABSTRACT DATA TYPES USED
===============================================================================

1. GRID ADT
-------------------------------------------------------------------------------

Implementation : 2D List

Represents the game board.

Example Board:

        R  G  B  Y
        R  R  B  Y
        G  G  Y  Y

Operations Supported:

    • Board creation
    • Board copying
    • Board display


2. GRAPH ADT
-------------------------------------------------------------------------------

The board is modeled as an implicit graph.

Each cell is treated as a node.

Edges exist between adjacent cells:

        Up
        Down
        Left
        Right

Used for:

    • DFS traversal
    • Connected component detection


3. STACK ADT
-------------------------------------------------------------------------------

Used in:

    • Iterative DFS traversal
    • Gravity simulation

The stack temporarily stores blocks during gravity processing.


4. SET ADT
-------------------------------------------------------------------------------

Used to store visited nodes during DFS traversal to avoid repeated visits.


5. LIST ADT
-------------------------------------------------------------------------------

Used for:

    • Storing connected components
    • Tracking possible moves
    • Managing board states


6. DICTIONARY ADT
-------------------------------------------------------------------------------

Used for memoization in:

    • Dynamic Programming
    • Backtracking algorithms

Stores previously evaluated board states.


===============================================================================
5. ALGORITHMS IMPLEMENTED
===============================================================================

Three major AI strategies are implemented.


5.1 GREEDY ALGORITHM (Easy AI)
-------------------------------------------------------------------------------

Idea:

    Always remove the largest available block group.

Steps:

    1. Find all connected components using DFS
    2. Calculate score of each component
    3. Sort components using Merge Sort
    4. Select the largest component

Time Complexity:

        DFS        : O(N × M)
        Merge Sort : O(K log K)

Advantages:

    • Very fast
    • Simple implementation

Disadvantages:

    • Only locally optimal
    • May miss better long-term moves


5.2 DIVIDE & CONQUER + DYNAMIC PROGRAMMING (Medium AI)
-------------------------------------------------------------------------------

This is the main algorithm used by the CPU opponent.

The process consists of three phases.


PHASE 1 – DIVIDE

    The board is divided into independent column regions.
    Empty columns naturally separate independent sections.


PHASE 2 – CONQUER

    Each region is evaluated using Dynamic Programming.

    Recursive evaluation explores future game states.

    Score formula:

        score = gain − opponent_future_score

    Memoization avoids recomputation of board states.


PHASE 3 – COMBINE

    Best results from each region are compared to determine
    the optimal move.

Advantages:

    • Efficient search space reduction
    • Near-optimal decision making


5.3 BACKTRACKING + MEMOIZATION (Hard AI)
-------------------------------------------------------------------------------

This strategy performs exhaustive search.

Steps:

    1. Try every possible move
    2. Recursively evaluate future states
    3. Compute total achievable score
    4. Cache board states using memoization

Formula:

        Total Score = Current Score + Best Future Score

Advantages:

    • Finds globally optimal solution

Disadvantages:

    • Computationally expensive
    • Slower for large boards


===============================================================================
6. GRAPH TRAVERSAL (DFS)
===============================================================================

Depth First Search is used to detect connected components.

Procedure:

    1. Start from selected cell
    2. Visit neighboring cells with same color
    3. Continue until the entire component is found

Time Complexity:

        O(N × M)


===============================================================================
7. GRAVITY ALGORITHM
===============================================================================

After removing blocks, gravity is applied.


VERTICAL GRAVITY

Blocks fall downward to fill empty spaces.


HORIZONTAL SHIFT

Entire columns shift left if they become empty.


===============================================================================
8. AI ANALYSIS SYSTEM (GUI)
===============================================================================

The GUI version includes a real-time AI visualization system.

Features:

    • Live board updates
    • Highlighted AI moves
    • Step-by-step algorithm execution
    • Adjustable analysis speed

Displayed Information:

    • Move number
    • Current score
    • Algorithm logs
    • Execution time


===============================================================================
9. ALGORITHM COMPARISON SYSTEM
===============================================================================

A benchmarking system compares algorithm performance.

Metrics measured:

    • Final Score
    • Number of Moves
    • Execution Time


Example Output:

    Strategy        Score     Moves     Time
    ------------------------------------------------
    Greedy          450       12        0.03s
    DC + DP         520       11        0.45s
    Backtracking    540       10        2.12s


===============================================================================
10. GAME MODES
===============================================================================

SINGLE PLAYER MODE

    The player solves the board alone.


MULTIPLAYER MODE (Human vs CPU)

    Player competes against the CPU.
    CPU uses Divide & Conquer + Dynamic Programming.


AI ANALYSIS MODE (GUI)

    Allows visualization of algorithms solving the board.

    Easy    : Greedy
    Medium  : Divide & Conquer + DP
    Hard    : Backtracking + Memoization


===============================================================================
11. BOARD SIZE OPTIONS
===============================================================================

Console Version:

    1. 5 × 5
    2. 10 × 5
    3. 15 × 10
    4. 20 × 5


GUI Version:

    1. 6 × 6
    2. 8 × 8
    3. 10 × 10


===============================================================================
12. HOW TO RUN THE PROGRAM
===============================================================================

Run GUI Version

        python same_game_gui.py

Requirements:

        Python 3.x
        Tkinter


Run Console Version

        python same_game_console.py


===============================================================================
13. INPUT FORMAT
===============================================================================

Row and Column values are zero indexed.

Example:

        Row    : 2
        Column : 3

Invalid moves (single blocks) are rejected.


===============================================================================
14. OUTPUT
===============================================================================

The program displays:

    • Board state after each move
    • Player and CPU scores
    • CPU decision process
    • Algorithm logs
    • Final winner


===============================================================================
15. KEY FEATURES
===============================================================================

    ✔ ADT-based system design
    ✔ Graph representation of the board
    ✔ DFS connected component detection
    ✔ Stack-based gravity simulation
    ✔ Greedy strategy implementation
    ✔ Divide & Conquer optimization
    ✔ Dynamic Programming with memoization
    ✔ Backtracking search strategy
    ✔ AI visualization system
    ✔ Algorithm benchmarking tools
    ✔ Interactive GUI gameplay


===============================================================================
16. LEARNING OUTCOMES
===============================================================================

This project demonstrates practical applications of:

    • Graph Theory
    • Depth First Search
    • Divide & Conquer algorithms
    • Dynamic Programming
    • Backtracking techniques
    • Memoization
    • Sorting algorithms
    • Algorithm performance analysis


===============================================================================
17. CONCLUSION
===============================================================================

The Same Game project demonstrates how a simple puzzle game
can be transformed into a complex demonstration of advanced
Data Structures and Algorithms.

By integrating Greedy, Divide & Conquer with Dynamic Programming,
and Backtracking strategies, the system enables comparison
between different algorithmic approaches.

The addition of GUI visualization and benchmarking tools further
enhances understanding of algorithm behavior and performance.

This project successfully connects theoretical algorithm design
with real-world implementation.


===============================================================================
END OF README
===============================================================================
