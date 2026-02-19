# ==========================================================
# 🔥 NEW FUNCTION 2: CONQUER - Evaluate a region using DP
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


# ==========================================================
# WORKING PRINCIPLE
# ==========================================================
# 1. This function represents the CONQUER phase of Divide & Conquer.
# 2. It receives a list of components belonging to a specific region.
# 3. For each component:
#       a) It creates a copy of the board.
#       b) Simulates removing that component.
#       c) Applies gravity to update the board.
# 4. It calculates the immediate gain = (size of component)^2.
# 5. Then it calls dp_score_difference() to compute optimal future
#    score difference assuming the opponent plays optimally.
# 6. It computes:
#           value = gain - future
#    which represents total advantage for CPU.
# 7. It selects the component that gives maximum score difference.
# 8. Finally, it returns the best component and its value.


# ==========================================================
# TIME COMPLEXITY ANALYSIS
# ==========================================================
# Let:
#   R = number of rows
#   C = number of columns
#   N = R * C (total cells)
#   K = number of components in region
#
# For each component:
#   - copy_grid()         → O(N)
#   - remove_component()  → O(N) (worst case)
#   - apply_gravity()     → O(N)
#   - dp_score_difference → Exponential in worst case
#                           but reduced using memoization
#
# So per component cost ≈ O(N + DP)
#
# Therefore total cost:
#   O(K * (N + DP))
#
# In worst case without memoization:
#   DP is exponential → O(b^d)
#
# With memoization:
#   DP reduces to number of unique board states.
#
# Overall practical complexity:
#   Dominated by DP recursion and state exploration.
#
# So overall complexity:
#   O(K * N + DP_states)
#
# Space Complexity:
#   O(DP_states) for memoization storage.
