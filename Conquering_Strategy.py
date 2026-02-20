# ==========================================================
# CONQUER - Evaluate a region using DP
# ==========================================================
def conquer_region(grid, region_cols, memo):
    """
    CONQUER PHASE:
    Solve one independent column region using turn-aware DP.
    Only consider components fully contained within the region columns.
    """
    best_component = None
    best_value = float('-inf')

    components = get_all_components(grid)

    # Filter components to only those entirely within this region
    region_components = []
    for comp in components:
        # Check if all columns in component are within region_cols
        if all(c in region_cols for r, c in comp):
            region_components.append(comp)

    print(f"[CONQUER] Region {region_cols} has {len(region_components)} eligible components")

    for comp in region_components:
        sim = copy_grid(grid)
        remove_component(sim, comp)
        apply_gravity(sim)

        gain = len(comp) ** 2
        future = dp_score_difference(sim, memo, False)
        value = gain - future

        if value > best_value:
            best_value = value
            best_component = comp

    return best_component, best_value


# ------------------------------------------------------------
# Purpose:
#   Selects the best move for CPU from a given region
#   using Dynamic Programming evaluation.
#
# How it works:
#   1. For each component in the region:
#        • Simulate removal + apply gravity.
#        • Calculate immediate score = (size)^2.
#        • Use DP to evaluate future score difference.
#        • Compute value = gain - future.
#   2. Choose component with maximum value.
#
# Returns:
#   • Best component
#   • Best score difference
#
# Important:
#   • Represents CONQUER phase of Divide & Conquer.
#   • Uses memoization inside DP.
#   • Considers long-term optimal play (not greedy).
#
# Time Complexity:
#   O(K × (N + DP))
#   Worst case exponential due to minimax recursion.
#
# Space Complexity:
#   O(DP_states) for memo storage.
# ------------------------------------------------------------

#HORIZONTAL COMPRESSION
write_col = 0
    for read_col in range(grid.cols):
        column_has_block = any(
            grid.board[r][read_col] is not None
            for r in range(grid.rows)
        )
        
        if column_has_block:
            if write_col != read_col:
                for r in range(grid.rows):
                    grid.board[r][write_col] = grid.board[r][read_col]
                    grid.board[r][read_col] = None
            write_col += 1
            
#-------------------------------------------------------------------            
# How it works:
    # Shift all non-empty columns to the left
    # write_col → position where next valid column should be placed
    # read_col → scans each column from left to right
    # If a column contains at least one block:
    #     Move that entire column to write_col position (if different)
    #     Clear old column
    #     Increment write_col
    # Result: All empty columns move to the right side

#Time Complexity: 
    #Outer loop (columns) -> O(C)
    #Check if column has block	-> O(R)
    #Move column (worst case)-> O(R)
    #Worst case → every column has blocks and must be moved: O(C×R)
#-----------------------------------------------------------------------
