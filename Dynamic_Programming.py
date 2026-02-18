def board_to_tuple(grid):
    return tuple(tuple(row) for row in grid.board)

def copy_grid(grid):
    new_grid = GridADT(ROWS, COLS)
    new_grid.board = [row[:] for row in grid.board]
    return new_grid

def dp_best_score(grid, memo):
    # -------------------------------------------------------------------
    # Function Name:
    #   dp_best_score
    #
    # Purpose:
    #   Recursively computes the maximum achievable score from the current
    #   board state using a dynamic programming approach with memoization.
    #   Each move consists of removing a connected component of size > 1,
    #   scoring points equal to (component_size)^2, and applying gravity.
    #
    # -------------------------------------------------------------------
    # Parameters:
    #   grid : GridADT object
    #       Current board state.
    #   memo : dict
    #       Stores previously computed results for board states to avoid
    #       redundant computations.
    #
    # Returns:
    #   max_score : int
    #       Maximum score achievable from this board state onward.
    #
    # -------------------------------------------------------------------
    # Working Process:
    #   Step 1: Convert the board into an immutable tuple for memoization.
    state = board_to_tuple(grid)

    #   Step 2: Return precomputed result if the state has been evaluated.
    if state in memo:
        return memo[state]

    #   Step 3: Check if the game is over (no removable components).
    if is_game_over(grid):
        memo[state] = 0
        return 0

    #   Step 4: Initialize the maximum score for this state.
    max_score = 0
    visited_cells = set()  # Tracks which cells have been included in a component

    #   Step 5: Iterate through all cells of the board
    for r in range(ROWS):
        for c in range(COLS):
            #   Step 5a: If the cell is non-empty and not visited, find its component
            if grid.board[r][c] and (r, c) not in visited_cells:

                #   Step 5b: Get all connected cells of the same color/value
                comp = get_component(grid, r, c)

                #   Step 5c: Mark all component cells as visited
                for cell in comp:
                    visited_cells.add(cell)

                #   Step 5d: Only consider components of size > 1
                if len(comp) > 1:
                    #   Step 5e: Make a copy of the board to simulate this move
                    temp = copy_grid(grid)

                    #   Step 5f: Remove the component and apply gravity
                    remove_component(temp, comp)
                    apply_gravity(temp)

                    #   Step 5g: Recursively compute the future score from the new board
                    future_score = dp_best_score(temp, memo)

                    #   Step 5h: Calculate total score for this move
                    total_score = len(comp) ** 2 + future_score

                    #   Step 5i: Update max_score if this move is better
                    if total_score > max_score:
                        max_score = total_score

    #   Step 6: Memoize the result for the current board state
    memo[state] = max_score

    #   Step 7: Return the maximum score achievable from this state
    return max_score
