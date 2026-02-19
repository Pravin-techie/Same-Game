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
# 🔥 NEW FUNCTION 3: COMBINE - Select best region
# ==========================================================
def combine_results(left_comp, left_value, right_comp, right_value):
    """
    COMBINE PHASE:
    Choose the region that gives better score difference.
    """
    print(f"\n[COMBINE] Left region value: {left_value}")
    print(f"[COMBINE] Right region value: {right_value}")
    
    if left_value >= right_value:
        print("[COMBINE] Selecting LEFT region move")
        return left_comp
    else:
        print("[COMBINE] Selecting RIGHT region move")
        return right_comp


# ----------------------------------------------------------
# Explanation:
# This function represents the COMBINE phase of the
# Divide & Conquer strategy.
#
# It receives:
#   - The best component from the left region
#   - Its evaluated score/value
#   - The best component from the right region
#   - Its evaluated score/value
#
# It compares both region scores and selects the component
# that provides the higher value (better move).
#
# Essentially, it merges the results of two subproblems
# (left and right regions) and chooses the optimal one.
#
# Time Complexity:
# O(1)
# Because it only performs a constant-time comparison
# between two values and returns one result.
#
# Space Complexity:
# O(1)
# No extra data structures proportional to input size
# are created.
# ----------------------------------------------------------
