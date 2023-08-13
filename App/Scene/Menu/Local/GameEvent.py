from App.Screen.GameEvent import GameEvent, EndOfScene
from App.Object.Object import Object
from App.Object.Selector import Selector


class MoveSelectorRight(GameEvent):
    def __init__(self, selector: Selector, obj):
        self.selector = selector
        self.obj = obj


    def action(self) -> None:
        item = self.selector.get_current_ref()
        self.obj.unhighlight_text(item)

        self.selector.erase()
        self.selector.right()
        self.selector.draw()

        item = self.selector.get_current_ref()
        self.obj.highlight_text(item)


class MoveSelectorLeft(GameEvent):
    def __init__(self, selector: Selector, obj):
        self.selector = selector
        self.obj = obj


    def action(self) -> None:
        item = self.selector.get_current_ref()
        self.obj.unhighlight_text(item)

        self.selector.erase()
        self.selector.left()
        self.selector.draw()

        item = self.selector.get_current_ref()
        self.obj.highlight_text(item)


class MoveSelectorUp(GameEvent):
    def __init__(self, selector: Selector, obj):
        self.selector = selector
        self.obj = obj


    def action(self) -> None:
        item = self.selector.get_current_ref()
        self.obj.unhighlight_text(item)

        self.selector.erase()
        self.selector.up()
        self.selector.draw()

        item = self.selector.get_current_ref()
        self.obj.highlight_text(item)


class MoveSelectorDown(GameEvent):
    def __init__(self, selector: Selector, obj):
        self.selector = selector
        self.obj = obj


    def action(self) -> None:
        item = self.selector.get_current_ref()
        self.obj.unhighlight_text(item)

        self.selector.erase()
        self.selector.down()
        self.selector.draw()

        item = self.selector.get_current_ref()
        self.obj.highlight_text(item)


class SelectorGet(GameEvent):
    def __init__(self, selector: Selector, storage: list):
        self.selector = selector
        self.storage = storage


    def action(self) -> str:
        item = self.selector.get_current_ref()
        self.storage.append(item)
        if len(self.storage) == 3:
            raise EndOfScene("The player chose: {}".format(self.storage))
        return item


class ToggleBanner(GameEvent):
    def __init__(self, banner: Object):
        self.banner = banner


    def action(self) -> None:
        self.banner.toggle()
