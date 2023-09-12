from App.Object.Selector import DefaultSelector

class CharacterSelector(DefaultSelector):
    def __init__(self, anchors: dict[str, tuple[int, int]], displacement: tuple[int, int]):
        super().__init__(anchors, displacement)


    def up(self) -> None:
        self.current -= 1
        self.current %= self.max
        self.move_index(self.current)


    def down(self) -> None:
        self.current += 1
        self.current %= self.max
        self.move_index(self.current)
