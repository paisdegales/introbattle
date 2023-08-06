from pygame import QUIT, MOUSEBUTTONDOWN
from pygame.mouse import get_pos
from enum import Enum

class GameEvent:
    def __init__(self, key: int) -> None:
        self.key = key

    def action(self) -> int:
        raise NotImplementedError()

class CloseGame(GameEvent):
    def __init__(self) -> None:
        super().__init__(QUIT)
    
    def action(self) -> int:
        exit()

class GetCursorPosition(GameEvent):
    def __init__(self) -> None:
        super().__init__(MOUSEBUTTONDOWN)
    
    def action(self) -> int:
        x, y = get_pos()
        print(f"X: {x}, Y: {y}")
