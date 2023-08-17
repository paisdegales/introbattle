from App.Screen.Screen import Screen
from App.Screen.GameEvent import KeyboardEventHandler, MouseEventHandler, CloseGame, GetCursorPosition, QUIT
from pygame.event import get as get_events
from logging import warning

class Scene:
    """
        Class which organizes the game in parts, so called 'Scenes'. All scenes should have separate folders inside App/Scenes/
        The idea is to gather objects (texts, images, sounds and so on) that make sense when put together in a certain context
    """


    def __init__(self, screen: Screen) -> None:
        self.screen = screen

        self.keyboard = KeyboardEventHandler()

        self.mouse = MouseEventHandler()
        self.mouse.add_buttondown(1, GetCursorPosition())

        self.quit = CloseGame()

        self.objects = list()


    def load_initial_frame(self, *args) -> None:
        raise NotImplementedError()


    def draw_initial_frame(self) -> None:
        raise NotImplementedError()


    def check_events(self) -> int:
        for event in get_events():
            try:
                if event.type == QUIT:
                    self.quit.action()
                elif self.keyboard.is_keyboard_event(event):
                    self.keyboard.handle(event.type, event.key)
                elif self.mouse.is_mouse_event(event):
                    self.mouse.handle(event.type, event.button)
            except Exception as err:
                err.add_note(f"Scene failed at check_events: {type(err)=}")
                raise err

    def terminate(self) -> None:
        raise NotImplementedError()

    def erase(self) -> None:
        raise NotImplementedError()

    def __str__(self) -> str:
        string = list()
        string.append("Menu Scene Overview:")
        for obj in self.objects:
            string.append(obj.__str__())
        string = "\n".join(string)
        return string
