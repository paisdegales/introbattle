from App.Font.Family import FontFamily
from App.Object.Object import Object
from App.Setup.Globals import BLACK, WHITE
from pygame.surface import Surface
from pygame.rect import Rect


class Banner(Object):
    def __init__(self, family_name: str, screen: Surface):
        self.font = FontFamily(family_name)
        self.canvas = screen


    def load(self, text: str, size: tuple[int, int] | None = None, vertex: str = "topleft", relative_coordinates: tuple[int, int] = (0,0)) -> None:
        surface = self.font.render("BoldItalic", text, 40, WHITE, BLACK)
        if size is None:
            super().__init__(surface=surface)
            self.screen = self.canvas
        else:
            min_size = self.font.get_render_size("BoldItalic", text, 40)
            desired_size_rect = Rect((0,0), size)
            min_size_rect = Rect((0,0), min_size)
            rect = min_size_rect.union(desired_size_rect)
            #print("min size: {}\ndesired_size_rect: {}\nselected rect: {}".format(min_size_rect, desired_size_rect, rect))
            size = rect.size
            super().__init__(size, surface.get_flags(), surface.get_bitsize())
            self.screen = self.canvas
            self.add("title", vertex, surface, relative_coordinates, None)
        self.make_contour(WHITE, 3)
