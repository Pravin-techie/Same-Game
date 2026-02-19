def divide_board_regions(grid):

    mid = grid.cols // 2
    left_region = []
    right_region = []
    overlap_region = []

    all_components = get_all_components(grid)

    for comp in all_components:
        left_present = any(c < mid for r, c in comp)
        right_present = any(c >= mid for r, c in comp)

        # Pure left component
        if left_present and not right_present:
            left_region.append(comp)

        # Pure right component
        elif right_present and not left_present:
            right_region.append(comp)

        # Overlapping component (spans both sides)
        else:   # (left_present and right_present)
            overlap_region.append(comp)

    print(f"\n[DIVIDE] Board split at column {mid}")
    print(f"Left region (pure left): {len(left_region)} components")
    print(f"Right region (pure right): {len(right_region)} components")
    print(f"Overlap region (spans both): {len(overlap_region)} components")
    
    return left_region, right_region, overlap_region


# ------------------------------------------------------------
# divide_board_regions(grid)
#
# Purpose:
#   Split removable components into LEFT, RIGHT,
#   and OVERLAP regions using the board’s vertical midpoint.
#
# How it works:
#   1. mid = grid.cols // 2
#   2. For each component:
#        • If all cells are left of mid  → Left region
#        • If all cells are right of mid → Right region
#        • If it crosses mid             → Overlap region
#
# Important:
#   • No component is split into parts.
#   • Overlapping components are stored separately.
#   • Regions do NOT duplicate components.
#
# Why overlap region:
#   To handle components that span across both subproblems
#   in Divide & Conquer without breaking connectivity.
#
# Time Complexity:
#   O(K)
#   where K = total number of cells across all components.
#
# Space Complexity:
#   O(C)
#   where C = number of components stored.
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



