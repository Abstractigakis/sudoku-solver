from numpy import ndarray, array, full
from pytest import raises
from unittest import TestCase
from src.exceptions import InvalidSudokuGameState, NoBlanks
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

    def test_sudoku_solver_constructor(self):
        assert isinstance(self.EXAMPLE.X_0, ndarray)
        assert isinstance(self.EXAMPLE.D_0, ndarray)
        assert isinstance(self.EXAMPLE.path_to_puzzle, str)
        assert self.EXAMPLE.attempt == 0

    def test_is_num_in_row(self):
        assert SudokuSolver.is_num_in_row(
            self.EXAMPLE.X_0, num=7, row=0) == True
        assert SudokuSolver.is_num_in_row(
            self.EXAMPLE.X_0, num=7, row=1) == True
        assert SudokuSolver.is_num_in_row(
            self.EXAMPLE.X_0, num=7, row=5) == False
        assert SudokuSolver.is_num_in_row(
            self.EXAMPLE.X_0, num=7, row=8) == False

    def test_is_num_in_col(self):
        assert SudokuSolver.is_num_in_col(
            self.EXAMPLE.X_0, num=7, col=0) == True
        assert SudokuSolver.is_num_in_col(
            self.EXAMPLE.X_0, num=7, col=2) == True
        assert SudokuSolver.is_num_in_col(
            self.EXAMPLE.X_0, num=7, col=1) == False
        assert SudokuSolver.is_num_in_col(
            self.EXAMPLE.X_0, num=7, col=5) == False

    def test_is_num_in_section(self):
        assert SudokuSolver.is_num_in_section(
            self.EXAMPLE.X_0, num=7, row=1, col=1) == True
        assert SudokuSolver.is_num_in_section(
            self.EXAMPLE.X_0, num=7, row=2, col=5) == True
        assert SudokuSolver.is_num_in_section(
            self.EXAMPLE.X_0, num=7, row=8, col=8) == False
        assert SudokuSolver.is_num_in_section(
            self.EXAMPLE.X_0, num=7, row=5, col=5) == False

    def test_get_section(self):
        actual = SudokuSolver.get_section(self.EXAMPLE.X_0, row=5, col=5)
        expected = array([[0, 0, 0], [5, 4, 0], [8, 6, 2]])
        assert (actual == expected).all() == True

        actual = SudokuSolver.get_section(self.EXAMPLE.X_0, row=8, col=8)
        expected = array([[0, 0, 0], [4, 5, 2], [0, 0, 3]])
        assert (actual == expected).all() == True

    def test_get_first_blank(self):
        assert (SudokuSolver.get_first_blank(
            self.EXAMPLE.X_0) == array([0, 1])).all()
        assert (SudokuSolver.get_first_blank(
            self.EMPTY.X_0) == array([0, 0])).all()
        assert (SudokuSolver.get_first_blank(
            self.ROW_ONE_DONE.X_0) == array([1, 4])).all()
        with raises(NoBlanks):
            SudokuSolver.get_first_blank(self.ONES.X_0)

    def test_domains(self):
        assert (self.EMPTY.D_0 == full((9, 9, 9), True)).all()
        assert self.ONES.D_0[0][0][0] == False
        assert self.ONES.D_0[0][0][1] == True
        row_1_domain_plane = self.ROW_ONE_DONE.D_0[0, :, :]
        assert (row_1_domain_plane == False).all() == True

    def test_insert(self):
        expected = full((9, 9), 0)
        expected[0][0] = 1
        X, D = SudokuSolver.insert(self.EMPTY.X_0, self.EMPTY.D_0, 1, 0, 0)
        print(D)
        assert (X == expected).all()
        assert (D == SudokuSolver.calc_D(expected)).all()
    # with raises(InvalidSudokuGameState):
    #     one_in_top_right.next_game_state(1, 0, 2)


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
