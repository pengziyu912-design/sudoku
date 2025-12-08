import cv2
import numpy as np
import os

GRID_SIZE = 9
DIGIT_SIZE = 32

TRIM_RATIO = 0.12
EMPTY_THRESHOLD = 0.004
SCORE_THRESHOLD = 0.45
DEBUG_MATCH = False



def binarize_image(gray):
    _, bin_img = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )
    return bin_img


def extract_digit_region(bin_cell, min_white_ratio=0.002):
    h, w = bin_cell.shape
    total = h * w
    white = cv2.countNonZero(bin_cell)

    if white / float(total) < min_white_ratio:
        return None

    ys, xs = np.where(bin_cell > 0)
    if len(xs) == 0 or len(ys) == 0:
        return None

    top, bottom = ys.min(), ys.max()
    left, right = xs.min(), xs.max()

    digit = bin_cell[top:bottom + 1, left:right + 1]

    pad = 2
    digit_padded = cv2.copyMakeBorder(
        digit, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=0
    )
    digit_resized = cv2.resize(
        digit_padded, (DIGIT_SIZE, DIGIT_SIZE), interpolation=cv2.INTER_AREA
    )

    return digit_resized


# Templates

def load_templates(template_dir="templates"):
    templates = {}
    for d in range(1, 10):
        path = os.path.join(template_dir, f"{d}.png")
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

        if img is None:
            print(f"[WARN] cannot read template: {path}")
            continue

        bin_img = binarize_image(img)
        digit_img = extract_digit_region(bin_img, min_white_ratio=0.0005)

        if digit_img is None:
            print(f"[WARN] template {path} is empty")
            continue

        templates[d] = digit_img

    print(f"[INFO] loaded {len(templates)} templates.")
    return templates


def match_digit(digit_img, templates, score_thresh=SCORE_THRESHOLD, debug=False, pos=None):
    best_digit = 0
    best_score = -1.0

    for d, tmpl in templates.items():
        result = cv2.matchTemplate(digit_img, tmpl, cv2.TM_CCOEFF_NORMED)
        score = result[0][0]

        if score > best_score:
            best_score = score
            best_digit = d

    if debug and pos is not None:
        r, c = pos
        print(f"cell({r},{c}) -> best_digit={best_digit}, score={best_score:.3f}")

    if best_score < score_thresh:
        return 0

    return best_digit


# Board Processing

def load_sudoku_image(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Cannot read image: {image_path}")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bin_img = binarize_image(gray)
    return img, bin_img


def find_board_bounds(bin_img):
    ys, xs = np.where(bin_img > 0)
    if len(xs) == 0 or len(ys) == 0:
        raise RuntimeError("Cannot locate board.")

    top = int(ys.min())
    bottom = int(ys.max())
    left = int(xs.min())
    right = int(xs.max())
    return top, bottom, left, right


def extract_cell(bin_img, row, col, bounds, trim_ratio=TRIM_RATIO):
    top, bottom, left, right = bounds
    board_h = bottom - top + 1
    board_w = right - left + 1

    cell_h = board_h // GRID_SIZE
    cell_w = board_w // GRID_SIZE

    y1 = top + row * cell_h
    y2 = y1 + cell_h
    x1 = left + col * cell_w
    x2 = x1 + cell_w

    cell = bin_img[y1:y2, x1:x2]

    mh = int(cell_h * trim_ratio)
    mw = int(cell_w * trim_ratio)
    cell = cell[mh:cell_h - mh, mw:cell_w - mw]

    return cell


def debug_save_cells(bin_img, bounds, out_dir="cells"):
    os.makedirs(out_dir, exist_ok=True)

    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            cell = extract_cell(bin_img, r, c, bounds)
            path = os.path.join(out_dir, f"{r}_{c}.png")
            cv2.imwrite(path, cell)

    print(f"[INFO] saved 81 cells to folder: {out_dir}")


# Main Recognition

def recognize_sudoku(image_path, template_dir="templates",
                     save_cells=False, debug_match=False):
    templates = load_templates(template_dir)
    if not templates:
        return None

    _, bin_img = load_sudoku_image(image_path)
    bounds = find_board_bounds(bin_img)

    if save_cells:
        debug_save_cells(bin_img, bounds)

    grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    non_empty = 0

    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            cell = extract_cell(bin_img, r, c, bounds)

            digit_img = extract_digit_region(cell)
            if digit_img is None:
                grid[r][c] = 0
                continue

            d = match_digit(
                digit_img,
                templates,
                debug=debug_match,
                pos=(r, c)
            )

            if d != 0:
                non_empty += 1

            grid[r][c] = d

    print(f"[INFO] recognized non-empty cells: {non_empty}")
    return grid


# Entry

if __name__ == "__main__":
    img_name = input("Enter Sudoku image filename (e.g. sudoku_puzzle.png): ").strip()

    if not img_name:
        print("No filename given.")
        raise SystemExit(1)

    if not os.path.exists(img_name):
        print(f"File not found: {img_name}")
        raise SystemExit(1)

    grid = recognize_sudoku(
        img_name,
        template_dir="templates",
        save_cells=False,
        debug_match=False
    )

    if grid is None:
        raise SystemExit(1)

    print("=== Recognized Sudoku Grid ===")
    print("[")
    for row in grid:
        print("  ", row, ",")
    print("]")

    print("\nPretty Sudoku:")
    for row in grid:
        print(" ".join(str(x) if x != 0 else "." for x in row))
