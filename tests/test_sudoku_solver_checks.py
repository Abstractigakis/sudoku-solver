
from unittest import TestCase, main
from src.sudoku_solver import SudokuSolver


class TestSudokuSolver(TestCase):
    def setUp(self) -> None:
        self.solver = SudokuSolver("./sudoku_problems/48/7.sd")

    def test_is_num_in_row(self):
        self.assertTrue(self.solver.is_num_in_row(num=7, row=0))
        self.assertTrue(self.solver.is_num_in_row(num=7, row=1))
        self.assertFalse(self.solver.is_num_in_row(num=7, row=5))
        self.assertFalse(self.solver.is_num_in_row(num=7, row=8))

    def test_is_num_in_col(self):
        self.assertTrue(self.solver.is_num_in_col(num=7, col=0))
        self.assertTrue(self.solver.is_num_in_col(num=7, col=2))
        self.assertFalse(self.solver.is_num_in_col(num=7, col=1))
        self.assertFalse(self.solver.is_num_in_col(num=7, col=5))

    def test_is_num_in_section(self):
        self.assertTrue(self.solver.is_num_in_section(num=7, row=1, col=1))
        self.assertTrue(self.solver.is_num_in_section(num=7, row=2, col=5))
        self.assertFalse(self.solver.is_num_in_section(num=7, row=8, col=8))
        self.assertFalse(self.solver.is_num_in_section(num=7, row=5, col=5))


if __name__ == '__main__':
    main()
