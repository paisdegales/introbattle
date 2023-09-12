from App.Object.Grid import Grid
from App.Object.Object import BaseObject
from App.Object.UserInterfaceImage import ArrowImage
from pygame.surface import Surface

class Selector(BaseObject):
    def __init__(self, name: str, surface: Surface, grid: Grid, displacement: tuple[int, int]):
        super().__init__(name, surface=surface)
        self.grid = grid
        self.line = 0
        self.column = 0
        self.displacement = displacement
        self.last_action = 'l'
        self.tip = "midbottom" # control's the vertex of the selector which points to smth
        self.select()


    def right(self):
        self.column += 1
        self.column %= self.grid.number_columns
        self.last_action = 'r'
        return self


    def left(self):
        self.column -= 1
        self.column %= self.grid.number_columns
        self.last_action = 'l'
        return self


    def up(self):
        self.line -= 1
        self.line %= self.grid.number_lines
        self.last_action = 'u'
        return self


    def down(self):
        self.line += 1
        self.line %= self.grid.number_lines
        self.last_action = 'd'
        return self


    def select(self, vertex: str = "topleft") -> list[int]:
        rect = self.grid.coordinates[self.line][self.column]
        if rect is None:
            if self.last_action == 'l':
                movement = self.left
            elif self.last_action == 'r':
                movement = self.right
            elif self.last_action == 'u':
                movement = self.up
            else:
                movement = self.down
            moves = 3
            while moves:
                movement()
                rect = self.grid.coordinates[self.line][self.column]
                if rect is not None:
                    break
                moves -= 1
            if not moves:
                raise Exception("selector: out of anchors to jump to in this line/column")
        coordinates = list(getattr(rect, vertex))
        self.move(self.tip, tuple(coordinates))
        self.shift(*self.displacement)
        return coordinates


class DefaultSelector(Selector):
    def __init__(self, grid: Grid, displacement: tuple[int, int]):
        super().__init__("default selector", ArrowImage().image, grid, displacement)
