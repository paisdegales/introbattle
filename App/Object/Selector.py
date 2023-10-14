from App.Object.Grid import Grid
from App.Object.Object import BaseObject
from App.Object.UserInterfaceImage import ArrowImage
from pygame.rect import Rect
from pygame.surface import Surface
from collections.abc import Iterable


class Selector(BaseObject):
    def __init__(self, name: str, surface: Surface, grid: Grid, displacement: tuple[int, int]):
        super().__init__(name, surface=surface)
        self.grid = grid
        self.line = 0
        self.column = 0
        self.displacement = displacement
        self.last_action = 'l'
        self.tip = "midbottom" # controls the vertex of the selector which points to smth
        self.links: list[list[object]] = list()
        for i in range(self.grid.number_lines):
            self.links.append(list())
        self.jump()


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


    def link(self, objects: Iterable) -> None:
        """ Link each square of the grid to an object

            If an object is linked to a square,
            it's implied that the selector points to
            both the square and the linked object"""

        for i in range(self.grid.number_lines):
            self.links[i].clear()


        for index, obj in enumerate(objects):
            i = index // self.grid.number_columns
            self.links[i].append(obj)


    def jump(self, vertex: str = "topleft") -> None:
        """ Moves the selector inside its grid after calls to 'right', 'left', 'up', 'down' were made
            The selector 'jumps' to the position where it should be.
            
            Parameters:
                vertex: the rectangle's vertex that should be pointed by this selector

            Return: object
                The object referenced by the selector (or None, in case nothing's referenced) """

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
        coordinates: tuple[int, int] = getattr(rect, vertex)
        self.move(self.tip, coordinates)
        self.shift(*self.displacement)


    def redraw_upon_movement(self, direction: str, vertex: str = "midtop") -> tuple[Rect]:
        """ Wrapper method to move the selector one grid square and redraw it right away

            Return: the (relative) areas that have changed on the surface where the selector is drawn """

        if not self.drawn:
            return (Rect(0, 0, 0, 0))

        surface: Surface = self.surface
        erased = self.erase()
        if direction == "left":
            self.left()
        elif direction == "right":
            self.right()
        elif direction == "up":
            self.up()
        elif direction == "down":
            self.down()
        self.jump(vertex=vertex)
        _, redrawn = self.draw(surface)
        return erased, redrawn


    def select(self) -> object:
        """ Parameters:

            Return: object
                The object referenced by the selector (or None, in case nothing's referenced) """

        obj = None
        if len(self.links[self.line]) > self.column:
            obj = self.links[self.line][self.column]

        return obj



class DefaultSelector(Selector):
    def __init__(self, grid: Grid, displacement: tuple[int, int]):
        super().__init__("default selector", ArrowImage().image, grid, displacement)
