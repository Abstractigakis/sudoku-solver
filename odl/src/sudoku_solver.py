from numpy import loadtxt, ndarray

from exceptions import ImpossiblePuzzle, InvalidSudokuGameState, MaxAtteptsReached, NoBlanks
from sudoku_game_state import SudokuGameState


class SudokuSolver:
    """Loads a numpy representation of a sudoku puzzle, and has methods that can be solve via the backtrace A algorithm with some optimizations

    mostly a name space with static methods, but also some variable state for what
    would otherwise be global couters
    """

#######################################################################################################
# loaders
#######################################################################################################
    @staticmethod
    def load_puzzle(path_to_puzzle: str) -> ndarray:
        """initalizes object instacne with a filepath to sudoku problem

        Args:
            path_to_puzzle (str): this file type must be .sd

        Returns:
            ndarray: 9x9 sudoku puzzlepuzzle
        """
        return loadtxt(path_to_puzzle, dtype=int)


#######################################################################################################
# dunders
#######################################################################################################

    def __init__(self, path_to_puzzle) -> None:
        """initalizes object variabels that are needed.  Mostly counters that would have to be lobal otherwise.

        Args:
            path_to_puzzle (str): this file type must be .sd
        """
        self.new_puzzle(path_to_puzzle)

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return str(self.initial_puzzle)

#######################################################################################################
# variable setters an resetters
#######################################################################################################
    def new_puzzle(self, path_to_puzzle: str):
        self.path_to_puzzle = path_to_puzzle
        self.initial_puzzle: SudokuGameState = SudokuGameState(
            self.load_puzzle(path_to_puzzle))

    def reset_naive_back_tracking_attempt_counter(self, max_attempts: int):
        self.naive_back_tracking_attempt_counter: int = max_attempts

    def reset_back_tracking_with_forward_checking_couter(self, max_attempts: int):
        self.back_tracking_with_forward_checking_couter = max_attempts

#######################################################################################################
# naive backtracking
#######################################################################################################
    def naive_back_tracking_attempt(self, puzzle: SudokuGameState):
        if self.naive_back_tracking_attempt_counter <= 0:
            # give up, because the naive way is too long
            raise MaxAtteptsReached(f"Max attempts reached")

        # attempting a gamestate
        self.naive_back_tracking_attempt_counter -= 1

        try:
            x, y = puzzle.get_first_blank()
            for k in range(1, 10):
                try:
                    # the case where next_puzzle is computed, meaning that it is
                    # possible to insert k into X[i][j], so we should try this
                    # and recursivly call backtracking on it
                    result_puzzle = self.naive_back_tracking_attempt(
                        puzzle=puzzle.next_state(num=k, row=x, col=y))
                except InvalidSudokuGameState:
                    pass

        except NoBlanks:
            # nothing is blank, puzzle solved!
            return puzzle

            # continue back tracking, if eventually we reach contradiction,
            if isinstance(result_puzzle, ndarray):
                # the case where the result puzzle was completed!
                #  return the puzzle as the final solution
                return result_puzzle

                # this k caused a issue, either it can't be inserted, or
                # it can be inserted, but caused a deeper issue that could
                # not be resolved, try k+1

        # at this point, for a given blank spot in the
        # puzzle, we have tried to insert all numbers,
        # but none were suitable.  So puzzle is not solvable
        raise ImpossiblePuzzle("Puzzle is intractible")

    def naive_back_tracking(self, max_attempts=10000):
        self.reset_naive_back_tracking_attempt_counter(max_attempts)

        try:
            solution = self.naive_back_tracking_attempt(
                puzzle=self.initial_puzzle)

        except MaxAtteptsReached:
            return False, max_attempts

        except ImpossiblePuzzle:
            return False, max_attempts

        return solution, max_attempts - self.naive_back_tracking_attempt_counter

#######################################################################################################
# backtracking with forward checking
#######################################################################################################
    def back_tracking_with_forward_checking_attempt(self, puzzle: ndarray):
        if self.back_tracking_with_forward_checking_couter <= 0:
            # give up, because the naive way is too long
            raise MaxAtteptsReached(f"Max attempts reached")

        # attempting a gamestate
        self.back_tracking_with_forward_checking_couter -= 1

        # this is the naive part, attempt to fill the first blank tile we see
        first_blank_tile = self.get_first_blank(puzzle)
        if(not first_blank_tile):
            # nothing is blank, puzzle solved!
            return puzzle

        x, y = first_blank_tile

        #  compute domains of the puzzle
        for k in range(1, 10):

            next_puzzle, next_puzzle_domain = __class__.attempt_insert_num(
                puzzle=puzzle, num=k, row=x, col=y)

            if isinstance(next_puzzle, ndarray):
                # the case where next_puzzle is computed, meaning that it is
                # possible to insert k into X[i][j], so we should try this
                # and recursivly call backtracking on it

                result_puzzle = self.naive_back_tracking_attempt(
                    puzzle=next_puzzle)

                # continue back tracking, if eventually we reach contradiction,
                if isinstance(result_puzzle, ndarray):
                    # the case where the result puzzle was completed!
                    #  return the puzzle as the final solution
                    return result_puzzle

                # this k caused a issue, either it can't be inserted, or
                # it can be inserted, but caused a deeper issue that could
                # not be resolved, try k+1

        # at this point, for a given blank spot in the
        # puzzle, we have tried to insert all numbers,
        # but none were suitable.  So puzzle is not solvable
        raise ImpossiblePuzzle("Puzzle is intractible")

    def back_tracking_with_forward_checking(self,  max_attempts=10000):
        self.reset_back_tracking_with_forward_checking_couter(max_attempts)

        try:
            solution = self.naive_back_tracking_attempt(
                puzzle=self.initial_puzzle)

        except MaxAtteptsReached:
            return False, max_attempts

        except ImpossiblePuzzle:
            return False, max_attempts

        return solution, max_attempts - self.naive_back_tracking_attempt_counter


if __name__ == '__main__':
    SS = SudokuSolver("../test_sudoku_problems/example_a.sd")
    res = SS.naive_back_tracking()
    print(res)
