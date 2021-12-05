
from unittest import TestCase, main

import numpy as np
from src.sudoku_solver import SudokuSolver


class TestSudokuSolver(TestCase):
    def setUp(self) -> None:
        self.example_a = SudokuSolver("./test_sudoku_problems/a.sd")
        self.ones = SudokuSolver("./test_sudoku_problems/ones.sd")
        self.empty = SudokuSolver("./test_sudoku_problems/empty.sd")
        self.row_one_done = SudokuSolver(
            "./test_sudoku_problems/row_one_done.sd")

    def test_is_num_in_row(self):
        self.assertTrue(SudokuSolver.is_num_in_row(
            puzzle=self.example_a.initial_puzzle, num=7, row=0))
        self.assertTrue(SudokuSolver.is_num_in_row(
            puzzle=self.example_a.initial_puzzle, num=7, row=1))
        self.assertFalse(SudokuSolver.is_num_in_row(
            puzzle=self.example_a.initial_puzzle, num=7, row=5))
        self.assertFalse(SudokuSolver.is_num_in_row(
            puzzle=self.example_a.initial_puzzle, num=7, row=8))

    def test_is_num_in_col(self):
        self.assertTrue(SudokuSolver.is_num_in_col(
            puzzle=self.example_a.initial_puzzle, num=7, col=0))
        self.assertTrue(SudokuSolver.is_num_in_col(
            puzzle=self.example_a.initial_puzzle, num=7, col=2))
        self.assertFalse(SudokuSolver.is_num_in_col(
            puzzle=self.example_a.initial_puzzle, num=7, col=1))
        self.assertFalse(SudokuSolver.is_num_in_col(
            puzzle=self.example_a.initial_puzzle, num=7, col=5))

    def test_is_num_in_section(self):
        self.assertTrue(SudokuSolver.is_num_in_section(
            puzzle=self.example_a.initial_puzzle, num=7, row=1, col=1))
        self.assertTrue(SudokuSolver.is_num_in_section(
            puzzle=self.example_a.initial_puzzle, num=7, row=2, col=5))
        self.assertFalse(SudokuSolver.is_num_in_section(
            puzzle=self.example_a.initial_puzzle, num=7, row=8, col=8))
        self.assertFalse(SudokuSolver.is_num_in_section(
            puzzle=self.example_a.initial_puzzle, num=7, row=5, col=5))

    def test_get_section(self):
        actual = SudokuSolver.get_section(
            puzzle=self.example_a.initial_puzzle, row=5, col=5)
        expected = np.array([[0, 0, 0], [5, 4, 0], [8, 6, 2]])
        self.assertTrue((actual == expected).all())

        actual = SudokuSolver.get_section(
            puzzle=self.example_a.initial_puzzle, row=8, col=8)
        expected = np.array([[0, 0, 0], [4, 5, 2], [0, 0, 3]])
        self.assertTrue((actual == expected).all())

    def test_get_first_blank(self):
        assert SudokuSolver.get_first_blank(
            puzzle=self.example_a.initial_puzzle) == (0, 1)
        assert SudokuSolver.get_first_blank(
            self.row_one_done.initial_puzzle
        ) == (1, 4)
        assert SudokuSolver.get_first_blank(
            puzzle=self.ones.initial_puzzle) == False
        assert SudokuSolver.get_first_blank(
            puzzle=self.empty.initial_puzzle) == (0, 0)

    def test_get_domains(self):
        actual = SudokuSolver.get_domains(puzzle=self.empty.initial_puzzle)
        expected = np.full((9, 9, 9), True)
        self.assertTrue((actual == expected).all())

        self.assertFalse(SudokuSolver.get_domains(
            puzzle=self.ones.initial_puzzle)[0][0][0])
        self.assertTrue(SudokuSolver.get_domains(
            puzzle=self.ones.initial_puzzle)[0][0][1])

        # row 0 is complete, so no numbers should be valid in row = 0 col[0:8]
        row_1_domain_plane = SudokuSolver.get_domains(
            puzzle=self.row_one_done.initial_puzzle)[0, :, :]
        all_false = (row_1_domain_plane == False).all()
        self.assertTrue(all_false)


if __name__ == '__main__':
    main()
