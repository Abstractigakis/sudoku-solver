def get_puzzle(puzzle_path:str) -> list:
    """Loads a sudoku puzzle from a file

    Args:
        puzzle_path (string): path to a .sd filename

    Returns:
        9x9 Array: a sudoku puzzle
    """
    X = []
    with open(puzzle_path, 'r') as file:
        for _ in range(9):
            chars = file.readline().split()
            row = [int(char) for char in chars]
            X.append(row)
    return X
