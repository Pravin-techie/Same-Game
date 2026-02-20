def divide_board_regions(grid):
    
    independent_regions = []
    current_region = []

    for c in range(grid.cols):
        column_has_block = any(
            grid.board[r][c] is not None
            for r in range(grid.rows)
        )

        if column_has_block:
            current_region.append(c)
        else:
            if current_region:
                independent_regions.append(current_region)
                current_region = []

    if current_region:
        independent_regions.append(current_region)

    print(f"\n[DIVIDE] Independent column regions: {independent_regions}")
    return independent_regions

# ------------------------------------------------------------
# divide_board_regions(grid)
#
# Purpose:
#   Split the board into independent column regions
#   separated by completely empty columns.
#
# How it works:
#   1. Traverse columns from left to right.
#   2. If a column has at least one block → add to current region.
#   3. If a column is empty → close the current region.
#   4. Continue until all columns are processed.
#
# Important:
#   • Regions contain contiguous non-empty columns.
#   • No column belongs to more than one region.
#   • Regions represent independent subproblems.
#
# Why separation by empty column:
#   An empty column guarantees that blocks on the left
#   cannot interact with blocks on the right.
#
# Time Complexity:
#   O(R × C)
#   where R = rows, C = columns.
#
# Space Complexity:
#   O(C)
#   to store column indices of regions.
# ------------------------------------------------------------

def get_optimal_hint(grid):
    memo = {}
    components = get_all_components(grid)
    
    if not components:
        return None, 0
    
    best_component = None
    best_total = -1
    
    for comp in components:
        sim = copy_grid(grid)
        remove_component(sim, comp)
        apply_gravity(sim)
        
        future = -dp_score_difference(sim, memo, True)
        total = len(comp) ** 2 + future
        
        if total > best_total:
            best_total = total
            best_component = comp
    
    return best_component[0], len(best_component) ** 2

# ------------------------------------------------------------
# get_optimal_hint(grid)
#
# Purpose:
#   Finds the best possible move for the human player
#   using Dynamic Programming evaluation.
#
# How it works:
#   1. Get all removable components.
#   2. For each component:
#        • Simulate removal + gravity.
#        • Use DP to evaluate future score impact.
#        • total = immediate_score + future_advantage
#   3. Select component with maximum total score.
#
# Returns:
#   • A hint cell (row, col) from best component
#   • Immediate score of that component
#
# Important:
#   • Uses memoization to avoid recomputation.
#   • Evaluates long-term advantage, not just greedy size.
#
# Time Complexity:
#   Exponential in worst case (DP minimax),
#   but reduced using memoization.
#
# Space Complexity:
#   O(N × M) for memo storage and grid copies.
# ------------------------------------------------------------




