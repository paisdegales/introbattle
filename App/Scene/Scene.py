from App.Object.BackgroundImage import BackgroundImage
from App.Screen import Screen
from pygame.event import Event


class EndOfScene(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class Scene:
    """ Class which organizes the game in parts, so called 'Scenes'. All scenes should have separate folders inside App/Scenes/
        The idea is to gather objects (texts, images, sounds and so on) that make sense when put together in a certain context """

    def __init__(self, screen: Screen) -> None:
        self.screen = screen
        self.objects = list()
        self.background = BackgroundImage(self.screen.screen.get_size())
        self.objects.append(self.background)
        self.noevent_counter = 0

    def load_initial_frame(self, *args) -> None:
        raise NotImplementedError()

    def check_event(self, event: Event) -> int:
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
