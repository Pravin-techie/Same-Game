# ==========================================================
# FUNCTION 3: COMBINE (Complete Divide & Conquer)
# ==========================================================

def best_move_from_left_and_right(grid):
  
    left_region, right_region = divide_board_regions(grid)
    left_comp, left_score = best_move_in_region(left_region)
    right_comp, right_score = best_move_in_region(right_region)

    if left_score >= right_score:
        return left_comp, left_score, "Left Region"
    else:
        return right_comp, right_score, "Right Region"


# ==========================================================
# OVERALL TIME COMPLEXITY
# ==========================================================
#
# Divide  : O(n)
# Conquer : O(n)
# Combine : O(1)
#
# T(n) = O(n) + O(n) + O(1)
# T(n) = O(n)
#
# FINAL TIME COMPLEXITY: O(n)
#
# ==========================================================
# HOW THIS FUNCTION WORKS
# ==========================================================
#
# 1. First, the grid is divided into two regions:
#    left half and right half.
#
# 2. Then, each region is solved independently to find
#    the best possible move and its score.
#
# 3. Finally, the function compares both scores and
#    returns the move from the region with the higher score.
#
# This follows the Divide and Conquer strategy:
# Divide  -> Split the problem
# Conquer -> Solve subproblems separately
# Combine -> Choose the better result
# ==========================================================
