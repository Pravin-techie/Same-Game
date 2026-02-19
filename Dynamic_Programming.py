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
#Worst case: O(N² + S × N²)


def cpu_best_move(grid):
    """
    CPU MOVE USING Divide & Conquer + DP
    Turn-aware adversarial score difference evaluation.
    """
    
    memo = {}
    components = divide_moves(grid)
    
    if not components:
        return []
    
    best_component = []
    best_value = float('-inf')
    
    for comp in components:
        sim = copy_grid(grid)
        remove_component(sim, comp)
        apply_gravity(sim)
        
        gain = len(comp) ** 2
        value = gain - dp_score_difference(sim, memo, False)
        
        if value > best_value:
            best_value = value
            best_component = comp
    
    return best_component
