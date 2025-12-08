# sudoku_generator_backtracking.py
# Sudoku generator using recursive backtracking and image export

import logging
import random
from typing import List, Tuple, Optional

from PIL import Image, ImageDraw, ImageFont

ListGrid = List[List[int]]


def mask(grid: ListGrid, rate: float = 0.5) -> ListGrid:
    """Randomly set some cells to 0 according to rate."""
    if rate < 0.0 or rate > 1.0:
        raise ValueError("mask rate should be between 0 and 1")

    h = len(grid)
    w = len(grid[0])
    result = [row[:] for row in grid]

    n = h * w
    masked_n = int(n * rate)
    flags = [True] * masked_n + [False] * (n - masked_n)
    random.shuffle(flags)

    for r in range(h):
        for c in range(w):
            if flags[r * w + c]:
                result[r][c] = 0

    return result


def is_valid(grid: ListGrid, row: int, col: int, num: int) -> bool:
    """Check if num can be placed at (row, col)."""
    # row
    if num in grid[row]:
        return False

    # column
    for r in range(9):
        if grid[r][col] == num:
            return False

    # 3x3 box
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if grid[r][c] == num:
                return False

    return True


def find_empty(grid: ListGrid) -> Optional[Tuple[int, int]]:
    """Return the next empty cell (row, col), or None if full."""
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                return r, c
    return None


def fill_grid_backtracking(grid: ListGrid) -> bool:
    """Fill the grid with a complete valid Sudoku solution."""
    empty = find_empty(grid)
    if not empty:
        return True

    row, col = empty
    nums = list(range(1, 10))
    random.shuffle(nums)

    for num in nums:
        if is_valid(grid, row, col, num):
            grid[row][col] = num
            if fill_grid_backtracking(grid):
                return True
            grid[row][col] = 0  # backtrack

    return False


def generate_full_grid() -> ListGrid:
    """Generate a full 9x9 Sudoku solution (no zeros)."""
    grid: ListGrid = [[0 for _ in range(9)] for _ in range(9)]
    ok = fill_grid_backtracking(grid)
    if not ok:
        logging.error("Backtracking failed to generate a full grid.")
        raise RuntimeError("Failed to generate a full Sudoku grid.")
    return grid


def generate(mask_rate: float = 0.5) -> ListGrid:
    """Generate a Sudoku puzzle by masking a full solution."""
    full = generate_full_grid()
    puzzle = mask(full, rate=mask_rate)
    return puzzle


def check_partial(grid: ListGrid) -> bool:
    """Check that rows, columns and boxes have no conflicts (ignoring zeros)."""
    # rows
    for r in range(9):
        seen = set()
        for c in range(9):
            v = grid[r][c]
            if v != 0:
                if v in seen:
                    return False
                seen.add(v)

    # columns
    for c in range(9):
        seen = set()
        for r in range(9):
            v = grid[r][c]
            if v != 0:
                if v in seen:
                    return False
                seen.add(v)

    # 3x3 boxes
    for br in range(0, 9, 3):
        for bc in range(0, 9, 3):
            seen = set()
            for r in range(br, br + 3):
                for c in range(bc, bc + 3):
                    v = grid[r][c]
                    if v != 0:
                        if v in seen:
                            return False
                        seen.add(v)

    return True


def print_grid(grid: ListGrid) -> None:
    for row in grid:
        print(" ".join(str(x) for x in row))
    print()


def draw_sudoku(grid: ListGrid, filename: str = "sudoku_puzzle.png") -> None:
    """Render the Sudoku grid as an image and save to filename."""
    cell_size = 60
    margin = 20
    size = 9 * cell_size + 2 * margin

    img = Image.new("RGB", (size, size), "white")
    draw = ImageDraw.Draw(img)

    # font
    try:
        font = ImageFont.truetype("arial.ttf", 32)
    except OSError:
        font = ImageFont.load_default()

    # grid lines
    for i in range(10):
        line_width = 3 if i % 3 == 0 else 1
        # vertical
        x = margin + i * cell_size
        draw.line((x, margin, x, margin + 9 * cell_size), fill="black", width=line_width)
        # horizontal
        y = margin + i * cell_size
        draw.line((margin, y, margin + 9 * cell_size, y), fill="black", width=line_width)

    # numbers
    for r in range(9):
        for c in range(9):
            v = grid[r][c]
            if v == 0:
                continue

            text = str(v)
            x0 = margin + c * cell_size
            y0 = margin + r * cell_size

            # use textbbox for Pillow >=10
            bbox = draw.textbbox((0, 0), text, font=font)
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]

            tx = x0 + (cell_size - w) / 2
            ty = y0 + (cell_size - h) / 2
            draw.text((tx, ty), text, fill="black", font=font)

    img.save(filename)
    print(f"Saved Sudoku image to {filename}")


# ===== Difficulty estimation by number of clues =====

def count_clues(grid: ListGrid) -> int:
    """Count how many non-zero cells (given clues) the puzzle has."""
    return sum(1 for row in grid for v in row if v != 0)


def estimate_difficulty_by_clues(grid: ListGrid) -> Tuple[str, int]:
    """
    Estimate difficulty based on number of given clues.
    You can tune the thresholds if you like.
    """
    clues = count_clues(grid)
    if clues >= 36:
        level = "Easy"
    elif clues >= 30:
        level = "Medium"
    else:
        level = "Hard"
    return level, clues


if __name__ == "__main__":
    # initial difficulty
    mask_rate = 0.6  # higher -> more empty cells -> harder

    while True:
        print("\n==============================")
        # generate puzzle with current mask_rate
        p = generate(mask_rate=mask_rate)
        print("=== Generated Sudoku puzzle ===")
        print_grid(p)
        print("Valid (no conflicts):", check_partial(p))

        level, clues = estimate_difficulty_by_clues(p)
        print(f"Number of clues: {clues}")
        print(f"Estimated difficulty: {level}")
        print(f"Current mask_rate: {mask_rate:.2f}")

        img_name = f"sudoku_puzzle_{level.lower()}_{clues}.png"
        draw_sudoku(p, img_name)

        # difficulty control
        cmd = input(
            "Adjust difficulty? (h = harder, e = easier, q = quit, other = regenerate same): "
        ).strip().lower()

        if cmd == "h":
            mask_rate = min(mask_rate + 0.05, 0.85)
            print(f"Difficulty increased. New mask_rate = {mask_rate:.2f}")
        elif cmd == "e":
            mask_rate = max(mask_rate - 0.05, 0.20)
            print(f"Difficulty decreased. New mask_rate = {mask_rate:.2f}")
        elif cmd == "q":
            print("Bye.")
            break
        else:
            print("Regenerating with same difficulty...")

