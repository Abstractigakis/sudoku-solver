from numpy import loadtxt, ndarray


def get_puzzle(puzzle_path: str) -> ndarray:
    """Loads a sudoku puzzle from a file

    Args:
        puzzle_path (string): path to a .sd filename

    Returns:
        ndarray: a sudoku puzzle
    """
    return loadtxt(puzzle_path, dtype=int)


if __name__ == '__main__':
    p = get_puzzle("../sudoku_problems/1/1.sd")
    print(type(p))
