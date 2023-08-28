from pygame.surface import Surface
from pygame.rect import Rect
from pygame.draw import line
from pygame.color import Color
from pygame.display import update
from pygame.transform import scale_by, flip, rotate


class UndefinedScreen(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class OutOfBoundary(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class Object:
    """
        brief summary of all Object's attributes:

        self.surface: pygame.surface.Surface
            This is the surface which contains what will be drawn onto the screen

        self.rect: pygame.rect.Rect
            This rectangle serves the purpose of positioning the Object's surface.
            The coordinates are relative to the 'screen' attr
            It has the same size as the surface itself.

        self.draw: bool
            This flag tells if the Object is currently drawn on the display or not

        self.screen: pygame.surface.Surface
            This is the screen on which the 'surface' attr will be drawn to

        self.addons: dict[Object]
            A addon is simply another Object, which belongs to the current Object.
            Addons are positioned relative to its parent's surface.

        self.alias: str
            This is the name to identify this instance of Object when printing it

        self.parent: Object
            another instance of Object which possesses this object

        self.drawn_area: pygame.rect.Rect
            This keeps track of the position where the surface got drawn onto the screen.

        self.beneath: pygame.pygame.Surface
            This keeps track of what was beneath the surface when it got drawn onto the screen.

        self.camouflage: bool
            This flag indicates if the Object should have the same background as its screen when it gets drawn onto it.

        self.__screen_bak: pygame.surface.Surface
            This is an identical copy of the screen as soon as it was bounded to this object.
            This copy should never be modified, as it serves the sole purpose of being the
            surface to be used by the 'erase' method.
    """

    def __init__(self, size: tuple[int, int] = (0, 0), flags: int = 0, depth: int | None = None, surface: Surface | None = None):
        if surface is None:
            self.surface = Surface(size, flags, depth)
        else:
            self.surface = Surface(surface.get_size(), surface.get_flags(), surface.get_bitsize())
            self.surface.blit(surface, (0, 0))
        self.rect = Rect((0, 0), self.surface.get_size())
        self.drawn = False
        self.screen_bak = None
        self.screen = None
        self.addons = dict()
        self.drawn_area = None
        self.beneath = None
        self.alias = "Unnamed"
        self.parent = None
        self.camouflage = False


    def __str__(self) -> str:
        string = """\n{} Object\n\tPlaced inside {} surface\n\trelative position: {} (topleft vertex)\n\tCurrently drawn: {}""".format(
            self.alias,
            "undefined" if self.__screen is None else self.screen.get_size(),
            self.rect.topleft,
            "yes" if self.drawn else "no",
        )

        if len(self.addons.values()):
            addons_str = list()
            for addon in self.addons.values():
                addon_str = addon.__str__().replace("\n", "\n\t")
                addons_str.append(addon_str)
            addons_str = "\n".join(addons_str).replace("\n", "\n\t")
            string = f"{string}\n\tAddons:{addons_str}"

        return string


    @property
    def screen(self):
        if self.__screen is None:
            raise UndefinedScreen("The object is missing its drawing surface!")
        return self.__screen


    @screen.setter
    def screen(self, screen: Surface | None):
        self.__screen = screen
        if self.screen_bak is None:
            self.screen_bak = screen


    @property
    def screen_bak(self):
        return self.__screen_bak


    @screen_bak.setter
    def screen_bak(self, screen: Surface | None):
        if screen is None:
            self.__screen_bak = None
            return
        self.__screen_bak = screen.copy()
        self.__screen_bak.blit(screen, (0, 0))


    def move(self, vertex: str, coordinates: tuple[int, int]) -> None:
        """Moves a certain vertex of the Object to a given coordinate on the screen where it'll be drawn"""
        setattr(self.rect, vertex, coordinates)


    def fits(self) -> bool:
        """Checks if the Object can be drawn to its drawing surface in its current position"""
        return self.screen.get_rect().contains(self.rect)


    def draw(self, screen: Surface | None = None, info: str = "", addons: str | list[str] = "all") -> None:
        """
            draws the configured surface and its addons on another surface

            if the screen supplied is None, then the 'draw' method tries to use the 'screen' attr, if it exists. Otherwise UndefinedScreen will be thrown.
        """

        # if the Object is already drawn, then why the heck draw it again?
        # call erase first and then call this again!
        # if self.drawn:
        #     return

        try:
            if screen is not None:
                self.screen = screen
        except UndefinedScreen as e:
            e.add_note(f"Error when drawing {self.alias}")
            raise e

        if not self.fits():
            raise OutOfBoundary(f"'{self.alias}' object cannot be drawn because it exceeds the surface's limits", self.rect, self.screen.get_rect())

        self.drawn = True

        # store what will be beneath the Object after it gets drawn onto the screen
        ## creates a surface of the same size as the Object
        beneath_surface = self.surface.copy()
        ## save what's currently in the position where the Object will be blitted
        beneath_surface.blit(self.screen, (0, 0), self.rect)
        self.beneath = beneath_surface

        # setting this object to become transparent basically means that it should
        # have the same texture as its underlying surface.
        if self.camouflage:
            self.surface.blit(beneath_surface, (0, 0))

        # first draw the Object's addons
        if addons == "all":
            for addon in self.addons.values():
                addon.draw(screen=self.surface, info="drawn onto '{}'".format(self.alias))
        elif isinstance(addons, list):
            for addon in addons:
                self.addons[addon].draw(screen=self.surface, info="drawn onto '{}'".format(self.alias))
        else:
            self.addons[addons].draw(screen=self.surface, info="drawn onto '{}'".format(self.alias))

        # finally draw the Object to the screen
        self.drawn_area = self.screen.blit(self.surface, self.rect)
        update(self.drawn_area)

        # print("DRAW", self.alias, f"topleft relative position: {self.rect.topleft}", f"size: {self.surface.get_size()}", info, sep="\n\t")


    def erase(self, info: str = "") -> Rect:
        """
            Erases the Object according to what's saved in the backup screen
        """
        if not self.drawn:
            return

        for addon in self.addons.values():
            addon.erase(info="erased from '{}'".format(self.alias))

        drawn_area = self.drawn_area
        self.screen.blit(self.screen_bak, drawn_area, drawn_area)
        update(drawn_area)
        self.drawn_area = None
        self.beneath = None
        self.drawn = False

        # print("ERASE", self.alias, info, f"area erased: {self.surface.get_size()}", sep="\n\t")

        return drawn_area


    def add(self, ref: str, another_obj) -> None:
        """
            adds a new addon to this Object
        """
        another_obj.alias = ref
        another_obj.parent = self
        self.addons[ref] = another_obj


    def remove(self, ref: str, pop: bool = False, force_update: bool = False) -> Rect:
        """
            erases a addon from the object's surface
            if pop is True, then the addon is removed from the addons list and won't be redrawn
            if force_update is True, then the addon requests its parental Object to update itself on the screen. This chains up a recursive call, until an Object currently drawn on the actual display updates itself
        """

        if ref not in self.addons.keys():
            return 

        addon = self.addons[ref]

        # if the addon is not drawn it cannot be erased
        # if the object itself is not drawn, then the addon cannot be blitted
        if not addon.drawn or not self.drawn:
            return

        erased_area = addon.erase(f"removed from '{self.alias}'")
        if force_update:
            self.request_parent_update(erased_area)
        if pop:
            self.addons.pop(ref)

        return erased_area


    def update(self, area: Rect) -> Rect:
        """
            repaints a portion of the Object's surface onto its screen

            usecase example:
                    # remove a addon of another addon and then update the root object on the screen
                    # box is the root object
                    # addon1 is the first level addon
                    # arrow is the second level addon
                    # 1. arrow is removed of addon1
                    # 2. addon1's surface is updated only where arrow was removed
                    # 3. box's surface is updated only where addon1 changed
                    erased_area = box.addons["addon1"].remove("arrow")
                    drawn_area = addon1.update(erased_area)
                    box.update(drawn_area)
        """

        relative_topleft = self.rect.move(*area.topleft)
        relative_topleft.update(relative_topleft.topleft, area.size)

        # print(f"UDPATE\n\trequest to update {area} of {self.alias} (surface: {self.surface})\n\t{self.alias} is drawn onto {self.screen}\n\t{self.alias} is at {self.rect.topleft} (topleft)\n\tarea to be updated: {relative_topleft}")

        drawn_area = self.screen.blit(self.surface, relative_topleft, area)
        update(drawn_area)
        return drawn_area


    def request_parent_update(self, area: Rect):
        """
            method to request its parent to repaint itself on the screen when an addon is erased

            reminder: self.screen corresponds to self.parent.surface if self.parent is not None
        """
        # print(f"PARENT_UPDATE\n\tRequest to update {area} of {self.alias} on {self.screen}.\n\t{self.alias} is at {self.rect.topleft}.\n\tThe updated area should have {self.rect.topleft} + {area.topleft} topleft coords")
        if self.parent is None:
            area_relative_topleft = area.move(*self.rect.topleft)
            area = self.screen.blit(self.screen_bak, area_relative_topleft, area_relative_topleft)
            update(area)
        else:
            area_relative_topleft = self.rect.move(*area.topleft)
            area = self.screen.blit(self.surface, area_relative_topleft, area)
            self.parent.request_parent_update(area)


    def get_addons_positions(self, vertex: str, mode: str = "absolute") -> dict[str, tuple[int, int]]:
        positions = dict()
        for name, addon in self.addons.items():
            x2, y2 = getattr(addon.rect, vertex)
            if mode == "absolute":
                x1, y1 = getattr(self.rect, "topleft")
                positions[name] = x1+x2, y1+y2
            else:
                positions[name] = x2, y2
        return positions


    def scale_by(self, factor: float) -> None:
        self.surface = scale_by(self.surface, factor)
        self.rect.update(self.rect.topleft, self.surface.get_size())


    def flip(self, x_flip: bool, y_flip: bool) -> None:
        self.surface = flip(self.surface, x_flip, y_flip)

    
    def rotate(self, ang: int) -> None:
        self.surface = rotate(self.surface, ang)
        self.rect.update(self.rect.topleft, self.surface.get_size())


    def make_contour(self, color: Color, thickness: int) -> None:
        line(self.surface, color, self.surface.get_rect().bottomleft, self.surface.get_rect().topleft, width=thickness)
        line(self.surface, color, self.surface.get_rect().topleft, self.surface.get_rect().topright, width=thickness)
        line(self.surface, color, self.surface.get_rect().topright, self.surface.get_rect().bottomright, width=thickness+2)
        line(self.surface, color, self.surface.get_rect().bottomright, self.surface.get_rect().bottomleft, width=thickness+2)
