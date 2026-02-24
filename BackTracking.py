def backtracking_best_score(grid, is_cpu_turn):
    """
    Pure Backtracking (no memoization)
    Explores all possible move sequences recursively.
    Returns score difference (CPU - Human).
    """

    components = get_all_components(grid)

    # Base case: no more moves
    if not components:
        return 0

    if is_cpu_turn:
        best = float('-inf')

        for comp in components:
            # --- Save current state (for backtracking) ---
            original_board = copy_grid(grid)

            # --- Make move ---
            remove_component(grid, comp)
            apply_gravity(grid)

            gain = len(comp) ** 2
            future = backtracking_best_score(grid, False)

            best = max(best, gain - future)

            # --- Undo move (Backtrack) ---
            grid.board = original_board.board

        return best

    else:
        worst = float('inf')

        for comp in components:
            # --- Save current state ---
            original_board = copy_grid(grid)

            # --- Make move ---
            remove_component(grid, comp)
            apply_gravity(grid)

            gain = len(comp) ** 2
            future = backtracking_best_score(grid, True)

            worst = min(worst, future - gain)

            # --- Undo move ---
            grid.board = original_board.board

        return worst



def cpu_best_move_backtracking(grid):
    """
    CPU move using pure Backtracking (no DP).
    Explores entire game tree.
    """

    components = get_all_components(grid)

    best_value = float('-inf')
    best_component = None

    for comp in components:
        original_board = copy_grid(grid)

        remove_component(grid, comp)
        apply_gravity(grid)

        gain = len(comp) ** 2
        future = backtracking_best_score(grid, False)

        value = gain - future

        if value > best_value:
            best_value = value
            best_component = comp

        # Backtrack
        grid.board = original_board.board

    return best_component
