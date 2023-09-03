from App.Object.BackgroundImage import BackgroundImage
from pygame.surface import Surface
from pygame.event import Event


class EndOfScene(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class Scene:
    """
        Class which organizes the game in parts, so called 'Scenes'. All scenes should have separate folders inside App/Scenes/
        The idea is to gather objects (texts, images, sounds and so on) that make sense when put together in a certain context
    """

    def __init__(self, screen: Surface) -> None:
        self.screen = screen
        self.objects = list()
        self.background = BackgroundImage(self.screen.get_size())
        self.objects.append(self.background)

    def load_initial_frame(self, *args) -> None:
        raise NotImplementedError()

    def draw_initial_frame(self) -> None:
        raise NotImplementedError()

    def check_events(self, events: list[Event]) -> int:
        raise NotImplementedError()

    def terminate(self):
        raise NotImplementedError()

    def erase(self) -> None:
        raise NotImplementedError()

    def __str__(self) -> str:
        string = list()
        string.append("Scene Overview:")
        for obj in self.objects:
            string.append(obj.__str__())
        string = "\n".join(string)
        return string
