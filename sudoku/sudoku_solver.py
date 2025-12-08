# sudoku_solver.py

from typing import List, Optional
from sudoku_recognition import recognize_sudoku  # your existing file
import cv2
import os

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


# ---------- Draw solved grid on image ----------

def draw_solution_on_image(image_path: str, solved_grid: Grid,
                           output_path: str = "sudoku_solved.png"):
    """
    Draw the solved grid on top of the original image and save it.
    All cells are drawn (including given numbers).
    """
    img = cv2.imread(image_path)
    if img is None:
        print("Cannot load image for drawing.")
        return

    h, w, _ = img.shape

    cell_h = h // 9
    cell_w = w // 9

    for r in range(9):
        for c in range(9):
            val = solved_grid[r][c]
            text = str(val)

            # roughly center text inside the cell
            x = c * cell_w + cell_w // 4
            y = r * cell_h + int(cell_h * 0.7)

            cv2.putText(
                img,
                text,
                (x, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0, 0, 255),   # red digits
                2,
                cv2.LINE_AA,
            )

    cv2.imwrite(output_path, img)
    print(f"[INFO] Solved image saved as: {output_path}")


# ---------- Full pipeline: recognize + solve + export image ----------

def solve_and_export_image(image_path: str):
    """
    image -> recognize_sudoku -> solve_sudoku -> print -> draw_solution_on_image
    """
    grid = recognize_sudoku(
        image_path,
        template_dir="templates",
        save_cells=False,
        debug_match=False,
    )

    if grid is None:
        print("Recognition failed.")
        return

    print_grid(grid, "Recognized Sudoku Grid")
    print_pretty(grid, "Recognized Sudoku (pretty)")

    if solve_sudoku(grid):
        print_grid(grid, "Solved Sudoku Grid")
        print_pretty(grid, "Solved Sudoku (pretty)")
        draw_solution_on_image(image_path, grid)
    else:
        print("No valid solution found.")


# ---------- Entry ----------

if __name__ == "__main__":
    img_name = input("Enter Sudoku image filename: ").strip()

    if not img_name:
        print("No filename given.")
        raise SystemExit(1)

    if not os.path.exists(img_name):
        print(f"File not found: {img_name}")
        raise SystemExit(1)

    solve_and_export_image(img_name)
