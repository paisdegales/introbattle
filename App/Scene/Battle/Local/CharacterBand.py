from pygame.rect import Rect
from App.Object.Fighter import Fighter, create_guild
from App.Object.Grid import Grid
from App.Object.Object import SizedObject
from App.Object.Selector import DefaultSelector


class CharacterBand(SizedObject):
    def __init__(self, name: str, characters: list[str], grid: Grid):
        super().__init__(name, (grid.w, grid.h))
        self.hide = True
        self.grid = grid
        self.fighters = create_guild(characters)
        self.selector = DefaultSelector(self.grid, (0, 0))
        self.selector.jump("midtop")
        for fighter, position in zip(self.fighters, self.grid.get_positions("midtop")):
            fighter.move("midtop", position)
            fighter.draw(self.image)
        self.selector.draw(self.image)
        self.selector.link(self.fighters)


    def go(self, direction: str) -> list[Rect]:
        """ move the selector up, down, left or right

            this method erases the selector off self's surface and redraws it
            in a different position.

            the modified areas use coordinates that are relative to the topleft
            vertex of the self's surface

            Parameters:
                direction: the direction the selector should follow ('up', 'down', 'left', 'right')

            Return: List[Rect]
                1. list[0] = the erased area
                1. list[1] = the drawn area """

        return list(self.selector.redraw_upon_movement(direction))

    
    def select(self) -> Fighter:
        return self.selector.select()


class HeroBand(CharacterBand):
    def __init__(self, heros: list[str]):
        if len(heros) != 3:
            return
        grid = Grid(3, 1, (100, 120))
        grid.move("topleft", (0, 10))
        grid.shift((50, 0), line_index=1)
        super().__init__("Hero band", heros, grid)


class EnemyBand(CharacterBand):
    def __init__(self, enemies: list[str]):
        grid = Grid(3, 1, (100, 120))
        grid.move("topleft", (0, 10))
        grid.shift((50, 0), line_index=0)
        grid.shift((50, 0), line_index=2)
        super().__init__("Enemy band", enemies, grid)
