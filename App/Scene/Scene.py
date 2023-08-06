from App.Screen.Screen import Screen
from App.Screen.GameEvent import GameEvent, CloseGame, GetCursorPosition
from pygame.event import get as get_events
from logging import warning

class Scene:
    """
        Class which organizes the game in parts, so called 'Scenes'. All scenes should have separate folders inside App/Scenes/
        The idea is to gather objects (texts, images, sounds and so on) that make sense when put together in a certain context
    """

    def __init__(self, screen: Screen) -> None:
        self.screen = screen
        self.events: dict[int, GameEvent] = dict()
        self.add_event(CloseGame())
        self.add_event(GetCursorPosition())

    def load_initial_frame(self) -> None:
        raise NotImplementedError()

    def draw_initial_frame(self) -> None:
        raise NotImplementedError()

    def check_events(self) -> int:
        for event in get_events():
            if event.type in self.events.keys():
                try:
                    evento_info = self.events[event.type].action()
                except Exception as err:
                    err.add_note(f"Scene failed at check_events: {type(err)=}")
                    raise err

    def add_event(self, new_event: GameEvent) -> None:
        if new_event.key in self.events.keys():
            return
        self.events[new_event.key] = new_event

    def erase(self) -> None:
        raise NotImplementedError()
