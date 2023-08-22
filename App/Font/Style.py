from App.Setup.Globals import folders
from pygame.font import Font, get_init, init
from pygame.color import Color
from pygame.rect import Rect
from pygame.surface import Surface
from logging import warning

class FontStyle():
    """
        Basic interface to manage new font styles
    """
    def __init__(self, family_name: str, style_name: str, file_extension: str = ".ttf", size: int = 12) -> None:
        if get_init() == False:
            init()

        self.family_name = family_name
        self.style_name = style_name
        filename = style_name + file_extension
        self.path = folders.get_filepath(family_name, filename)
        self.size = size

    @property
    def size(self) -> int:
        return self.__size

    @size.setter
    def size(self, size: int) -> None:
        try:
            self.font = Font(self.path, size)
            self.__size = size
        except FileNotFoundError as e:
            warning(e.args)
            raise e
        except Exception as e:
            warning(e.args, type(e))
            raise e
            

    def render(self, text: str, text_color: Color, background_color: Color | None = None, area: tuple[int,int] | None = None, vertex: str = "center") -> Surface:
        surface = self.font.render(text, True, text_color, background_color)
        if area:
            # minimal dimensions needed for a surface to contain the text
            min_size = self.get_render_size(text)
            # rect: a rectangle with the desired proportions
            rect = Rect((0, 0), area)
            # min_rect: a rectangle with the minimal proportions needed to fit the text's surface
            min_rect = Rect((0, 0), min_size)
            # the 'union' method somehows returns a rectangle which covers both areas. If the desired proportions are not enough to fit the text's surface, then the rect = min_rect. Otherwise, rect = rect
            rect = min_rect.union(rect)
            # a new surface with just enough or more space is created
            new_surface = Surface(rect.size, surface.get_flags(), surface.get_bitsize())
            # the min_rect is analogous to the text's surface (since it descended from it). Therefore we can use it to later position the surface.
            # The text's vertex is aligned with its corresponding background's vertex
            setattr(min_rect, vertex, getattr(rect, vertex))
            # the text is finally blitted
            new_surface.blit(surface, min_rect.topleft)
            # the surface is ready!
            surface = new_surface
        return surface

    def get_render_size(self, text: str) -> tuple[int, int]:
        return self.font.size(text)
