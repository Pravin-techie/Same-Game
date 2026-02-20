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
# COMBINING PHASE
# ==========================================================
def combine_results(results):
    """
    COMBINE PHASE:
    Select best move among all region results.
    """

    best_component = None
    best_value = float('-inf')

    for comp, value in results:
        if comp is not None and value > best_value:
            best_value = value
            best_component = comp

    return best_component


# ----------------------------------------------------------
# Explanation:
# This function represents the COMBINE phase of the
# Divide & Conquer strategy.
#
# The input 'results' is a list where each element is:
#     (component, value)
# where:
#     component -> list of cells representing a possible move
#     value     -> evaluated score (or score difference)
#
# The function works as follows:
# 1. Initialize best_value as negative infinity to ensure
#    that any real score will replace it.
# 2. Iterate through each (component, value) pair in results.
# 3. Ignore invalid components (comp is None).
# 4. Compare the value with the current best_value.
# 5. If a higher value is found, update best_value and
#    store the corresponding component.
# 6. After checking all region results, return the
#    component with the highest value.
#
# This effectively merges the evaluated results from
# multiple regions and selects the optimal move.
#
# Time Complexity:
# O(k), where k = number of region results.
# The function performs a single pass through the list.
#
# Space Complexity:
# O(1), since only a few tracking variables are used
# regardless of the size of the input list.
# ----------------------------------------------------------


