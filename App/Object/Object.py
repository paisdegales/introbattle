from App.Setup.Utils import object_logger
from pygame.surface import Surface
from pygame.rect import Rect
from pygame.draw import line
from pygame.color import Color
from pygame.transform import scale_by, flip, rotate
from pygame.image import load


class BaseObject:
    """ Base class to support positioning, transforming, updating, erasing and drawing objects to surfaces

        It works like Sprites, except that this class is not intended to be used by a 'Group' class, but rather it works by itself """

    def __init__(self, name: str, surface: Surface):
        object_logger.info('%s initialized', name)

        # the name to identify this instance when printing it
        self.name: str = name
        # the surface which contains what will be drawn onto the screen
        self.image: Surface = surface
        # the Object's image positioning. It's coordinates are relative to the surface it's drawn onto.
        self.rect: Rect = Rect((0, 0), surface.get_size())
        self.drawn: bool = False
        # indicates if the Object should have the same background as its screen when it gets drawn onto it.
        self.hide: bool = False
        # controls how much an object 'vibrates' when calling 'vibrate'
        self.vibration: int = 5


    def __str__(self) -> str:
        string = [f"name: {self.name}", f"topleft (rel. coords.): {self.rect.topleft}", f"size: {self.rect.size}"]
        return "\n".join(string)


    def shift(self, dx: int, dy: int) -> None:
        x, y = self.rect.topleft
        if (x + dx) < 0:
            return
        if (y + dy) < 0:
            return
        self.rect.topleft = x + dx, y + dy


    def move(self, vertex: str, coordinates: tuple[int, int]) -> None:
        setattr(self.rect, vertex, coordinates)


    def draw(self, surface: Surface) -> tuple[Surface, Rect]:
        """ Draw the entire object in a surface
            The object's 'rect' attribute is used to control where it'll be drawn
            This method returns everything that is necessary to erase the object from where it was drawn.

            Parameters:
                surface: the surface where the object will be drawn onto
            
            Return: Tuple
                1 element: a surface of what is beneath the object
                2 element: a rect, which indicates the RELATIVE POSITION where the object was drawn in the surface """

        if self.drawn:
            raise Exception(f"{self.name} can't be drawn again")


        if self.hide:
            bak = self.image.copy()
            bak.set_colorkey(Color(0, 0, 0))
            bak.blit(self.image, (0, 0))
            self.image.blit(surface, (0, 0), self.rect)
            self.image.blit(bak, (0, 0))

        self.beneath = self.image.copy()
        self.beneath.blit(surface, (0, 0), self.rect)
        self.area = surface.blit(self.image, self.rect.topleft)
        self.surface = surface
        self.drawn = True

        object_logger.info('%s was drawn from %s to %s in a %s surface', self.name, str(self.area.topleft), str(self.area.bottomright), repr(surface.get_size()))

        return self.beneath, self.area


    def erase(self) -> Rect:
        """ Erase the entire object off the surface used previously by 'draw'

            PS: when drawing onto the screen/pygame window, make sure to update
            the portion of the screen that has changed, otherwise no visible
            changes will be seen

            Parameters:

            Return: Rect
                * the portion of the surface that has changed """

        if not self.drawn:
            raise Exception(f"{self.name} can't be erased")

        area = self.surface.blit(self.beneath, self.area.topleft)
        if area.size == (0, 0):
            raise Exception(f"{self.name} apparently was not erased")

        del self.surface, self.area, self.beneath
        self.drawn = False

        return area


    def refresh(self, area: Rect) -> tuple[Surface, Rect]:
        """ repaints a portion of this object in the previously drawn surface 

            Parameters:
                area: the portion of this object that is going to be drawn. If None, then the entire object is redrawn.
            
            Return: Tuple
                1 element: a surface of what is beneath the object
                2 element: a rect, which indicates the relative position where the object was drawn in the surface """

        if not self.drawn:
            raise Exception(f"{self.name} can't be refreshed if not drawn")

        if self.hide:
            bak = self.image.copy()
            bak.set_colorkey(Color(0, 0, 0))
            bak.blit(self.image, (0, 0))
            self.image.blit(self.beneath, (0, 0))
            self.image.blit(bak, (0, 0))

        beneath = Surface(area.size)
        beneath.blit(self.image, (0,0), area)
        refreshed_area = self.surface.blit(self.image, self.rect.move(*area.topleft), area)

        return beneath, refreshed_area


    def replace(self, area: Rect, surface: Surface) -> Rect:
        """ replaces a portion of this object with another surface

            Parameters:
                area: the portion of this object to be replaced by something else
                surface: the replacer surface

            Return: Rect
                * the area of what has changed """

        if not self.drawn:
            raise Exception(f"{self.area} of {self.name} won't be replaced if not drawn")

        if area.size != surface.get_size():
            raise Exception(f"Apparently the area to be replaced and the surface's size mismatch. This can't happen.")

        replaced_area = self.image.blit(surface, area)
        _, replaced_area = self.refresh(replaced_area)

        return replaced_area


    def vibrate(self, surface: Surface) -> tuple[Surface, Rect]:
        """ make this entire object vibrate

            the vibration performs the following steps:
                1. the object is erased
                2. the object is shifted by 'self.vibration' pixels
                3. the object is redrawn on the same surface as before

            Return: Tuple
                1. a surface of what is beneath the object
                2. the area of the Object that has changed
                    * the area's coordinates are relative to the surface the object is currently drawn onto """

        if not self.drawn:
            # raise Exception(f"{self.name} can't be vibrated without being drawn")
            return Surface((0, 0)), Rect(0, 0, 0, 0)
        erased_area = self.erase()
        self.shift(self.vibration, self.vibration)
        beneath, area = self.draw(surface)
        area = erased_area.union(area)
        self.vibration *= -1
        return beneath, area


    def vibrate_component(self, component_name: str) -> Rect:
        """ make a certain component of this object vibrate

            Return: Rect
                * the area of the object that has changed """

        if not self.drawn:
            return Rect(0, 0, 0, 0)
        component = getattr(self, component_name)
        if not isinstance(component, BaseObject):
            raise Exception(f"{component_name} can't be vibrated!")
        _, r = component.vibrate(self.image)
        _, r = self.refresh(r)
        return r


    def scale_by(self, factor: float) -> None:
        self.image = scale_by(self.image, factor)
        self.rect.update(self.rect.topleft, self.image.get_size())


    def flip(self, x_flip: bool, y_flip: bool) -> None:
        self.image = flip(self.image, x_flip, y_flip)

    
    def rotate(self, ang: int) -> None:
        self.image = rotate(self.image, ang)
        self.rect.update(self.rect.topleft, self.image.get_size())


    def make_contour(self, color: Color, thickness: int) -> None:
        w, h = self.image.get_size()
        line(self.image, color, (0, h), (0, 0), width=thickness)
        line(self.image, color, (0, 0), (w, 0), width=thickness)
        line(self.image, color, (w, 0), (w, h), width=thickness+2)
        line(self.image, color, (w, h), (0, h), width=thickness+2)



class SizedObject(BaseObject):
    def __init__(self, name: str, size: tuple[int, int]):
        super().__init__(name, Surface(size))


class ImportedObject(BaseObject):
    def __init__(self, name: str, filename: str):
        surface = load(filename)
        min_rect = surface.get_bounding_rect()
        cropped_surface = Surface(min_rect.size, flags=surface.get_flags(), depth=surface.get_bitsize())
        cropped_surface.blit(surface, (0, 0), min_rect)
        super().__init__(name, cropped_surface)
