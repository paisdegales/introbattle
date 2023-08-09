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
            """
            after setting the screen and positioning each portrait, they still
            have to be updated. Why?  this is because each portrait initially
            has a black background, because of the way the Surface() method
            works. So in order to sync the portrait's background with the
            scene's background, we have to update every portrait's surface with
            the screen's background. If this was not done, then the text of
            each portrait would have a black rectangle under them and this is
            not visually delightful/appealing
            """
            portrait.update_surface(screen)
            portrait.draw()
            w, h = portrait.get_size()
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
