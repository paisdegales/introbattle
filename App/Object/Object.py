from pygame.surface import Surface
from pygame.rect import Rect
from pygame.draw import line
from pygame.color import Color
from pygame.transform import scale_by, flip, rotate
from pygame.image import load

class BaseObject:
    """
        brief summary of all Object's attributes:

        self.name: str
            This is the name to identify this instance of Object when printing it

        self.image: pygame.surface.Surface
            This is the surface which contains what will be drawn onto the screen

        self.rect: pygame.rect.Rect
            This rectangle serves the purpose of positioning the Object's surface.
            The coordinates are relative to the 'screen' attr
            It has the same size as the surface itself.

        self.hide: bool
            This flag indicates if the Object should have the same background as its screen when it gets drawn onto it.
    """

    def __init__(self, name: str, surface: Surface):
        self.name = name
        self.image = surface
        self.rect: Rect = Rect((0, 0), surface.get_size())
        self.hide = False
        self.drawn = False


    def __str__(self) -> str:
        string = [f"name: {self.name}", f"topleft (rel. coords.): {self.rect.topleft}", f"size: {self.rect.size}"]
        return "\n".join(string)


    def shift(self, dx: int, dy: int) -> None:
        x, y = self.rect.topleft
        self.rect.topleft = x + dx, y + dy


    def move(self, vertex: str, coordinates: tuple[int, int]) -> None:
        setattr(self.rect, vertex, coordinates)


    def draw(self, surface: Surface) -> tuple[Surface, Rect]:
        if self.drawn:
            raise Exception(f"{self.name} can't be drawn again")
        beneath = self.image.copy()
        beneath.blit(surface, (0, 0), self.rect)
        area = surface.blit(self.image, self.rect.topleft)
        self.drawn = True
        return beneath, area


    def erase(self, surface: Surface, eraser: Surface, area: Rect) -> Rect:
        """ replace an 'area' of a 'surface' with 'eraser'
            this method 'assumes' that what's being replaced/erased is this object :)
            because of this assumption, the 'drawn' attribute of this obj is set to False """

        if not self.drawn:
            raise Exception(f"{self.name} can't be erased")
        area = surface.blit(eraser, area.topleft)
        self.drawn = False
        return area


    def scale_by(self, factor: float) -> None:
        self.image = scale_by(self.image, factor)
        self.rect.update(self.rect.topleft, self.image.get_size())


    def flip(self, x_flip: bool, y_flip: bool) -> None:
        self.image = flip(self.image, x_flip, y_flip)

    
    def rotate(self, ang: int) -> None:
        self.image = rotate(self.image, ang)
        self.rect.update(self.rect.topleft, self.image.get_size())


    def make_contour(self, color: Color, thickness: int) -> None:
        line(self.image, color, self.rect.bottomleft, self.rect.topleft, width=thickness)
        line(self.image, color, self.rect.topleft, self.rect.topright, width=thickness)
        line(self.image, color, self.rect.topright, self.rect.bottomright, width=thickness+2)
        line(self.image, color, self.rect.bottomright, self.rect.bottomleft, width=thickness+2)


class SizedObject(BaseObject):
    def __init__(self, name: str, size: tuple[int, int]):
        surface = Surface(size)

        """ debugging purposes
        surf = surface.copy()
        surf.fill(Color(255, 0, 0))
        surf.blit(surface, (0, 0))
        surface = surf
        """

        super().__init__(name, surface)


class ImportedObject(BaseObject):
    def __init__(self, name: str, filename: str):
        surface = load(filename)
        min_rect = surface.get_bounding_rect()
        cropped_surface = Surface(min_rect.size, flags=surface.get_flags(), depth=surface.get_bitsize())
        cropped_surface.blit(surface, (0, 0), min_rect)

        """ debugging purposes
        surf = cropped_surface.copy()
        surf.fill(Color(255, 0, 0))
        surf.blit(cropped_surface, (0, 0))
        cropped_surface = surf
        """

        super().__init__(name, cropped_surface)
