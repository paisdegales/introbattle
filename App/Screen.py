from App.Object.Object import BaseObject
from App.Setup.Utils import screen_logger
from pygame.surface import Surface
from pygame.rect import Rect
from pygame.display import init, get_init, set_mode, list_modes, set_caption, update

class Screen:
    """ Create/manage the user's display screen. """

    def __init__(self, display: tuple[int, int]) -> None:
        if not get_init():
            init()

        set_caption("Introbattle")
        if display in list_modes():
            self.image = set_mode(size=display)
        else:
            self.image = set_mode() # max proportions

        screen_logger.info('%s display created', self.image.get_size())

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
        """ The 'draw' method draws all its positional parameters to the display screen
            and returns a list of the areas that have changed.

            The objects are drawn in the same order they are provided in the argument list.

            The areas that have changed will only be displayed after calling 'pygame.update' or
            the 'update' method """

        areas: list[Rect] = list()

        for obj in objs:
            if not obj.drawn:
                screen_logger.info('%s will be drawn to the display', obj.name)
                eraser, area = obj.draw(self.image)
                self.objects[obj.name] = (obj, eraser, area)
                areas.append(area)

        self.changed.extend(areas)

        return areas


    def erase(self, *names: str) -> list[Rect]:
        """ erases **entire** objects off the screen

            A brief word on 'erasing'
            There are two ways of erasing an object off the screen:
                1. calling the 'erase' method for that object
                2. blitting to the screen what's beneath the object at its current position
            PS: both methods involve updating the regions of the screen that have changed

            The 'erase' method opts for the first strategy, but the second one could also be done.
            The second strategy for erasing objects grants the screen more control over how objects
            are erased. That's why it's supported. """

        objects: list[BaseObject] = list()
        areas: list[Rect] = list()

        keys = self.objects.keys()
        for name in names:
            if name not in keys:
                continue
            objects.append(self.objects[name][0])

        for obj in objects:
            screen_logger.info('%s will be erased from the display', obj.name)
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

        screen_logger.info('area from %s to %s was queued for eventual update', str(area.topleft), str(area.topright))
        self.changed.append(area)


    def update(self) -> None:
        if len(self.changed):
            screen_logger.info('%s group is about to be updated', str(self.changed))
            update(self.changed)
            self.changed.clear()
