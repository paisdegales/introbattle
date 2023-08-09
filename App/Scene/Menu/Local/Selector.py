from App.Object.UserInterfaceImage import ArrowImage
from logging import warning

class Selector(ArrowImage):
    def __init__(self, anchors: dict[str, tuple[int, int]], displacement: tuple[int, int]):
        super().__init__()
        self.alias = "Select indicator"
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
        if self.current >= 0 and self.current < 3:
            pass
        elif self.current == 3:
            self.current = 0
        else:
            self.current = 1
        self.move_index(self.current)


    def down(self) -> None:
        if self.current >= 3 and self.current < self.max:
            pass
        elif self.current == 2:
            self.current = 4
        elif self.current == 1:
            self.current = 3
        else:
            self.current = 3
        self.move_index(self.current)
