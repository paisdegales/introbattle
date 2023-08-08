from App.Object.UserInterfaceImage import ArrowImage
from logging import warning

class Selector(ArrowImage):
    def __init__(self, anchors: dict[str, tuple[int, int]], displacement: tuple[int, int]):
        super().__init__()
        self.anchors: dict[str, tuple[int, int]] = anchors
        self.mnemonic: dict[int, str] = dict()
        for index, k in enumerate(self.anchors.keys()):
            self.anchors[k] = (self.anchors[k][0] + displacement[0], self.anchors[k][1] + displacement[1])
            self.mnemonic[index] = k
        self.current = 0
        self.max = len(self.mnemonic.keys())
        self.move_index(0)


    def get_current_ref(self) -> str:
        return self.anchors[self.mnemonic[self.current]]


    def move_index(self, index: int) -> None:
        self.move(self.mnemonic[index])


    def move(self, anchor: str) -> None:
        if anchor not in self.anchors.keys():
            warning("Error when moving selector!")
            return
        self.rect.midbottom = self.anchors[anchor]


    def right(self) -> None:
        self.current += 1
        self.current %= self.max
        self.move_index(self.current)


    def left(self) -> None:
        self.current -= 1
        self.current %= self.max
        self.move_index(self.current)


    def up(self) -> None:
        self.current += 2
        self.current %= self.max
        self.move_index(self.current)


    def down(self) -> None:
        self.current -= 2
        self.current %= self.max
        self.move_index(self.current)
