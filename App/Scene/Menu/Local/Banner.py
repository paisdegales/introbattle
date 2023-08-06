from App.Font.Family import FontFamily
from App.Object.Object import Object
from App.Setup.Globals import BLACK, WHITE
from pygame.surface import Surface

class Banner(Object):
    def __init__(self, family_name: str, screen: Surface):
        self.font = FontFamily(family_name)
        self.canvas = screen
    
    def load(self, text: str, size: tuple[int, int] | None = None, vertex: str = "topleft", coordinates: tuple[int, int] = (0,0)) -> None:
        surface = self.font.render("BoldItalic", text, 40, WHITE, BLACK)
        if size is None:
            super().__init__(surface=surface)
            self.screen = self.canvas
        else:
            super().__init__(size, surface.get_flags(), surface.get_bitsize())
            self.screen = self.canvas
            self.add("title", vertex, surface, coordinates, None)
        self.make_contour(WHITE, 3)
