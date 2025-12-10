# 🧩 Smart Sudoku System

![Build Status](https://github.com/pengziyu912-design/sudoku/actions/workflows/sudoku_test.yml/badge.svg)

A comprehensive Python-based Sudoku system capable of **generating** unique puzzles, **recognizing** Sudoku grids from images using Computer Vision (OpenCV), and **solving** them automatically with visual overlays.

This project was developed as part of a Software Engineering coursework, demonstrating modular design, unit testing, and continuous integration (CI).

## ✨ Features

* **Sudoku Generator**:
    * Generates valid 9x9 Sudoku puzzles with guaranteed **unique solutions**.
    * Adjustable difficulty levels (Easy, Medium, Hard) based on clue count.
    * Exports puzzles as high-quality PNG images with sequential numbering to prevent overwriting.
* **Sudoku Solver**:
    * **Smart Input**: Supports GUI file selection and Drag-and-Drop functionality.
    * **Computer Vision**: Automatically extracts the grid and digits from images using OpenCV.
    * **Backtracking Algorithm**: Solves any valid puzzle efficiently.
    * **Visual Overlay**: Draws the solution in **red** directly onto the original image, perfectly centered in the empty cells.
* **Quality Assurance**:
    * Includes a comprehensive **Unit Test** suite covering generation, validation, and solving logic.
    * Automated testing via **GitHub Actions (CI)** ensures code stability on every push.

## 📂 Project Structure

```text
/
├── .github/workflows/   # CI/CD configuration for GitHub Actions
├── sudoku/              # Main Source Code Directory
│   ├── templates/       # Digit templates for OCR (1.png - 9.png)
│   ├── sudoku_generator.py    # Generates new puzzles
│   ├── sudoku_recognition.py  # OCR logic (OpenCV)
│   ├── sudoku_solver.py       # Main solver application
│   ├── test_project.py        # Unit tests
│   └── requirements.txt       # Python dependencies
├── .gitignore           # System file to ignore temporary files
└── README.md            # Project documentation

## 🚀 Installation
Clone the repository:

Bash

git clone https://github.com/pengziyu912-design/sudoku.git
cd sudoku
Navigate to the source folder:

Bash

cd sudoku
Install dependencies:

Bash

pip install -r requirements.txt

```markdown
## 📖 Usage

### 1. Generating a Puzzle
Run the generator to create a new Sudoku image.
```bash
python sudoku_generator.py
Controls:

h: Increase difficulty (remove more numbers).

e: Decrease difficulty.

q: Quit.

Enter: Regenerate with current settings.

Output: Files will be saved as sudoku_puzzle_medium_33_1.png, _2.png, etc.

2. Solving a Puzzle
Run the solver to recognize and solve an existing image.

Bash

python sudoku_solver.py
A file selection window will pop up. Select any Sudoku image (e.g., one generated in step 1).

Alternatively, you can drag and drop the image file path into the terminal.

Process:

The system recognizes the digits.

Solves the puzzle mathematically.

Generates a solution image (e.g., sudoku_puzzle_..._solved.png) with answers in red.

🧪 Running Tests
This project uses unittest to ensure reliability. You can run the tests locally to verify everything is working:

Bash

python test_project.py
Expected Output: Ran 7 tests in 0.xxx s ... OK

(Note: These tests are also run automatically on GitHub via GitHub Actions whenever code is pushed.)

🛠️ Technologies Used
Python 3.9+

OpenCV (cv2): Image processing and digit recognition.

Pillow (PIL): Image generation and text rendering.

NumPy: Matrix operations.

Tkinter: GUI file selection.

GitHub Actions: Continuous Integration (CI).
