from App.Font.Family import FontFamily
from App.Object.Object import Object
from App.Setup.Globals import BLACK, WHITE
from pygame.surface import Surface
from pygame.rect import Rect


class Banner(Object):
    def __init__(self, family_name: str):
        self.font = FontFamily(family_name)


    def load(self, text: str, size: tuple[int, int] | None = None, vertex: str = "center") -> None:
        if size is None:
            surface = self.font.render("BoldItalic", text, 40, WHITE, BLACK)
        else:
            surface = self.font.render("BoldItalic", text, 40, WHITE, BLACK, size, vertex)
        super().__init__(surface=surface)
        self.make_contour(WHITE, 3)
        self.alias = "Banner"
