from App.Object.Object import BaseObject
from pygame.surface import Surface
from pygame.rect import Rect
from pygame.display import init, get_init, set_mode, list_modes, set_caption, update

class Screen:
    """ Class responsible for creating/managing the user's display screen. """

    def __init__(self, display: tuple[int, int]) -> None:
        if not get_init():
            init()

        set_caption("Introbattle")
        if display in list_modes():
            self.screen = set_mode(size=display)
        else:
            self.screen = set_mode() # max proportions

        """ this dict stores everything necessary to erase an entire object off the screen
            the key is the object's name
            the tuple's first item is the object itself 
            the tuple's second item is the surface beneath the object
            the tuple's third item is the absolute position of the drawing on the screen """
        self.objects: dict[str, tuple[BaseObject, Surface , Rect]] = dict()


        """ stores temporarilly all positions on the screen that got drawn/erased 
            all positions can be later updated all together with a call to 'update' """
        self.changed: list[Rect] = list()


    def draw(self, *objs: BaseObject) -> list[Rect]:
        areas: list[Rect] = list()

        for obj in objs:
            if not obj.drawn:
                eraser, area = obj.draw(self.screen)
                self.objects[obj.name] = (obj, eraser, area)
                areas.append(area)

        self.changed.extend(areas)

        return areas


    def erase(self, *names: str) -> list[Rect]:
        """ erases entire objects off the screen"""

        objects: list[BaseObject] = list()
        areas: list[Rect] = list()
        surfaces: list[Surface] = list()

        keys = self.objects.keys()
        for name in names:
            if name not in keys:
                continue
            objects.append(self.objects[name][0])
            surfaces.append(self.objects[name][1])
            areas.append(self.objects[name][2])

        for obj, surface, area in zip(objects, surfaces, areas):
            if obj.drawn:
                obj.erase(self.screen, surface, area)

        for name in names:
            if name not in keys:
                continue
            self.objects.pop(name)

        self.changed.extend(areas)
            
        return areas


    def refresh(self, name: str, area: Rect) -> Rect:
        """ refresh a small area of an object on the screen

            area: the relative area of the object to be updated (Rect)

            this method should be called when the object's surface has changed (AND
             HAS NOT MOVED) but the screen still hasn't been updated

            the idea is that:
                # the object's image is changed before
                erased_area = screen.update(name, area)
            is better than:
                # the object's image is changed before
                erased_area_list = screen.erase(name) # len(list) == 1
                drawn_area_list = screen.draw(obj) # len(list) == 1

            why 'refresh' is better to update a single object:
            * 'refresh' generates smaller rectangles for screen updates
                > 'erase' and 'draw' both operate on the entire object
            * less code
            * 'refresh' returns a single Rect 
                > 'erase' and 'draw' both return a list of Rectangles
            * 'refresh' doesn't affect the 'objects' attribute
                > this means that the erase operation of the entire object will
                remain exactly the same after it's image got updated """

        surface = self.objects[name][0]
        coordinates = self.objects[name][2]
        rect = self.screen.blit(surface.image, coordinates.move(*area.topleft).topleft, area)
        self.changed.append(rect)

        return rect


    def update(self) -> None:
        if len(self.changed):
            update(self.changed)
            self.changed.clear()
