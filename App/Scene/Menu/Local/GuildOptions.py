from App.Scene.Menu.Local.HeroPortrait import HeroPortrait
from App.Object.CharacterImage import create_all_hero_images
from pygame.surface import Surface

class GuildOptions:
    def __init__(self):
        self.heros = create_all_hero_images()
        self.portraits: dict[str, HeroPortrait] = dict()
        for hero in self.heros:
            portrait = HeroPortrait(hero.name, "OpenSans")
            self.portraits[hero.name] = portrait

    def draw(self, screen: Surface) -> None:
        init_x, init_y = 300, 300
        inter_column_spacing = 50
        inter_line_spacing = 50
        second_line_displacement = 75
        w, h = 0, 0
        per_line = 3
        max_cols = 2
        for index, portrait in enumerate(self.portraits.values()):
            quot, rem = divmod(index, per_line)
            portrait.screen = screen
            x = init_x + (w + inter_column_spacing)*rem + second_line_displacement*quot
            y = init_y + (h + inter_line_spacing)*quot
            portrait.move("topleft", (x, y))
            portrait.draw()
            w, h = portrait.get_size()

    def erase(self, heroname: str | None = None) -> None:
        for portrait in self.portraits.values():
            portrait.erase()

    def get_anchors(self) -> dict[str, tuple[int, int]]:
        anchors: dict[str, tuple[int, int]] = dict()
        for heroname, portrait in self.portraits.items():
            anchors.update({heroname: portrait.rect.midtop})
        return anchors
