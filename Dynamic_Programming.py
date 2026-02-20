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
#Worst case: O(2^N × N²)


def cpu_best_move(grid):
    """
    CPU MOVE USING TRUE DIVIDE & CONQUER + DP
    - DIVIDE: Split into independent column regions (separated by empty columns)
    - CONQUER: Evaluate each region independently with turn-aware DP
    - COMBINE: Select best overall move from all regions
    """
    print("\n" + "="*50)
    print("CPU TURN - TRUE DIVIDE & CONQUER + DP")
    print("="*50)
    
    memo = {}
    
    # -------- PHASE 1: DIVIDE --------
    print("\n🔹 PHASE 1: DIVIDE")
    regions = divide_board_regions(grid)
    
    # -------- PHASE 2: CONQUER --------
    print("\n🔹 PHASE 2: CONQUER")
    results = []
    
    for i, region_cols in enumerate(regions):
        print(f"\n--- Region {i} (cols {region_cols}) ---")
        comp, value = conquer_region(grid, region_cols, memo)
        results.append((comp, value))
    
    # -------- PHASE 3: COMBINE --------
    print("\n🔹 PHASE 3: COMBINE")
    best_component = combine_results(results)
    
    if best_component:
        print(f"[RESULT] Selected component of size {len(best_component)} at {best_component[0]}")
    else:
        print("[RESULT] No valid moves found")
    
    print("="*50)
    return best_component
