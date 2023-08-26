# from App.Object.UserInterfaceImage import ArrowImage
# from App.Object.Selector import Selector
from App.Object.Selector import DefaultSelector
from pygame.transform import rotate

class OptionsSelector(DefaultSelector):
    def __init__(self, anchors: dict[str, tuple[int, int]], displacement: tuple[int, int]):
        super().__init__(anchors, displacement)
        self.rotate(-270)


    def left(self) -> None:
        self.current -= 1
        self.current %= self.max
        self.move_index(self.current)


    def right(self) -> None:
        self.current += 1
        self.current %= self.max
        self.move_index(self.current)
