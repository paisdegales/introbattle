from pygame.surface import Surface
from pygame.rect import Rect
from pygame.draw import line
from pygame.color import Color
from pygame.display import update
from pygame.transform import scale_by, flip
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
            super().__init__(surface.get_size(), surface.get_flags(), surface.get_bitsize())
            self.blit(surface, (0, 0))
        self.rect = Rect((0,0), self.get_size())
        self.drawn = False
        self.screen = None
        self.addons = dict()
        self.alias = "Unnamed"
        self._eraser: list[Surface] = list()


    @property
    def screen(self):
        if self._screen is None:
            raise UndefinedScreen("The object is missing its drawing surface!")
        return self._screen


    @screen.setter
    def screen(self, screen: Surface | None):
        """ Defines which surface the Object is gonna be drawn to

            Be aware: this property does not keep track of all the changes the
            'screen' argument might go through after this method terminates.
            Prefer to only set the screen to be drawn when the object is about
            to call the 'draw' method. Otherwise the code might be
            error-bug-prone and calls to the 'erase' method might not work
            properly/as expected.

            Known bug: the '_screen_bak' attr might get overriden with
            sucessive calls to the 'draw' method. This is not the expected
            behavior, since this could lead to an ineffective 'erase' method
            call. The reason for this, is that if the '_screen_bak' attr gets
            updated after the Object is already drawn, then it will actually be
            a copy of the Object it self before the update!  In this sense, the
            '_screen_bak' attr should only be set once, or the drawing process
            could be better designed to ensure that '_screen_bak' only changes
            when the screen passed is actually a **different** screen
        """
        self._screen = screen
        if screen is not None:
            self._screen_bak = screen.copy()
            self._screen_bak.blit(screen, (0, 0))
        else:
            self._screen_bak = None


    def move(self, vertex: str, coordinates: tuple[int, int]) -> None:
        """Moves a certain vertex of the Object to a given coordinate on the screen where it'll be drawn"""
        setattr(self.rect, vertex, coordinates)


    def fits(self) -> bool:
        """Checks if the Object can be drawn to its drawing surface in its current position"""
        return self.screen.get_rect().contains(self.rect)


    def draw(self, screen: Surface | None = None, transparent: bool = False) -> None:
        # if a screen to be drawn to is passed, then use it. Otherwise, try to use the
        # existing one (which **might** be stored in self.screen). If no screen was set
        # up until this moment, then an Exception is going to be thrown;
        if screen is not None:
            self.screen = screen

        if not self.fits():
            raise OutOfBoundary("The object cannot be drawn because it's exceeds the surface's limits", self.rect, self.screen.get_rect())

        self.drawn = True
        # the eraser stores what will be beneath the Object after it gets drawn.
        # to create the eraser, first we need to store what's currently on the
        # position where the Object will be drawn. Notice that the screen's surface
        # is not used by itself, because this screen could get dirty as more and more
        # things are drawn into it. Instead, it's used a backup screen surface, which
        # is an identical copy of the screen's surface once it was bounded to this object.
        beneath_surface = self.copy()
        beneath_surface.blit(self._screen_bak, (0, 0), self.rect)
        self._eraser.append(beneath_surface)

        # setting this object to become transparent basically means that it should
        # have the same texture as its underlying surface. Since the eraser stores
        # exactly what's under the image, we can use it to camouflage the Object's surface
        # among its background.
        if transparent:
            self.blit(beneath_surface, (0, 0))

        # all surface's addons are attached first
        self.draw_addons()

        # the final surface gets now drawn onto the screen
        self.drawn_area = self.screen.blit(self, self.rect)
        update(self.drawn_area)


    def draw_addons(self) -> None:
        for addon in self.addons.values():
            addon.draw(screen=self)


    def erase(self) -> None:
        if not self.drawn:
            return
        self.drawn = False
        beneath_surface = self._eraser.pop()
        self.screen.blit(beneath_surface, self.drawn_area)
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
        obj.alias = ref
        # notice that the 'screen' attribute of the just created obj was not set here,
        # but it's later defined when the 'draw_addons' method gets called. Why is that?
        # The reason for this is that the parental object (whose addons belong to) might
        # not be ready to be drawn onto the screen just yet as new addons get added.
        # To work this around, the 'screen' attribute is only set when the objects need
        # to be drawn. This also makes sense, since there's no point for rushing and setting
        # the addons' surfaces just yet.
        obj.move(vertex, coords)
        self.addons[ref] = obj


    def remove(self, ref: str, pop: bool = False, force_update: bool = False) -> None:
        self.addons[ref].erase()
        if pop:
            self.addons.pop(ref)
        if force_update:
            self.draw(self.screen)


    def toggle_addon(self, ref: str) -> None:
        if self.addons[ref].drawn:
            # self.addons[ref].erase()
            addon = self.addons[ref]
            # since the 'draw' method draws all addons of the object, we need to
            # remove the addon first, so that the 'draw' method does not repaint it right after.
            # the 'draw' method for the 'addon' itself does not update the screen, since its
            # screen is the object's surface, not the actual screen
            self.remove(ref, pop=True, force_update=True)
            self.draw()
            self.add(ref, "topleft", addon.to_surface(), addon.rect.topleft, None)
        else:
            self.addons[ref].draw()


    def to_surface(self) -> Surface:
        surface = Surface(self.get_size(), self.get_flags(), self.get_bitsize())
        surface.blit(self, (0, 0))
        return surface


    @property
    def alias(self) -> str:
        return self.__alias


    @alias.setter
    def alias(self, alias: str) -> None:
        self.__alias = alias


    def __str__(self) -> str:
        return "{} object, placed inside {} surface, 'topleft' vertex at {}, currently drawn: {}, addons: {}".format(self.alias, self.screen.get_size(), self.rect.topleft, "yes" if self.drawn else "no", self.addons.keys())


    def update_surface(self, surface: Surface) -> None:
        self.erase()
        self.blit(surface, (0, 0), self.rect)
        self.draw_addons()
