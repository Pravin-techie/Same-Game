def divide_board_regions(grid):
    mid = grid.cols // 2
    left_region = []
    right_region = []
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
        elif left_present and right_present:
            left_region.append(comp)
            right_region.append(comp)

    print(f"\n[DIVIDE] Board split at column {mid}")
    print(f"Left region: {len(left_region)} components")
    print(f"Right region: {len(right_region)} components")
    print("(Overlapping components included in both regions)")
    return left_region, right_region


# -------------------------------------------------------------------
# Function Name:
#   divide_board_regions
#
# Purpose:
#   Divides all removable connected components into two regions:
#       • Left Region
#       • Right Region
#   The assignment depends on where the majority of the component’s
#   cells lie relative to the board's vertical midpoint.
#
# -------------------------------------------------------------------
# Division Rule:
#   1. Midpoint is computed using:
#          mid = COLS // 2
#
#   2. For every removable component:
#          • Count cells where column < mid  → left_count
#          • right_count = total size - left_count
#
#   3. Region Assignment:
#          • If left_count >= right_count → Left Region
#          • Else → Right Region
#
# -------------------------------------------------------------------
# Assumptions:
#   • COLS is defined globally.
#   • get_all_valid_components(grid) exists.
#   • Components are returned as list of (row, col) tuples.
#   • Only components of size > 1 are considered removable.
#
# -------------------------------------------------------------------
# Working Process:
#   Step 1: Calculate midpoint of the board.
#   Step 2: Fetch all valid removable components.
#   Step 3: For each component:
#              - Count how many cells lie in the left half.
#              - Determine remaining cells in right half.
#   Step 4: Compare counts and assign region.
#   Step 5: Return left_region and right_region lists.
#
# -------------------------------------------------------------------
# Time Complexity:
#   O(N × M)
#   Each cell is processed once through component detection
#   and region distribution counting.
#
# Space Complexity:
#   O(N × M)
#   Extra space used for component storage and visited tracking.
#
# -------------------------------------------------------------------
# Example:
#
#   If COLS = 6 → mid = 3
#
#   Column Index:
#       0   1   2   |   3   4   5
#
#   Component A:
#       [(0,0), (0,1), (1,0), (1,1)]
#       All columns < 3
#       → Assigned to Left Region
#
#   Component B:
#       [(0,4), (1,4), (2,5)]
#       All columns ≥ 3
#       → Assigned to Right Region
#
# -------------------------------------------------------------------
# Edge Cases Covered:
#   • No removable components present
#   • Component distributed across both halves
#   • Even or odd number of columns
#   • Empty board
# -------------------------------------------------------------------

