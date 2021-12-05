
from unittest import TestCase, main

import numpy as np
from src.sudoku_solver import SudokuSolver


class TestSudokuSolver(TestCase):
    def setUp(self) -> None:
        self.solver = SudokuSolver("./test_sudoku_problems/a.sd")
        self.ones = SudokuSolver("./test_sudoku_problems/ones.sd")
        self.empty = SudokuSolver("./test_sudoku_problems/empty.sd")
        self.row_one_done = SudokuSolver(
            "./test_sudoku_problems/row_one_done.sd")

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

    def test_get_section(self):
        actual = self.solver.get_section(row=5, col=5)
        expected = np.array([[0, 0, 0], [5, 4, 0], [8, 6, 2]])
        self.assertTrue((actual == expected).all())

        actual = self.solver.get_section(row=8, col=8)
        expected = np.array([[0, 0, 0], [4, 5, 2], [0, 0, 3]])
        self.assertTrue((actual == expected).all())

    def test_get_first_blank(self):
        assert self.solver.get_first_blank() == (0, 1)
        assert self.row_one_done.get_first_blank() == (1, 4)
        assert self.ones.get_first_blank() == False
        assert self.empty.get_first_blank() == (0, 0)

    def test_get_domains(self):
        actual = self.empty.get_domains()
        expected = np.full((9, 9, 9), True)
        self.assertTrue((actual == expected).all())

        self.assertFalse(self.ones.get_domains()[0][0][0])
        self.assertTrue(self.ones.get_domains()[0][0][1])

        # row 0 is complete, so no numbers should be valid in row = 0 col[0:8]
        row_1_domain_plane = self.row_one_done.get_domains()[0, :, :]
        all_false = (row_1_domain_plane == False).all()
        self.assertTrue(all_false)


if __name__ == '__main__':
    main()
