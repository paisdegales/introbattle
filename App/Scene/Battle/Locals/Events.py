from App.Screen.GameEvent import GameEvent, KeyboardEventHandler
from App.Object.Selector import Selector
from App.Scene.Battle.Locals.OptionsBox import OptionsBox
from App.Scene.Battle.Locals.CharacterBand import HeroBand
from App.Scene.Battle.Locals.OptionsSelector import OptionsSelector
from pygame.display import get_surface
from pygame.surface import Surface
from pygame.locals import K_LEFT, K_RIGHT, K_RETURN

class MoveSelectorUp(GameEvent):
    def __init__(self, selector: Selector):
        super().__init__()
        self.selector = selector


    def action(self) -> None:
        self.selector.erase()
        self.selector.up()
        self.selector.draw()
        #self.selector.get_current_ref()

class MoveSelectorDown(GameEvent):
    def __init__(self, selector: Selector):
        super().__init__()
        self.selector = selector


    def action(self) -> None:
        self.selector.erase()
        self.selector.down()
        self.selector.draw()
        #self.selector.get_current_ref()


class SelectLeftOption(GameEvent):
    def __init__(self, box: OptionsBox):
        super().__init__()
        self.box = box


    def action(self) -> None:
        self.box.option_selector.erase()
        self.box.option_selector.left()
        self.box.option_selector.draw(screen=self.box.screen)


class SelectRightOption(GameEvent):
    def __init__(self, box: OptionsBox):
        super().__init__()
        self.box = box


    def action(self) -> None:
        self.box.option_selector.erase()
        self.box.option_selector.right()
        self.box.option_selector.draw(screen=self.box.screen)


class SelectAction(GameEvent):
    def __init__(self, keyboard_handler: KeyboardEventHandler, box: OptionsBox):
        super().__init__()
        self.kbd_handler = keyboard_handler
        self.box = box

    def action(self) -> None:
        atk_dfd = self.box.state.option_selector.get_current_ref()
        #print(atk_dfd)
        self.kbd_handler.turnoff()
        self.box.erase()
        self.box.next_state()
        #self.box.load(fighter)
        self.box.draw()


class SelectHero(GameEvent):
    def __init__(self, keyboard_handler: KeyboardEventHandler, box: OptionsBox):
        super().__init__()
        self.kbd_handler = keyboard_handler
        self.box = box


    def action(self) -> None:
        self.kbd_handler.turnoff()
        self.box.erase()
        self.box.next_state()
        self.box.draw()
        self.kbd_handler.add_keydown(K_LEFT, SelectLeftOption(self.box.state))
        self.kbd_handler.add_keydown(K_RIGHT, SelectRightOption(self.box.state))
        self.kbd_handler.add_keydown(K_RETURN, SelectAction(self.kbd_handler, self.box))


#class SelectOption(GameEvent):
#    def __init__(self, selector: Selector, box: OptionsBox):
#        super().__init__()
#        self.box = box
#        self.selector = selector
#
#
#    def action(self) -> None:
#        self.box.erase()
#        self.box.next_state()
#        self.box.load(selector.get_current_ref())
#        self.box.draw()
