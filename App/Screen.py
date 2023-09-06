from App.Object.Object import BaseObject
from pygame.surface import Surface
from pygame.rect import Rect
from pygame.display import init, get_init, set_mode, list_modes, set_caption, update

class Screen:
    """ Class responsible for creating/managing the user's display screen.

        There are two ways of erasing an object off the screen:
            1. call the 'erase' method of that object
            2. blit to the screen what's beneath the object at its position
        But methods involve updating the regions of the screen that have changed

        The 'erase' method of the Screen class opts for the first method, but the
        second one can also be implemented and works just as fine.

        The second method for erasing objects grants the screen more control on how objects
        are erased and this is the reason why it's supported (eventhough not implemented) """

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

        keys = self.objects.keys()
        for name in names:
            if name not in keys:
                continue
            objects.append(self.objects[name][0])

        for obj in objects:
            area = obj.erase()
            areas.append(area)

        for name in names:
            if name not in keys:
                continue
            self.objects.pop(name)

        self.changed.extend(areas)
            
        return areas


    def queue(self, area: Rect) -> None:
        """ queues a portion of the screen to be updated by 'update' """

        self.changed.append(area)


    def update(self) -> None:
        if len(self.changed):
            update(self.changed)
            self.changed.clear()
