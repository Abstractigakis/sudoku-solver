from numpy import ndarray, array, full
from pytest import raises
from unittest import TestCase
from src.enums import BackTrackingHeuristics
from src.exceptions import CantRemoveFromBlank, InvalidInsert, NoBlanks
from src.sudoku_solver import SudokuSolver


class TestSudokuSolver(TestCase):
    def setUp(self):
        self.EMPTY = SudokuSolver(
            "./tests/sudoku_test_problems/empty.sd")
        self.EXAMPLE = SudokuSolver(
            "./tests/sudoku_test_problems/example_a.sd")
        self.ONES = SudokuSolver(
            "./tests/sudoku_test_problems/ones.sd")
        self.ROW_ONE_DONE = SudokuSolver(
            "./tests/sudoku_test_problems/row_one_done.sd")
        self.IMPOSSIBLE = SudokuSolver(
            "./tests/sudoku_test_problems/impossible.sd")
        self.NOT_VIABLE = SudokuSolver(
            "./tests/sudoku_test_problems/not_viable.sd")

    def test_sudoku_solver_constructor(self):
        assert isinstance(self.EXAMPLE.X, ndarray)
        assert isinstance(self.EXAMPLE.D, ndarray)
        assert isinstance(self.EXAMPLE.path_to_puzzle, str)
        assert self.EXAMPLE.attempt == 0

    def test_is_num_in_row(self):
        assert self.EXAMPLE.is_num_in_row(num=7, row=0) == True
        assert self.EXAMPLE.is_num_in_row(num=7, row=1) == True
        assert self.EXAMPLE.is_num_in_row(num=7, row=5) == False
        assert self.EXAMPLE.is_num_in_row(num=7, row=8) == False

    def test_is_num_in_col(self):
        assert self.EXAMPLE.is_num_in_col(num=7, col=0) == True
        assert self.EXAMPLE.is_num_in_col(num=7, col=2) == True
        assert self.EXAMPLE.is_num_in_col(num=7, col=1) == False
        assert self.EXAMPLE.is_num_in_col(num=7, col=5) == False

    def test_is_num_in_section(self):
        assert self.EXAMPLE.is_num_in_section(num=7, row=1, col=1) == True
        assert self.EXAMPLE.is_num_in_section(num=7, row=2, col=5) == True
        assert self.EXAMPLE.is_num_in_section(num=7, row=8, col=8) == False
        assert self.EXAMPLE.is_num_in_section(num=7, row=5, col=5) == False

    def test_get_section(self):
        actual = self.EXAMPLE.get_section(row=5, col=5)
        expected = array([[0, 0, 0], [5, 4, 0], [8, 6, 2]])
        assert (actual == expected).all() == True

        actual = self.EXAMPLE.get_section(row=8, col=8)
        expected = array([[0, 0, 0], [4, 5, 2], [0, 0, 3]])
        assert (actual == expected).all() == True

    def test_get_first_blank(self):
        assert (self.EXAMPLE.get_first_blank() == array([0, 1])).all()
        assert (self.EMPTY.get_first_blank() == array([0, 0])).all()
        assert (self.ROW_ONE_DONE.get_first_blank() == array([1, 4])).all()
        with raises(NoBlanks):
            self.ONES.get_first_blank()

    def test_domains(self):
        assert (self.EMPTY.D == full((9, 9, 9), True)).all()
        assert self.ONES.D[0][0][0] == False
        assert self.ONES.D[0][0][1] == True
        row_1_domain_plane = self.ROW_ONE_DONE.D[0, :, :]
        assert (row_1_domain_plane == False).all() == True

    def test_insert_remove(self):
        expected = full((9, 9), 0)
        expected[0][0] = 1
        self.EMPTY.insert(1, 0, 0)
        assert (self.EMPTY.X == expected).all()
        # assert (D == SudokuSolver.calc_D(expected)).all()
        with raises(InvalidInsert):
            self.EMPTY.insert(1, 0, 2)
        with raises(CantRemoveFromBlank):
            self.EMPTY.remove(0, 2)
        self.EMPTY.remove(0, 0)
        assert (self.EMPTY.X == full((9, 9), 0)).all()

    def test_insert_remove_forward_checking(self):
        expected = full((9, 9), 0)
        expected[0][0] = 1
        self.EMPTY.insert(1, 0, 0, BackTrackingHeuristics.FORWARD_CHECKING)
        assert (self.EMPTY.X == expected).all()
        with raises(InvalidInsert):
            self.EMPTY.insert(1, 0, 2, BackTrackingHeuristics.FORWARD_CHECKING)
        with raises(CantRemoveFromBlank):
            self.EMPTY.remove(0, 2)
        self.EMPTY.remove(0, 0)
        assert (self.EMPTY.X == full((9, 9), 0)).all()

    def test_is_viable(self):
        assert self.NOT_VIABLE.is_viable() == False
        assert self.EMPTY.is_viable() == True
        assert self.EXAMPLE.is_viable() == True


# def test_is_square_impossible():
#     for i in range(9):
#         for j in range(9):
#             # everything is possible on an empty board
#             assert EMPTY.is_square_impossible(i, j) == False
#     for i in range(9):
#         # noting is impossible when numbers are already there
#         assert ROW_ONE_DONE.is_square_impossible(i, 1) == False
#     assert IMPOSSIBLE.is_square_impossible(0, 0) == True


# def test_is_game_state_impossible():
#     assert IMPOSSIBLE.is_game_state_impossible() == True
