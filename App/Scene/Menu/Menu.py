from App.Object.BackgroundImage import BackgroundImage
from App.Scene.Menu.Local.Banner import Banner
from App.Scene.Menu.Local.GuildOptions import GuildOptions
from App.Scene.Menu.Local.Selector import MenuSelector
from App.Scene.Menu.Local.Positioning import *
from App.Scene.Menu.Local.GameEvent import *
from App.Scene.Scene import Scene
from App.Screen.Screen import Screen
from pygame.locals import K_z, K_UP, K_DOWN, K_LEFT, K_RIGHT
from logging import warning

class Menu(Scene):
    def __init__(self, screen: Screen) -> None:
        super().__init__(screen)
        self.player_options: list[str] = list()


    def load_initial_frame(self) -> None:
        try:
            self.background = BackgroundImage(self.screen.get_size())

            self.banner = Banner("OpenSans")
            self.banner.load("Introbattle!", size=(280, 80), vertex="center", relative_coordinates=(140, 40))

            self.guild_options = GuildOptions()

        except Exception as e:
            warning(f"Failed when loading the menu: {type(e)}")
            raise e


    def draw_initial_frame(self) -> None:
        try:
            self.background.move(*BACKGROUND_POSITION)
            self.background.draw(screen=self.screen)

            self.banner.move(*BANNER_POSITION)
            self.banner.draw(screen=self.screen, transparent=False)

            self.guild_options.draw(screen=self.screen)

            self.selector = MenuSelector(self.guild_options.get_anchors(), displacement=(0, -10))
            self.selector.draw(screen=self.screen)
            self.keyboard.add_keydown(K_UP, MoveSelectorUp(self.selector, self.guild_options))
            self.keyboard.add_keydown(K_DOWN, MoveSelectorDown(self.selector, self.guild_options))
            self.keyboard.add_keydown(K_LEFT, MoveSelectorLeft(self.selector, self.guild_options))
            self.keyboard.add_keydown(K_RIGHT, MoveSelectorRight(self.selector, self.guild_options))
            self.keyboard.add_keydown(K_z, SelectorGet(self.selector, self.player_options))

            self.objects.append(self.background)
            self.objects.append(self.banner)
            self.objects.append(self.guild_options)
            self.objects.append(self.selector)
        except Exception as e:
            warning("Failed when drawing the menu")
            raise e


    def erase(self) -> None:
        try:
            #self.background.erase()
            self.banner.erase()
            self.guild_options.erase()
            self.selector.erase()
        except Exception as e:
            warning("Failed when trying to erase the menu scene!")
            raise e


    def terminate(self) -> list[str]:
        return self.player_options


    def __str__(self) -> str:
        string = list()
        string.append("Menu Scene Overview:")
        for obj in self.objects:
            string.append(obj.__str__())
        string = "\n".join(string)
        return string

