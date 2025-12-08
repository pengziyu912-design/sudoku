# sudoku_solver.py

from typing import List, Optional
from sudoku_recognition import recognize_sudoku  # use your existing file

Grid = List[List[int]]  # 9x9 grid, 0 means empty


# ---------- Core solver ----------

def is_valid(grid: Grid, row: int, col: int, val: int) -> bool:
    """Check if val can be placed at (row, col)."""
    # row
    if any(grid[row][c] == val for c in range(9)):
        return False
    # column
    if any(grid[r][col] == val for r in range(9)):
        return False
    # 3x3 box
    br = (row // 3) * 3
    bc = (col // 3) * 3
    for r in range(br, br + 3):
        for c in range(bc, bc + 3):
            if grid[r][c] == val:
                return False
    return True


def find_empty_cell(grid: Grid) -> Optional[tuple]:
    """Return coordinates of next empty cell, or None if full."""
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                return r, c
    return None


def solve_sudoku(grid: Grid) -> bool:
    """
    Backtracking solver.
    Modifies grid in place. Returns True if solved.
    """
    empty = find_empty_cell(grid)
    if empty is None:
        return True  # solved

    row, col = empty

    for val in range(1, 10):
        if is_valid(grid, row, col, val):
            grid[row][col] = val
            if solve_sudoku(grid):
                return True
            grid[row][col] = 0  # backtrack

    return False


# ---------- Printing helpers ----------

def print_grid(grid: Grid, title: str = "Grid"):
    print(f"=== {title} ===")
    print("[")
    for row in grid:
        print("  ", row, ",")
    print("]")
    print()


def print_pretty(grid: Grid, title: str = "Grid"):
    print(title)
    for r in range(9):
        line = ""
        for c in range(9):
            v = grid[r][c]
            ch = str(v) if v != 0 else "."
            if c % 3 == 0 and c != 0:
                line += " |"
            line += " " + ch
        print(line)
        if r % 3 == 2 and r != 8:
            print("-" * 25)
    print()


# ---------- Main: recognize from image + solve ----------

if __name__ == "__main__":
    img_name = input("Enter Sudoku image filename: ").strip()

    if not img_name:
        print("No filename given.")
        raise SystemExit(1)

    grid = recognize_sudoku(
        img_name,
        template_dir="templates",
        save_cells=False,
        debug_match=False,
    )

    if grid is None:
        print("Recognition failed.")
        raise SystemExit(1)

    print_grid(grid, "Recognized Sudoku Grid")
    print_pretty(grid, "Recognized Sudoku (pretty)")

    if solve_sudoku(grid):
        print_grid(grid, "Solved Sudoku Grid")
        print_pretty(grid, "Solved Sudoku (pretty)")
    else:
        print("No valid solution found.")
