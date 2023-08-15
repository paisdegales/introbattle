from App.Object.Selector import DefaultSelector

class MenuSelector(DefaultSelector):
    def __init__(self, anchors: dict[str, tuple[int, int]], displacement: tuple[int, int]):
        super().__init__(anchors, displacement)


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
