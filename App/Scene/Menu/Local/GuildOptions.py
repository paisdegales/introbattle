from App.Object.CharacterImage import create_all_hero_images
from App.Object.Grid import Grid
from App.Object.Object import SizedObject
from App.Object.Selector import DefaultSelector
from App.Scene.Menu.Local.HeroPortrait import HeroPortrait

class GuildOptions(SizedObject):
    def __init__(self, position: tuple[int, int]):
        self.grid = Grid(2, 3, (150, 100))
        self.grid.move("topleft", position)
        self.grid.coordinates[1][2] = None
        self.grid.shift((50, 0), 1, None)

        self.heros = create_all_hero_images()
        self.portraits = list()
        for hero, position in zip(self.heros, self.grid.get_positions("midtop")):
            h = HeroPortrait(hero.name)
            h.move("midtop", position)
            self.portraits.append(h)
            # setattr(self, hero.name.lower(), h)

        self.selector = DefaultSelector(self.grid, (0, -8))
        self.selector.select("midtop")

        w, h = self.portraits[2].rect.right, self.portraits[3].rect.bottom
        super().__init__("guild options", (w, h))
        for portrait in self.portraits:
            portrait.draw(self.image)
        self.selector.draw(self.image)
