from App.Object.Object import BaseObject
from App.Object.UserInterfaceImage import ArrowImage
from pygame.surface import Surface

class Selector(BaseObject):
    def __init__(self, name: str, surface: Surface, anchors: dict[str, tuple[int, int]], displacement: tuple[int, int]):
        super().__init__(name, surface=surface)
        self.anchors: dict[str, tuple[int, int]] = anchors
        self.mnemonic: dict[int, str] = dict()
        for index, k in enumerate(self.anchors.keys()):
            x, y = self.anchors[k] 
            self.anchors[k] = (x + displacement[0], y + displacement[1])
            self.mnemonic[index] = k
        self.current = 0
        self.max = len(self.mnemonic.keys())
        self.move_index(0)



    def get_current_ref(self) -> str:
        return self.mnemonic[self.current]


    def move_index(self, index: int) -> None:
        self.move(self.mnemonic[index])


    def move(self, anchor: str) -> None:
        if anchor not in self.anchors.keys():
            print("Error when moving selector!")
            return
        self.rect.midbottom = self.anchors[anchor]


    def right(self) -> None:
        raise NotImplementedError()


    def left(self) -> None:
        raise NotImplementedError()


    def up(self) -> None:
        raise NotImplementedError()


    def down(self) -> None:
        raise NotImplementedError()

class DefaultSelector(Selector):
    def __init__(self, anchors: dict[str, tuple[int, int]], displacement: tuple[int, int]):
        super().__init__("default selector", ArrowImage().image, anchors, displacement)
