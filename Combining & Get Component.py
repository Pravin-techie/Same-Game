# ==========================================================
# GET COMPONENT - WITH BOUNDARY SAFETY
# ==========================================================
def get_component(grid, r, c):
    """
    Get connected component at position (r,c) with boundary safety.
    """
    # Boundary safety check
    if r < 0 or r >= grid.rows or c < 0 or c >= grid.cols:
        return []
    
    # Empty cell check
    if grid.board[r][c] is None:
        return []

    visited = set()
    component = []
    bfs(grid, r, c, grid.board[r][c], visited, component)
    return component


# ----------------------------------------------------------
# Explanation:
# This function returns all connected same-colored cells
# starting from position (r, c).
# It first ensures the given position is inside the board
# and not empty. Then it performs a BFS traversal to explore
# all adjacent cells (up, down, left, right) that have the
# same color and collects them into the 'component' list.

# ----------------------------------------------------------
# Time Complexity:
# O(ROWS × COLS) in the worst case,
# because BFS may visit every cell once if the entire board
# consists of the same color.
# ----------------------------------------------------------

# ==========================================================
# COMBINING RESULT
# ==========================================================

def combine_results(left_result, right_result, overlap_result):
    """
    COMBINE PHASE:
    Select best component from all three regions
    """
    candidates = [left_result, right_result, overlap_result]
    
    best_component = []
    best_value = float('-inf')

    print(f"\n[COMBINE] Left: {left_result[1]} | Right: {right_result[1]} | Overlap: {overlap_result[1]}")
    
    for comp, value in candidates:
        if value > best_value:
            best_value = value
            best_component = comp

    region_names = ["LEFT", "RIGHT", "OVERLAP"]
    for i, (comp, value) in enumerate(candidates):
        if comp == best_component and value == best_value:
            print(f"[COMBINE] Selecting {region_names[i]} region (value: {value})")
            break
    
    return best_component


# ----------------------------------------------------------
# Explanation:
# This function represents the COMBINE phase of an extended
# Divide & Conquer approach where three subregions exist:
#   1. Left region
#   2. Right region
#   3. Overlap region
#
# Each region result is expected in the form:
#   (component, value)
# where:
#   component -> list of cells
#   value     -> evaluated score of that component
#
# The function:
#   1. Stores all three region results into a list.
#   2. Iterates through them to find the maximum value.
#   3. Selects the component corresponding to that maximum value.
#   4. Prints which region was selected.
#
# This merges (combines) the solutions of three subproblems
# into one final optimal decision.
#
# Time Complexity:
# O(1)
# Since the number of regions is fixed (3), the loop runs
# a constant number of times. Therefore, execution time
# does not depend on board size.
#
# Space Complexity:
# O(1)
# Only a small fixed-size list (3 elements) is created.
# ----------------------------------------------------------
