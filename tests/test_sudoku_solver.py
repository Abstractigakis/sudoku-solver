from src.sudoku_solver import SudokuSolver
from src.sudoku_game_state import SudokuGameState


EXAMPLE = SudokuSolver("./tests/sudoku_test_problems/example_a.sd")


def test_sudoku_solver_constructor():
    assert isinstance(EXAMPLE.intial_game_state, SudokuGameState)
    assert isinstance(EXAMPLE.path_to_puzzle, str)
    assert EXAMPLE.naive_back_tracking_attempt_number == 0
    assert EXAMPLE.back_tracking_with_forward_checking_attempt_number == 0
