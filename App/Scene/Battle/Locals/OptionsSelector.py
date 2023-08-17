from App.Object.UserInterfaceImage import ArrowImage
from App.Object.Selector import Selector
from pygame.transform import rotate

class OptionsSelector(Selector):
    def __init__(self, anchors: dict[str, tuple[int, int]], displacement: tuple[int, int]):
        surf = ArrowImage().to_surface()
        surf = rotate(surf, -270)
        super().__init__(surf, anchors, displacement)


    def left(self) -> None:
        if self.current in [1, 3]:
            self.current -= 1
            self.current %= self.max
            self.move_index(self.current)


    def right(self) -> None:
        if self.current in [0, 2]:
            self.current += 1
            self.current %= self.max
            self.move_index(self.current)
