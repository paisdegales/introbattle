from App.Scene.Menu.Local.Banner import Banner
from App.Scene.Menu.Local.GuildOptions import GuildOptions
from App.Scene.Menu.Local.Positioning import *
from App.Scene.Scene import Scene
from App.Screen import Screen
from pygame.locals import K_z, K_UP, K_DOWN, K_LEFT, K_RIGHT, QUIT, MOUSEBUTTONDOWN, KEYDOWN
from pygame.mouse import get_pos
from pygame.event import Event


class Menu(Scene):
    def __init__(self, screen: Screen) -> None:
        super().__init__(screen)
        self.player_options: list[str] = list()


    def load_initial_frame(self) -> None:
        try:
            self.background.move(*BACKGROUND_POSITION)
            self.banner = Banner("OpenSans")
            self.banner.load("Introbattle!", size = BANNER_SIZE, vertex="center")
            self.banner.move(*BANNER_POSITION)
            self.guild_options = GuildOptions((200, 200))
            self.objects.append(self.banner)
            self.objects.append(self.guild_options)
            self.screen.draw(*self.objects)
        except Exception as e:
            e.add_note(f"Failed when loading the menu: {type(e)}")
            raise e


    def check_event(self, event: Event) -> None:
        if event.type == QUIT:
            exit()
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = get_pos()
                print(f"X: {x}, Y: {y}")
        elif event.type == KEYDOWN:
            if event.key == K_UP:
                self.guild_options.select("up")
            elif event.key == K_DOWN:
                self.guild_options.select("down")
            elif event.key == K_LEFT:
                self.guild_options.select("left")
            elif event.key == K_RIGHT:
                self.guild_options.select("right")
            elif event.key == K_z:
                # self.selector.select(self.player_options)
                pass


    def erase(self) -> None:
        try:
            #self.background.erase()
            self.banner.erase()
            self.guild_options.erase()
        except Exception as e:
            e.add_note("Failed when trying to erase the menu scene!")
            raise e


    def terminate(self) -> list[str]:
        return self.player_options
