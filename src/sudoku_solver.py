from numpy import ndarray, loadtxt, argwhere

from numpy.core.numeric import full
from src.exceptions import InvalidInsert, MaxAtteptsReached, NoBlanks, PuzzleUnsolvable, NotSudokuFile, CantRemoveFromBlank
from src.enums import BackTrackingHeuristics


class SudokuSolver:

    #######################################################################################################
    # loaders
    #######################################################################################################
    @staticmethod
    def load_game_state_from_sd_file(path_to_puzzle: str) -> ndarray:
        if path_to_puzzle[-3:] != ".sd":
            raise NotSudokuFile(path_to_puzzle)
        return loadtxt(path_to_puzzle, dtype=int)

    #######################################################################################################
    # dunders
    #######################################################################################################
    def __init__(self, path_to_puzzle: str, max_attempts: int = 10000) -> None:
        self.path_to_puzzle = path_to_puzzle
        self.X: ndarray = __class__.load_game_state_from_sd_file(
            path_to_puzzle)
        self.calc_D()
        self.attempt = 0
        self.max_attempts = max_attempts

    #######################################################################################################
    # setters
    #######################################################################################################
    def increment_attempt(self) -> None:
        self.attempt += 1
        if self.attempt == self.max_attempts:
            raise MaxAtteptsReached(self.max_attempts)

    #######################################################################################################
    # get indicies
    #######################################################################################################

    def get_all_indicies_that_are_num(self, num: int) -> tuple:
        return argwhere(self.X == num)

    def get_first_blank(self) -> tuple[int, int]:
        blanks = self.get_all_indicies_that_are_num(0)
        if len(blanks) == 0:
            raise NoBlanks
        return blanks[0]

    @staticmethod
    def get_section_corner_coordinates(row: int, col: int) -> tuple[int, int]:
        return row - row % 3, col - col % 3

    def get_section(self, row: int, col: int) -> ndarray:
        i, j = __class__.get_section_corner_coordinates(row, col)
        return self.X[i:i+3, j:j+3]

    #######################################################################################################
    # check valid moves
    #######################################################################################################

    def is_num_in_row(self, num: int, row: int) -> bool:
        return num in self.X[row]

    def is_num_in_col(self, num: int, col: int) -> bool:
        return num in self.X[:, col]

    def is_num_in_section(self, num: int, row: int, col: int) -> bool:
        return num in self.get_section(row, col)

    def is_safe_to_insert(self, num: int, row: int, col: int) -> bool:
        return not self.is_num_in_row(num, row) \
            and not self.is_num_in_col(num, col) \
            and not self.is_num_in_section(num, row, col)

    #######################################################################################################
    # calculations
    #######################################################################################################
    def calc_D(self) -> None:
        # this might be easy to uderstand, but is inssuffecient for run time.
        # if we have to run this on each insert and remove, then we will greatly
        # slow our algorithm by adding an O(n^3) operation
        self.D = full((9, 9, 9), False)
        for i in range(9):
            for j in range(9):
                for k in range(9):
                    self.D[i][j][k] = self.is_safe_to_insert(k+1, i, j)

    def update_D(self, num: int, row: int, col: int, tf) -> None:
        """on insertion of a num into X at row col, how do the domains change?"""
        for i in range(9):
            if self.X[i][col] == 0:
                self.D[i][col][num-1] = tf
            if self.X[row][i] == 0:
                self.D[row][i][num-1] = tf
        for i in range(3):
            a = row - row % 3 + i
            for j in range(3):
                b = col - col % 3 + j
                if(self.X[a][b] == 0):
                    self.D[a][b][num-1] = tf

    def is_viable(self):
        for i in range(9):
            for j in range(9):
                if self.X[i][j] == 0 and (self.D[i][j] == False).all():
                    return False
        return True

    def insert_D(self, num: int, row: int, col: int) -> None:
        self.update_D(num, row, col, False)

    def remove_D(self, num: int, row: int, col: int) -> None:
        self.update_D(num, row, col, True)

    def insert(self, num: int, row: int, col: int, use_domains: bool = False) -> None:
        if not self.is_safe_to_insert(num, row, col):
            raise InvalidInsert
        self.X[row][col] = num
        if use_domains:
            self.insert_D(num, row, col)
            if not self.is_viable():
                self.remove(row, col)
                raise InvalidInsert

    def remove(self, row: int, col: int, use_domains: bool = False) -> None:
        num = self.X[row][col]
        if num == 0:
            raise CantRemoveFromBlank
        self.X[row][col] = 0
        if use_domains:
            self.remove_D(num, row, col)

    #######################################################################################################
    # the backtrcking algorithm
    #######################################################################################################

    def back_tracking_attempt(self, forward_checking: bool = False) -> ndarray:
        self.increment_attempt()

        try:
            row, col = self.get_first_blank()  # will raise NoBlanks if puzzle is solved!
        except NoBlanks:
            # by design, if we give puzzle from the state that is valid,
            # and we reach this section of the code, then we know the puzzle
            # is solved, but really, we should check if the puzzle is valid
            # NOTE: we only need to do this check in the case that teh puzzle
            # is alreday solved when we supply it to NBTA.
            return self.X

        for num in range(1, 10):
            # the case where next_puzzle is computed, meaning that it is
            # possible to insert k into X[i][j], so we should try this
            # and recursivly call backtracking on it
            try:
                self.insert(num, row, col, forward_checking)
                res = self.back_tracking_attempt(forward_checking)
                if isinstance(res, ndarray):
                    return res

            except NoBlanks:
                # by design, if we give puzzle from the state that is valid,
                # and we reach this section of the code, then we know the puzzle
                # is solved, but really, we should check if the puzzle is valid
                return self.X

            except InvalidInsert:
                # if the result puzzle is in valid, move on and try num+1
                pass

            except PuzzleUnsolvable:
                # if our current puzzle is unsolvable, but we have more to
                # numbers to chekc continue
                self.remove(row, col, forward_checking)

        # we checked all the numbers for a given spot, and they did not fit
        # for the puzzle, so need to raise puzzle unsolved
        raise PuzzleUnsolvable

    def back_tracking(self, heuristic: BackTrackingHeuristics = BackTrackingHeuristics.NAIVE) -> tuple[ndarray, int]:
        self.attempt = 0
        return self.back_tracking_attempt(forward_checking=heuristic != BackTrackingHeuristics.NAIVE), self.attempt
