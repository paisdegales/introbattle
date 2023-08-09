from pygame import QUIT, MOUSEBUTTONDOWN, MOUSEBUTTONUP, KEYDOWN, KEYUP
from pygame.mouse import get_pos
from pygame.event import Event


class GameEvent:
    def action(self) -> None:
        raise NotImplementedError()


class KeyboardEventHandler:
    def __init__(self):
        self.events = dict()
        self.events.update({KEYDOWN: dict(),
                            KEYUP: dict()})


    def is_keyboard_event(self, event: Event) -> None:
        return event.type in (KEYDOWN, KEYUP)


    def add_keydown(self, key: int, event: GameEvent) -> None:
        self.events[KEYDOWN][key] = event


    def add_keyup(self, key: int, event: GameEvent) -> None:
        self.events[KEYUP][key] = event


    def handle(self, event_type: int, key: int) -> None:
        if event_type not in self.events.keys():
            return
        if key not in self.events[event_type].keys():
            return
        self.events[event_type][key].action()


class MouseEventHandler:
    def __init__(self):
        self.events = dict()
        self.events.update({MOUSEBUTTONUP: dict(),
                            MOUSEBUTTONDOWN: dict()})


    def is_mouse_event(self, event: Event) -> None:
        return event.type in (MOUSEBUTTONUP, MOUSEBUTTONDOWN)


    def add_buttonup(self, key: int, event: GameEvent) -> None:
        self.events[MOUSEBUTTONUP][key] = event


    def add_buttondown(self, key: int, event: GameEvent) -> None:
        self.events[MOUSEBUTTONDOWN][key] = event


    def handle(self, event_type: int, button: int) -> None:
        if event_type not in self.events.keys():
            return
        if button not in self.events[event_type].keys():
            return
        self.events[event_type][button].action()


class EndOfScene(Exception):
    def action(self, *args):
        super().__init__(*args)


class CloseGame(GameEvent):
    def action(self) -> None:
        exit()


class GetCursorPosition(GameEvent):
    def action(self) -> None:
        x, y = get_pos()
        print(f"X: {x}, Y: {y}")
