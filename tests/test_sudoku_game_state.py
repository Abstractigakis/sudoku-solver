

from numpy import ndarray, array
from pytest import raises
from src.exceptions import NoBlanks
from src.sudoku_game_state import SudokuGameState

EMPTY = SudokuGameState.load_game_state_from_sd_file(
    "./tests/sudoku_test_problems/empty.sd")

EXAMPLE = SudokuGameState.load_game_state_from_sd_file(
    "./tests/sudoku_test_problems/example_a.sd")

ONES = SudokuGameState.load_game_state_from_sd_file(
    "./tests/sudoku_test_problems/ones.sd")

ROW_ONE_DONE = SudokuGameState.load_game_state_from_sd_file(
    "./tests/sudoku_test_problems/row_one_done.sd")


def test_load_sudoku_game_state():
    EMPTY = SudokuGameState.load_game_state_from_sd_file(
        "./tests/sudoku_test_problems/empty.sd")
    assert isinstance(EMPTY.puzzle, ndarray)
    assert EMPTY.puzzle.shape == (9, 9)


def test_is_num_in_row():
    assert EXAMPLE.is_num_in_row(num=7, row=0) == True
    assert EXAMPLE.is_num_in_row(num=7, row=1) == True
    assert EXAMPLE.is_num_in_row(num=7, row=5) == False
    assert EXAMPLE.is_num_in_row(num=7, row=8) == False


def test_is_num_in_col():
    assert EXAMPLE.is_num_in_col(num=7, col=0) == True
    assert EXAMPLE.is_num_in_col(num=7, col=2) == True
    assert EXAMPLE.is_num_in_col(num=7, col=1) == False
    assert EXAMPLE.is_num_in_col(num=7, col=5) == False


def test_is_num_in_section():
    assert EXAMPLE.is_num_in_section(num=7, row=1, col=1) == True
    assert EXAMPLE.is_num_in_section(num=7, row=2, col=5) == True
    assert EXAMPLE.is_num_in_section(num=7, row=8, col=8) == False
    assert EXAMPLE.is_num_in_section(num=7, row=5, col=5) == False


def test_get_section():
    actual = EXAMPLE.get_section(row=5, col=5)
    expected = array([[0, 0, 0], [5, 4, 0], [8, 6, 2]])
    assert (actual == expected).all() == True

    actual = EXAMPLE.get_section(row=8, col=8)
    expected = array([[0, 0, 0], [4, 5, 2], [0, 0, 3]])
    assert (actual == expected).all() == True


def test_get_first_blank():
    print(ROW_ONE_DONE)
    assert (EXAMPLE.get_first_blank() == array([0, 1])).all()
    assert (EMPTY.get_first_blank() == array([0, 0])).all()
    assert (ROW_ONE_DONE.get_first_blank() == array([1, 4])).all()
    with raises(NoBlanks):
        ONES.get_first_blank()
