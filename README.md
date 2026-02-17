SAME GAME – ADT & DSA BASED IMPLEMENTATION (EVALUATION 2)

Project Type    : Data Structures & Algorithms Mini Project
Language        : Python
Game Type       : Console Based Puzzle Game
Paradigm        : ADT + Advanced Algorithmic Design
Members         : Pravin R 
                  Vidhyadharan RP
                  Srijith S
                  Vijay Sathappan T
----------------------------------------------------------
1. PROJECT DESCRIPTION
----------------------------------------------------------
This project is a console-based implementation of the
classic "Same Game" using Data Structures and Algorithms.

The objective of the game is to remove connected blocks
of the same color from a grid to score points. The game
ends when no more valid moves exist.

Evaluation 2 significantly enhances the earlier version
by replacing the Greedy CPU strategy with Dynamic
Programming for optimal decision making.

This implementation focuses on:
• Abstract Data Types (ADT)
• Graph Traversal using DFS
• Stack usage for gravity
• Merge Sort for structured move ordering
• Dynamic Programming with Memoization
• Optimal Game Logic Design

----------------------------------------------------------
2. GAME MODES
----------------------------------------------------------
1. Single Player Mode
   - Player plays alone
   - Final score displayed at the end

2. Multiplayer Mode (Human vs CPU)
   - Human and CPU play alternately
   - CPU uses Dynamic Programming + Merge Sort
   - CPU evaluates future game states recursively
   - Winner is decided based on final score

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
   - Prevents redundant traversal

5. List ADT
   - Stores connected components (clusters)
   - Stores possible move options

6. Dictionary ADT
   - Used for memoization in Dynamic Programming
   - Stores board states with computed best scores

----------------------------------------------------------
4. ALGORITHMS USED
----------------------------------------------------------

• Depth First Search (DFS)
  - Finds connected components of same color
  - Uses recursion and backtracking
  - Time Complexity: O(N × M)

• Merge Sort
  - Sorts possible CPU moves by total score
  - Time Complexity: O(K log K)

• Dynamic Programming (NEW in Evaluation 2)
  - Replaces Greedy strategy
  - Recursively evaluates all possible move sequences
  - Uses memoization to avoid recomputation
  - Score Formula:
        score = (component_size)^2 + dp(next_state)

• Gravity Algorithm
  - Blocks fall down after removal using stack logic
  - Time Complexity: O(N × M)

----------------------------------------------------------
5. GAME RULES
----------------------------------------------------------
1. Player selects a cell using row and column
2. Only connected blocks of the same color are removed
3. Minimum 2 connected blocks required for a valid move
4. Score Formula:
      Score = (Number of blocks removed)^2
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

Note:
Larger board sizes increase Dynamic Programming
computation complexity.

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
• CPU move is automatically computed using DP
• Final scores and winner displayed at game end

----------------------------------------------------------
10. KEY FEATURES
----------------------------------------------------------
✔ Menu Driven Interface
✔ Clean ADT-based Design
✔ Graph Traversal using DFS
✔ Stack-based Gravity Logic
✔ Merge Sort for Move Selection
✔ Dynamic Programming based Optimal CPU
✔ Memoization using Dictionary
✔ Fully Commented and Modular Code
✔ Improved Algorithmic Intelligence

----------------------------------------------------------
11. CONCLUSION
----------------------------------------------------------
This project demonstrates how a simple puzzle game can be
modeled using advanced Data Structures and Algorithms.

Compared to Evaluation 1, this version replaces the
Greedy strategy with Dynamic Programming, ensuring
optimal CPU decision-making rather than locally optimal
choices.

It clearly showcases the practical application of:
• Graph Theory
• DFS Traversal
• Stack Operations
• Sorting Algorithms
• Dynamic Programming
• Memoization Techniques

This enhanced version reflects deeper understanding
of algorithmic optimization and computational reasoning.

----------------------------------------------------------
END OF README – EVALUATION 2
----------------------------------------------------------
