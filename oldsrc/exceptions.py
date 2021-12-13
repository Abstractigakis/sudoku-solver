class MaxAtteptsReached(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class ImpossiblePuzzle(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidSudokuGameState(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class NoBlanks(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class PuzzleUnsolvable(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
