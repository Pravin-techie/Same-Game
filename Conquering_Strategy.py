# ==========================================================
# CONQUER - Evaluate a region using DP
# ==========================================================
def conquer_region(grid, region_components, memo):
    """
    CONQUER PHASE:
    Evaluate each component in a region using turn-aware DP.
    Returns the best component from this region and its value.
    """
    if not region_components:
        return [], float('-inf')
    
    best_component = []
    best_value = float('-inf')

    print(f"\n[CONQUER] Evaluating {len(region_components)} components in region...")
    
    for comp in region_components:
        sim = copy_grid(grid)
        remove_component(sim, comp)
        apply_gravity(sim)

        gain = len(comp) ** 2
        future = dp_score_difference(sim, memo, False)  # After CPU move, human's turn
        value = gain - future

        if value > best_value:
            best_value = value
            best_component = comp

    print(f"[CONQUER] Best component score difference: {best_value}")
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

