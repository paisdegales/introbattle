from App.Screen.GameEvent import GameEvent, KeyboardEventHandler
from App.Object.Selector import Selector
from App.Scene.Battle.Locals.OptionsBox import OptionsBox

class MoveSelectorUp(GameEvent):
    def __init__(self, selector: Selector):
        self.selector = selector


    def action(self) -> None:
        self.selector.erase()
        self.selector.up()
        self.selector.draw()
        item = self.selector.get_current_ref()

class MoveSelectorDown(GameEvent):
    def __init__(self, selector: Selector):
        self.selector = selector


    def action(self) -> None:
        self.selector.erase()
        self.selector.down()
        self.selector.draw()
        item = self.selector.get_current_ref()


class SelectHero(GameEvent):
    def __init__(self, keyboard_handler: KeyboardEventHandler, box: OptionsBox):
        self.kbd_handler = keyboard_handler
        self.box = box


    def action(self) -> None:
        self.kbd_handler.turnoff()
        self.box.erase()
        self.box.next_state()
        self.box.draw()
