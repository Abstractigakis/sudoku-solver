class MaxAtteptsReached(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class ImpossiblePuzzle(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
