from numpy import loadtxt, ndarray


class SudokuPuzzleSolver:
    """Loads a numpy representation of a sudoku puzzle, and has methods that can be solve via the backtrace A algorithm with some optimizations
    """

    def __init__(self, path_to_puzzle: str) -> None:
        """initalizes object instacne with a filepath to sudoku problem

        Args:
            path_to_puzzle (str): this file type must be .sd
        """
        self.puzzle: ndarray = loadtxt(path_to_puzzle, dtype=int)

    def __repr__(self) -> str:
        """the print method

        Returns:
            str: prints the puzzle
        """
        return str(self.puzzle)

    def __str__(self) -> str:
        """the str method

        Returns:
            str: returns string of the puzzle
        """
        return str(self.puzzle)


if __name__ == "__main__":
    sps = SudokuPuzzleSolver("../sudoku_problems/1/1.sd")
    print(sps)
