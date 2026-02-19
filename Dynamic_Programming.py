# FUNCTION 2: DP SCORE DIFFERENCE - Turn-aware optimal evaluation 
# Worst case:  O(2^N × N²)

def dp_score_difference(grid, memo, is_cpu_turn):
    """
    Returns maximum score DIFFERENCE (current player - opponent)
    from this board state.
    """

    state = (tuple(tuple(row) for row in grid.board), is_cpu_turn)

    if state in memo:
        return memo[state]

    components = divide_moves(grid)

    if not components:
        return 0

    if is_cpu_turn:
        best = float('-inf')
        for comp in components:
            sim = copy_grid(grid)
            remove_component(sim, comp)
            apply_gravity(sim)

            gain = len(comp) ** 2
            future = dp_score_difference(sim, memo, False)

            best = max(best, gain - future)

        memo[state] = best
        return best

    else:
        worst = float('inf')
        for comp in components:
            sim = copy_grid(grid)
            remove_component(sim, comp)
            apply_gravity(sim)

            gain = len(comp) ** 2
            future = dp_score_difference(sim, memo, True)

            worst = min(worst, future - gain)

        memo[state] = worst
        return worst

# FUNCTION 3: CPU MOVE - Using turn-aware adversarial DP
#Worst case: O(S × N²)


def cpu_best_move(grid):
    """
    CPU MOVE USING VISIBLE DIVIDE & CONQUER + DP
    - DIVIDE: Split board into Left/Right regions
    - CONQUER: Evaluate each region using turn-aware DP
    - COMBINE: Select best region
    """
    
    print("\n" + "="*50)
    print("CPU TURN - DIVIDE & CONQUER + DP")
    print("="*50)
    
    memo = {}
    
    # -------- DIVIDE PHASE --------
    print("\n🔹 PHASE 1: DIVIDE")
    left_region, right_region = divide_board_regions(grid)
    
    # -------- CONQUER PHASE --------
    print("\n🔹 PHASE 2: CONQUER")
    left_comp, left_value = conquer_region(grid, left_region, memo)
    right_comp, right_value = conquer_region(grid, right_region, memo)
    
    # -------- COMBINE PHASE --------
    print("\n🔹 PHASE 3: COMBINE")
    best_component = combine_results(left_comp, left_value, right_comp, right_value)
    
    print("="*50)
    return best_component
