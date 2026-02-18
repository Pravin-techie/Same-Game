# FUNCTION 2: CONQUER
# Find best move inside given region
# ==========================================================
def best_move_in_region(region_components):

    if not region_components:
        return [], 0

    best_component = []
    best_score = 0

    for comp in region_components:
        score = len(comp) ** 2
        if score > best_score:
            best_score = score
            best_component = comp

    return best_component, best_score

 # ------------------------------------------------------
    # WORKING PRINCIPLE:
    # 1. Input: A list of connected components (regions).
    #    Each component is a list of cells.
    #
    # 2. If no components exist → return empty move & score 0.
    #
    # 3. For each component:
    #       - Compute score = (size of component)^2
    #       - Compare with current best score
    #       - Update best component if score is higher
    #
    # 4. Return the component that gives maximum score.
# ------------------------------------------------------

    # TIME COMPLEXITY:
    # Let k = number of components
    # For each component we compute len(comp)
    #
    # Total Complexity:
    # O(k)    (assuming len(comp) is O(1))
    #
    # In worst case, if total cells = N,
    # overall scanning across components is O(N).
    #
    # SPACE COMPLEXITY:
    # O(1) extra space
    # ----------------------------------------------------------
