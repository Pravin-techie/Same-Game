def divide_board_regions(grid):

    regions = []
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
                regions.append(current_region)
                current_region = []

    if current_region:
        regions.append(current_region)

    return regions

# ------------------------------------------------------------
# divide_board_regions(grid)
#
# Purpose:
#   Divide the board into independent column regions
#   separated by fully empty columns.
#
# How it works:
#   1. Iterate through columns from left to right.
#   2. For each column, check if it contains at least one block.
#   3. If non-empty → add column index to current_region.
#   4. If empty → close the current region (if not empty)
#      and start a new region.
#   5. After finishing all columns, append the last region
#      if it exists.
#
# Output:
#   A list of lists.
#   Each inner list contains indices of contiguous
#   non-empty columns forming one independent region.
#
# Key Property:
#   Columns separated by an empty column are independent,
#   meaning blocks on one side cannot interact with blocks
#   on the other side due to gravity and compression rules.
#
# Time Complexity:
#   O(R × C)
#   (each column scans all rows once)
#
# Space Complexity:
#   O(C)
#   (stores column indices of regions)
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





