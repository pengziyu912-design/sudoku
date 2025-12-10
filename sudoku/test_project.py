import unittest
import numpy as np
import sudoku_generator as generator      
import sudoku_solver as solver           
import sudoku_recognition as recognition  

class TestSudokuGenerator(unittest.TestCase):
    """Tests for the Sudoku Generator module."""

    def setUp(self):
        # Create an empty 9x9 grid before testing
        self.empty_grid = [[0 for _ in range(9)] for _ in range(9)]

    def test_is_valid_basic(self):
        """Test basic row/column/box validation logic."""
        self.empty_grid[0][0] = 5
        
        # 1. Test Valid: Placing a distinct number in the same row
        self.assertTrue(generator.is_valid(self.empty_grid, 0, 1, 6), 
                        "Should allow distinct number in same row")

        # 2. Test Row Conflict: Placing duplicate 5 in the same row
        self.assertFalse(generator.is_valid(self.empty_grid, 0, 8, 5), 
                         "Should detect row conflict")

        # 3. Test Column Conflict: Placing duplicate 5 in the same column
        self.assertFalse(generator.is_valid(self.empty_grid, 8, 0, 5), 
                         "Should detect column conflict")

    def test_generate_full_grid(self):
        """Test if a full grid is generated correctly."""
        grid = generator.generate_full_grid()
        
        # Check size
        self.assertEqual(len(grid), 9)
        self.assertEqual(len(grid[0]), 9)
        
        # Check that it contains no zeros (fully filled)
        for row in grid:
            self.assertNotIn(0, row, "Full grid should not contain zeros")

    def test_generate_puzzle_structure(self):
        """Test the structure of the generated puzzle."""
        # Use low difficulty (retain more numbers) for a quick test
        puzzle = generator.generate(mask_rate=0.2)
        
        self.assertEqual(len(puzzle), 9)
        # Check if there are holes (should contain 0)
        has_zero = any(0 in row for row in puzzle)
        self.assertTrue(has_zero, "Generated puzzle should have holes (0)")


class TestSudokuSolver(unittest.TestCase):
    """Tests for the Sudoku Solver module."""

    def test_find_empty(self):
        """Test the function for finding empty cells."""
        grid = [[0]*9 for _ in range(9)]
        grid[0][0] = 1
        # The first empty cell should be (0, 1)
        self.assertEqual(solver.find_empty_cell(grid), (0, 1))

    def test_solve_simple_case(self):
        """Test ability to solve a simple puzzle."""
        # First generate a full solution using generator
        full_grid = generator.generate_full_grid()
        
        # Remove one number (make a hole)
        original_val = full_grid[0][0]
        full_grid[0][0] = 0
        
        # Call solver to solve it
        solved = solver.solve_sudoku(full_grid)
        
        self.assertTrue(solved, "Solver should return True for valid puzzle")
        self.assertEqual(full_grid[0][0], original_val, "Solver should restore the correct number")


class TestSudokuRecognition(unittest.TestCase):
    """Tests for the Recognition module."""

    def test_binarize_logic(self):
        """Test binarization logic (using fake image data)."""
        # Create a 100x100 fake image (numpy array)
        fake_img = np.zeros((100, 100), dtype=np.uint8)
        fake_img[:, 50:] = 255 
        
        # Perform binarization
        bin_img = recognition.binarize_image(fake_img)
        
        # Check return type and shape
        self.assertIsInstance(bin_img, np.ndarray)
        self.assertEqual(bin_img.shape, (100, 100))

    def test_extract_digit_region_empty(self):
        """Test that a completely black cell should return None."""
        empty_cell = np.zeros((50, 50), dtype=np.uint8)
        result = recognition.extract_digit_region(empty_cell)
        self.assertIsNone(result, "Should return None for empty black cell")


if __name__ == '__main__':
    # Run all tests
    unittest.main(verbosity=2)