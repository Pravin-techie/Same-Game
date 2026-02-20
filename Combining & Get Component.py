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
# COMBINE
# ==========================================================
def combine_results(results):
    """
    COMBINE PHASE:
    Select best move among all independent regions.
    """
    best_component = None
    best_value = float('-inf')
    best_region_idx = -1

    for i, (comp, value) in enumerate(results):
        if value > best_value:
            best_value = value
            best_component = comp
            best_region_idx = i

    print(f"[COMBINE] Selected region {best_region_idx} with value: {best_value}")
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
# The function:
#   1. Initializes variables to track the best component.
#   2. Iterates through all region results.
#   3. Compares their values.
#   4. Selects the component with the highest value.
#   5. Prints which region index was selected.
#   6. Returns the best component.
#
# This effectively merges the solutions of multiple
# independent regions and chooses the optimal one.
#
# Time Complexity:
# O(k)
# Where k = number of independent regions (length of results).
# The loop runs once over all region results.
#
# Space Complexity:
# O(1)
# Only a few variables are used regardless of input size.
# ----------------------------------------------------------

