# sudoku_solver.py

from typing import List, Optional
from sudoku_recognition import recognize_sudoku  # your existing file
import cv2
import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
try:
    import tkinter as tk
    from tkinter import filedialog
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False

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
def draw_solution_on_image(image_path: str, solved_grid: Grid, original_grid: Grid,
                           output_path: str = "sudoku_solved.png"):
    """
    Draw the solved grid using PIL (Pillow) for better font rendering and centering.
    """
    # 1. Load image using OpenCV (to handle Chinese paths correctly)
    try:
        img_array = np.fromfile(image_path, dtype=np.uint8)
        img_cv2 = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    except Exception as e:
        print(f"[ERROR] Could not read image: {e}")
        return

    if img_cv2 is None:
        print("[ERROR] Cannot load image for drawing.")
        return

    # 2. Convert OpenCV image (BGR) to PIL image (RGB)
    img_rgb = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(img_rgb)
    draw = ImageDraw.Draw(pil_img)

    # 3. Calculate grid dimensions
    width, height = pil_img.size
    cell_w = width / 9
    cell_h = height / 9

    # 4. Load Font (Arial) - Dynamic size based on cell height
    font_size = int(cell_h * 0.6)  # Font is 60% of cell height
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except OSError:
        font = ImageFont.load_default()

    # 5. Draw Red Numbers
    for r in range(9):
        for c in range(9):
            # Only draw if the cell was originally empty
            if original_grid[r][c] != 0:
                continue

            text = str(solved_grid[r][c])

            # Calculate precise center using text bounding box
            left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
            text_w = right - left
            text_h = bottom - top

            # Center position
            x = (c * cell_w) + (cell_w - text_w) / 2 - left
            y = (r * cell_h) + (cell_h - text_h) / 2 - top

            # Draw text in RED (R=255, G=0, B=0)
            draw.text((x, y), text, fill=(255, 0, 0), font=font)

    # 6. Save the result
    try:
        # Convert back to BGR for OpenCV saving OR just save with PIL (easier)
        pil_img.save(output_path) 
        print(f"[INFO] Solved image saved as: {output_path}")
    except Exception as e:
        print(f"[ERROR] Failed to save image: {e}")

# ---------- Full pipeline: recognize + solve + export image ----------
def solve_and_export_image(image_path: str):
    """
    Pipeline: Image -> Recognize -> Solve -> Print -> Draw Solution
    Saves output as: {original_name}_solved.{extension}
    """
    print(f"\n[INFO] Processing file: {image_path}")
    
    # 1. Recognize the Sudoku from the image
    grid = recognize_sudoku(
        image_path,
        template_dir="templates",
        save_cells=False,
        debug_match=False,
    )

    if grid is None:
        print("[ERROR] Recognition failed.")
        return

    print_grid(grid, "Recognized Sudoku Grid")
    
    # Make a copy of the original grid BEFORE solving
    original_grid = [row[:] for row in grid]

    # 2. Solve the Sudoku
    if solve_sudoku(grid):
        print_grid(grid, "Solved Sudoku Grid")
        print_pretty(grid, "Solved Sudoku (Pretty)")
        
        # 3. Export the result image with suffix "_solved"
        # ---------------------------------------------------
        # [NEW] Split path into root and extension
        # e.g., "puzzles/my_sudoku.png" -> ("puzzles/my_sudoku", ".png")
        # ---------------------------------------------------
        root, ext = os.path.splitext(image_path)
        
        # Construct new path: "puzzles/my_sudoku_solved.png"
        output_path = f"{root}_solved{ext}"
        
        draw_solution_on_image(image_path, grid, original_grid, output_path=output_path)
        
    else:
        print("[INFO] No valid solution found for this puzzle.")

# ---------- Entry ----------

if __name__ == "__main__":
    img_name = ""

    # Method 1: Try GUI File Selection
    if GUI_AVAILABLE:
        try:
            print("Launching file selector window...")
            root = tk.Tk()
            root.withdraw()
            
            img_name = filedialog.askopenfilename(
                title="Select Sudoku Image to Solve",
                filetypes=[("Image files", "*.png;*.jpg;*.jpeg")]
            )
            root.destroy()
        except Exception as e:
            print(f"[WARN] GUI selector failed, switching to manual input.")
            GUI_AVAILABLE = False

    # Method 2: Manual Input / Drag & Drop
    if not img_name:
        if GUI_AVAILABLE:
            print("No file selected via window.")
        
        prompt = "Please enter (or drag) the image filename: "
        img_name = input(prompt).strip()
        
        # Remove quotes if user dragged a file
        img_name = img_name.strip('"').strip("'")

    # Validate file existence
    if not img_name or not os.path.exists(img_name):
        print(f"[ERROR] File not found: {img_name}")
        sys.exit(1)
        
    # Run the solver pipeline
    solve_and_export_image(img_name)