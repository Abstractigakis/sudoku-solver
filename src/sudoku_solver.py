from numpy import array, ndarray, loadtxt, argwhere, vectorize, fromfunction, count_nonzero

from src.exceptions import InvalidInsert, MaxAtteptsReached, NoBlanks, PuzzleUnsolvable, NotSudokuFile, CantRemoveFromBlank


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
    def __init__(self, path_to_puzzle: str) -> None:
        self.path_to_puzzle = path_to_puzzle
        self.X_0: ndarray = __class__.load_game_state_from_sd_file(
            path_to_puzzle)
        self.D_0: ndarray = __class__.calc_D(X=self.X_0)
        self.attempt = 0

    #######################################################################################################
    # setters
    #######################################################################################################
    def increment_attempt(self, max_attempts: int) -> None:
        self.attempt += 1
        if self.attempt == max_attempts:
            raise MaxAtteptsReached(max_attempts)

    #######################################################################################################
    # get indicies
    #######################################################################################################

    @staticmethod
    def get_all_indicies_that_are_num(X: ndarray, num: int) -> tuple:
        return argwhere(X == num)

    @staticmethod
    def get_first_blank(X: ndarray) -> tuple[int, int]:
        blanks = __class__.get_all_indicies_that_are_num(X, 0)
        if len(blanks) == 0:
            raise NoBlanks
        return blanks[0]

    @staticmethod
    def get_section_corner_coordinates(row: int, col: int) -> tuple[int, int]:
        return row - row % 3, col - col % 3

    @staticmethod
    def get_section(X: ndarray, row: int, col: int) -> ndarray:
        i, j = __class__.get_section_corner_coordinates(row, col)
        return X[i:i+3, j:j+3]

    #######################################################################################################
    # check valid moves
    #######################################################################################################

    @staticmethod
    def is_num_in_row(X: ndarray, num: int, row: int) -> bool:
        return num in X[row]

    @staticmethod
    def is_num_in_col(X: ndarray, num: int, col: int) -> bool:
        return num in X[:, col]

    @staticmethod
    def is_num_in_section(X: ndarray, num: int, row: int, col: int) -> bool:
        return num in __class__.get_section(X, row, col)

    @staticmethod
    def is_safe_to_insert(X: ndarray, num: int, row: int, col: int) -> bool:
        return not __class__.is_num_in_row(X, num, row) \
            and not __class__.is_num_in_col(X, num, col) \
            and not __class__.is_num_in_section(X, num, row, col)

    #######################################################################################################
    # calculations
    #######################################################################################################
    @staticmethod
    def calc_D_ll(X: ndarray) -> ndarray:
        """set the domain property for the current puzzle state, which is a 3d boolean tensor where
        each i,j,k entry is true, if the number k-1 can be inserted into square i, j in the puzzle
        """

        # DEV NOTE: numpy's from function creates 3, 3d tensors i, j, k. the
        #  is_safe_to_insert method, is only meant to work for one entry, not
        #  to handle the full tensors.  We also dont want to iterate beacuse
        #  its slow.  So use vecttorize.
        #
        #  NOTE we dont want to vectorize the puzzle.

        # this can be called on each game state on creation, but this is an
        # expensive operation.  better to only use domains ad-hoc

        vfunc = vectorize(__class__.is_safe_to_insert, excluded={"X"})
        return fromfunction(
            lambda i, j, k: vfunc(X, num=k+1, row=i, col=j), (9, 9, 9), dtype=int)

    @staticmethod
    def calc_D(X: ndarray) -> ndarray:
        D = []
        for i in range(9):
            a = []
            for j in range(9):
                b = []
                for k in range(9):
                    b.append(__class__.is_safe_to_insert(X, k+1, i, j))
                a.append(b)
            D.append(a)
        return array(D)

    @staticmethod
    def forward_checking(X: ndarray, D: ndarray, row: int, col: int, num: int, tf) -> ndarray:
        """on insertion of a num into X at row col, how do the domains change?"""
        for i in range(9):
            if (X[i][col] == 0):
                D[i][col][num-1] = tf
            if (X[row][i] == 0):
                D[row][i][num-1] = tf
        for i in range(3):
            a = row - row % 3 + i
            for j in range(3):
                b = col - col % 3 + j
                if(X[a][b] == 0):
                    D[a][b][num-1] = tf
        return D

    @staticmethod
    def insert(X: ndarray, D: ndarray, num: int, row: int, col: int) -> ndarray:
        """Modifies the X, and D ndarrays, i.e. pass by reference"""
        if not __class__.is_safe_to_insert(X, num, row, col):
            raise InvalidInsert
        X[row][col] = num
        D = __class__.forward_checking(X, D, num, row, col, True)
        return X, D

    @staticmethod
    def remove(X: ndarray, D: ndarray, row: int, col: int) -> ndarray:
        """Modifies the X, and D ndarrays, i.e. pass by reference"""
        num = X[row][col]
        if num == 0:
            raise CantRemoveFromBlank
        X[row][col] = 0
        D = __class__.forward_checking(X, D, num, row, col, False)
        return X, D

    #######################################################################################################
    # naive backtracking
    #######################################################################################################

    # def naive_back_tracking_attempt(self, X: ndarray, max_attempts: int)->ndarray:
    #     self.increment_attempt(max_attempts)

    #     # will raise NoBlanks if puzzle is solved!
    #     try:
    #         row, col = __class__.get_first_blank(X)
    #     except NoBlanks:
    #         # by design, if we give puzzle from the state that is valid,
    #         # and we reach this section of the code, then we know the puzzle
    #         # is solved, but really, we should check if the puzzle is valid
    #         return X

    #     for num in range(1, 10):
    #         # the case where next_puzzle is computed, meaning that it is
    #         # possible to insert k into X[i][j], so we should try this
    #         # and recursivly call backtracking on it
    #         try:
    #             next_game_state = game_state.next_game_state(num, row, col)
    #             reuslt_game_state = self.naive_back_tracking_attempt(
    #                 next_game_state, max_attempts)
    #             if isinstance(reuslt_game_state, SudokuGameState):
    #                 return reuslt_game_state

    #         except NoBlanks:
    #             # by design, if we give puzzle from the state that is valid,
    #             # and we reach this section of the code, then we know the puzzle
    #             # is solved, but really, we should check if the puzzle is valid
    #             return game_state

    #         except InvalidSudokuGameState:
    #             # if the result puzzle is in valid, move on and try num+1
    #             pass
    #         except PuzzleUnsolvable:
    #             # if our current puzzle is unsolvable, but we have more to
    #             # numbers to chekc continue
    #             pass

    #     # we checked all the numbers for a given spot, and they did not fit
    #     # for the puzzle, so need to raise puzzle unsolved
    #     raise PuzzleUnsolvable

    def naive_back_tracking(self, max_attempts: int = 10000) -> tuple[ndarray, int]:
        self.attempt = 0
        return self.naive_back_tracking_attempt(self.X_0, max_attempts), self.attempt

    # #######################################################################################################
    # # backtracking with forward checking
    # #######################################################################################################
    # def reset_back_tracking_with_forward_checking_attempt_number(self):
    #     self.back_tracking_with_forward_checking_attempt_number = 0

    # def increment_back_tracking_with_forward_checking_attempt_number(self, max_attempts: int) -> None:
    #     self.back_tracking_with_forward_checking_attempt_number += 1
    #     if self.back_tracking_with_forward_checking_attempt_number == max_attempts:
    #         raise MaxAtteptsReached(max_attempts)

    # def back_tracking_with_forward_checking_attempt(self, game_state: SudokuGameState, max_attempts: int):
    #     self.increment_back_tracking_with_forward_checking_attempt_number(
    #         max_attempts)

    #     # will raise NoBlanks if puzzle is solved!
    #     try:
    #         row, col = game_state.get_first_blank()
    #     except NoBlanks:
    #         # by design, if we give puzzle from the state that is valid,
    #         # and we reach this section of the code, then we know the puzzle
    #         # is solved, but really, we should check if the puzzle is valid
    #         return game_state

    #     for num in range(1, 10):
    #         # the case where next_puzzle is computed, meaning that it is
    #         # possible to insert k into X[i][j], so we should try this
    #         # and recursivly call backtracking on it
    #         try:
    #             next_game_state = game_state.next_game_state(num, row, col)
    #             if next_game_state.is_impossible:
    #                 reuslt_game_state = self.back_tracking_with_forward_checking_attempt(
    #                     next_game_state, max_attempts)
    #                 if isinstance(reuslt_game_state, SudokuGameState):
    #                     return reuslt_game_state

    #         except NoBlanks:
    #             # by design, if we give puzzle from the state that is valid,
    #             # and we reach this section of the code, then we know the puzzle
    #             # is solved, but really, we should check if the puzzle is valid
    #             return game_state

    #         except InvalidSudokuGameState:
    #             # if the result puzzle is in valid, move on and try num+1
    #             pass
    #         except PuzzleUnsolvable:
    #             # if our current puzzle is unsolvable, but we have more to
    #             # numbers to chekc continue
    #             pass

    #     # we checked all the numbers for a given spot, and they did not fit
    #     # for the puzzle, so need to raise puzzle unsolved
    #     raise PuzzleUnsolvable

    # def back_tracking_with_forward_checking(self, max_attempts: int = 10000) -> tuple[SudokuGameState, int]:
    #     self.reset_back_tracking_with_forward_checking_attempt_number()
    #     return self.back_tracking_with_forward_checking_attempt(
    #         self.intial_game_state, max_attempts), self.back_tracking_with_forward_checking_attempt_number
