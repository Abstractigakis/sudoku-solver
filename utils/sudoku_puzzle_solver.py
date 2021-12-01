from numpy import loadtxt, ndarray


class SudokuPuzzleSolver:

    def __init__(self, path_to_puzzle: str) -> None:
        self.puzzle: ndarray = loadtxt(path_to_puzzle, dtype=int)

    def __repr__(self) -> str:
        return str(self.puzzle)

    def __str__(self) -> str:
        return str(self.puzzle)


if __name__ == "__main__":
    sps = SudokuPuzzleSolver("../sudoku_problems/1/1.sd")
    print(sps)
