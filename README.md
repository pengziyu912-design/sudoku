# 🧩 Smart Sudoku System


A comprehensive Python-based Sudoku system capable of **generating** unique puzzles, **recognizing** Sudoku grids from images using Computer Vision (OpenCV), and **solving** them automatically with visual overlays.

This project demonstrated modular design, unit testing, and continuous integration (CI).

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
