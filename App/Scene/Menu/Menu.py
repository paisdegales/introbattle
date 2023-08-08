from App.Object.BackgroundImage import BackgroundImage
from App.Scene.Menu.Local.Banner import Banner
from App.Scene.Menu.Local.GuildOptions import GuildOptions
from App.Scene.Menu.Local.Selector import Selector
from App.Scene.Menu.Local.Positioning import *
from App.Scene.Menu.Local.GameEvent import *
from App.Scene.Scene import Scene
from App.Screen.Screen import Screen
from pygame.locals import K_z, K_UP, K_DOWN, K_LEFT, K_RIGHT
from logging import warning

class Menu(Scene):
    def __init__(self, screen: Screen) -> None:
        super().__init__(screen)


    def load_initial_frame(self) -> None:
        try:
            self.background = BackgroundImage(self.screen.get_size())

            self.banner = Banner("OpenSans", self.screen)
            self.banner.load("Introbattle!", size=(280, 80), vertex="center", relative_coordinates=(140, 40))

            self.guild_options = GuildOptions()

        except Exception as e:
            warning(f"Failed when loading the menu: {type(e)}")
            raise e


    def draw_initial_frame(self) -> None:
        try:
            self.background.screen = self.screen
            self.background.move(*BACKGROUND_POSITION)
            self.background.draw()

            self.banner.move(*BANNER_POSITION)
            self.banner.draw()

            self.guild_options.draw(self.screen)

            self.selector = Selector(self.guild_options.get_anchors(), displacement=(0, -10))
            self.selector.screen = self.screen
            self.selector.draw()
            self.keyboard.add_keydown(K_UP, MoveSelectorUp(self.selector))
            self.keyboard.add_keydown(K_DOWN, MoveSelectorDown(self.selector))
            self.keyboard.add_keydown(K_LEFT, MoveSelectorLeft(self.selector))
            self.keyboard.add_keydown(K_RIGHT, MoveSelectorRight(self.selector))
            self.keyboard.add_keydown(K_z, SelectorGet(self.selector))
        except Exception as e:
            warning("Failed when drawing the menu")
            raise e


    def erase(self) -> None:
        try:
            #self.background.erase()
            self.banner.erase()
        except Exception as e:
            warning("Failed when trying to erase the menu scene!")
            raise e
