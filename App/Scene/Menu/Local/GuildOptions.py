from App.Object.CharacterImage import create_all_hero_images
from App.Object.Grid import Grid
from App.Object.Object import Object
from App.Scene.Menu.Local.HeroPortrait import HeroPortrait, HEROPORTRAIT_IMAGESIZE
from pygame.surface import Surface

class GuildOptions(Object):
    def __init__(self):
        self.heros = create_all_hero_images()
        self.portraits: dict[str, HeroPortrait] = dict()
        for hero in self.heros:
            portrait = HeroPortrait(hero.name, "OpenSans")
            self.portraits[hero.name] = portrait


    def draw(self, screen: Surface, topleft: tuple[int, int]) -> None:
        w, h = HEROPORTRAIT_IMAGESIZE
        initial_pos = topleft
        spacing = 2*w, 1.5*h
        lines_columns = 2, 3
        line_displacement = (w, 0)
        grid = Grid(initial_pos, spacing, lines_columns) 
        coords = grid.coordinates()
        coords = grid.shift(coords, line_displacement, line_index=1)
        for coords, portrait in zip(coords, self.portraits.values()):
            portrait.move("topleft", coords)
            portrait.camouflage = True
            portrait.draw(screen=screen, info="drawn onto the screen")
        self.highlight_text(self.heros[0].name)


    def erase(self, heroname: str | None = None) -> None:
        for portrait in self.portraits.values():
            portrait.erase()


    def get_anchors(self) -> dict[str, tuple[int, int]]:
        anchors: dict[str, tuple[int, int]] = dict()
        for heroname, portrait in self.portraits.items():
            anchors.update({heroname: portrait.rect.midtop})
        return anchors


    def highlight_text(self, heroname: str) -> None:
        self.portraits[heroname].highlight_text()
        self.portraits[heroname].draw()


    def unhighlight_text(self, heroname: str) -> None:
        self.portraits[heroname].unhighlight_text()
        self.portraits[heroname].draw()


    def __str__(self) -> str:
        string = list()
        string.append("Guild Options wrapper object")
        for portrait in self.portraits.values():
            string.append(portrait.__str__())
        string = "\n\t".join(string)
        return string
