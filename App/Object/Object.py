from pygame.surface import Surface
from pygame.rect import Rect
from pygame.draw import line
from pygame.color import Color
from pygame.display import update
from logging import warning

class UndefinedScreen(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class OutOfBoundary(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class Object(Surface):
    def __init__(self, *args, surface: Surface = None):
        if surface is None:
            super().__init__(*args)
        else:
            super().__init__(surface.get_size(), surface.get_flags(), surface)
            self.blit(surface, (0, 0))
        self.rect = Rect((0,0), self.get_size())
        self.drawn = False
        self.screen = None
        self.addons = dict()

    @property
    def screen(self):
        if self._screen is None:
            raise UndefinedScreen("The object is missing its drawing surface!")
        return self._screen

    @screen.setter
    def screen(self, screen: Surface | None):
        """Defines which surface the Object is gonna be drawn to"""
        self._screen = screen

    def move(self, vertex: str, coordinates: tuple[int, int]) -> None:
        """Moves a certain vertex of the Object to a given coordinate"""
        setattr(self.rect, vertex, coordinates)

    def fits(self) -> bool:
        """Checks if the Object can be drawn to its drawing surface in its current position"""
        return self.screen.get_rect().contains(self.rect)

    def draw(self) -> None:
        if not self.fits():
            raise OutOfBoundary("The object cannot be drawn because it's exceeds the surface's limits", self.rect, self.screen.get_rect())
            
        self.drawn = True
        self._eraser = self.copy()
        self._eraser.blit(self.screen, (0, 0), self.rect)
        self.drawn_area = self.screen.blit(self, self.rect)
        update(self.drawn_area)

    def erase(self) -> None:
        if not hasattr(self, "_eraser"):
            warning("Object cannot be erased before being drawn!")
            return 
        self.drawn = False
        self.screen.blit(self._eraser, self.drawn_area)
        update(self.drawn_area)

    def toggle(self) -> None:
        if self.drawn:
            self.erase()
        else:
            self.draw()

    def make_contour(self, color: Color, thickness: int) -> None:
        line(self, color, self.get_rect().bottomleft, self.get_rect().topleft, width=thickness)
        line(self, color, self.get_rect().topleft, self.get_rect().topright, width=thickness)
        line(self, color, self.get_rect().topright, self.get_rect().bottomright, width=thickness+2)
        line(self, color, self.get_rect().bottomright, self.get_rect().bottomleft, width=thickness+2)

    def add(self, ref: str, vertex: str, *args) -> None:
        surf, coords, area = args
        obj = Object(surface=surf)
        obj.screen = self
        obj.move(vertex, coords)
        self.addons[ref] = obj
        obj.draw()
        self.draw()

    def remove(self, ref: str) -> None:
        self.addons[ref].erase()
        self.draw()

    def toggle_addon(self, ref: str) -> None:
        if self.addons[ref].drawn:
            self.addons[ref].erase()
        else:
            self.addons[ref].draw()
