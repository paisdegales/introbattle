from App.Screen.GameEvent import GameEvent
from App.Object.Object import Object
from App.Scene.Menu.Local.Selector import Selector


class MoveSelectorRight(GameEvent):
    def __init__(self, selector: Selector):
        self.selector = selector


    def action(self) -> None:
        self.selector.erase()
        self.selector.right()
        self.selector.draw()


class MoveSelectorLeft(GameEvent):
    def __init__(self, selector: Selector):
        self.selector = selector


    def action(self) -> None:
        self.selector.erase()
        self.selector.left()
        self.selector.draw()


class MoveSelectorUp(GameEvent):
    def __init__(self, selector: Selector):
        self.selector = selector


    def action(self) -> None:
        self.selector.erase()
        self.selector.up()
        self.selector.draw()


class MoveSelectorDown(GameEvent):
    def __init__(self, selector: Selector):
        self.selector = selector


    def action(self) -> None:
        self.selector.erase()
        self.selector.down()
        self.selector.draw()


class SelectorGet(GameEvent):
    def __init__(self, selector: Selector):
        self.selector = selector


    def action(self) -> str:
        return self.selector.get_current_ref()


class ToggleBanner(GameEvent):
    def __init__(self, banner: Object):
        self.banner = banner


    def action(self) -> None:
        self.banner.toggle()
