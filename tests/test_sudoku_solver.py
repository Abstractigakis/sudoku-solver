
from unittest import TestCase, main

from src.sudoku_solver import SudokuSolver


class TestSudokuSolver(TestCase):
    def setUp(self) -> None:
        self.example_a = SudokuSolver("./test_sudoku_problems/example_a.sd")
        self.ones = SudokuSolver("./test_sudoku_problems/ones.sd")
        self.empty = SudokuSolver("./test_sudoku_problems/empty.sd")
        self.row_one_done = SudokuSolver(
            "./test_sudoku_problems/row_one_done.sd")


if __name__ == '__main__':
    main()
