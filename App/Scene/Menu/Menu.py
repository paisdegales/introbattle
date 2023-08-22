from App.Scene.Menu.Local.Banner import Banner
from App.Scene.Menu.Local.GuildOptions import GuildOptions
from App.Scene.Menu.Local.Positioning import *
from App.Scene.Menu.Local.Selector import MenuSelector
from App.Scene.Scene import Scene
from App.Screen.Screen import Screen
from logging import warning
from pygame.event import Event, clear
from pygame.locals import K_z, K_UP, K_DOWN, K_LEFT, K_RIGHT, QUIT, MOUSEBUTTONDOWN, KEYDOWN
from pygame.mouse import get_pos

class Menu(Scene):
    def __init__(self, screen: Screen) -> None:
        super().__init__(screen)
        self.player_options: list[str] = list()


    def load_initial_frame(self) -> None:
        try:
            self.banner = Banner("OpenSans")
            self.banner.load("Introbattle!", size = BANNER_SIZE, vertex="center")
            self.guild_options = GuildOptions()

        except Exception as e:
            warning(f"Failed when loading the menu: {type(e)}")
            raise e


    def draw_initial_frame(self) -> None:
        try:
            self.background.move(*BACKGROUND_POSITION)
            self.background.draw(screen=self.screen, info="drawn onto main screen")

            self.banner.move(*BANNER_POSITION)
            self.banner.draw(screen=self.screen, info="drawn onto main screen")

            self.guild_options.draw(screen=self.screen, topleft=GUILDOPTIONS_TOPLEFT)

            self.selector = MenuSelector(self.guild_options, displacement=SELECTOR_DISPLACEMENT)
            self.selector.draw(screen=self.screen)

            self.objects.append(self.background)
            self.objects.append(self.banner)
            self.objects.append(self.guild_options)
            self.objects.append(self.selector)
        except Exception as e:
            warning("Failed when drawing the menu")
            raise e


    def check_events(self, events: list[Event]) -> None:
        try:
            for event in events:
                if event.type == QUIT:
                    exit()
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x, y = get_pos()
                        print(f"X: {x}, Y: {y}")
                elif event.type == KEYDOWN:
                    if event.key == K_UP:
                        self.selector.up()
                    elif event.key == K_DOWN:
                        self.selector.down()
                    elif event.key == K_LEFT:
                        self.selector.left()
                    elif event.key == K_RIGHT:
                        self.selector.right()
                    elif event.key == K_z:
                        self.selector.select(self.player_options)
            clear()
        except Exception as err:
            err.add_note(f"Menu Scene failed at check_events: {type(err)=}")
            raise err


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

