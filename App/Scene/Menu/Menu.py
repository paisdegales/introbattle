from App.Scene.Menu.Local.Banner import Banner
from App.Scene.Menu.Local.GuildOptions import GuildOptions
from App.Scene.Menu.Local.Locals import *
from App.Scene.Scene import Scene, EndOfScene
from App.Screen import Screen
from App.Setup.Globals import ANIMATE
from App.Setup.Utils import menu_scene_logger
from pygame.locals import K_z, K_UP, K_DOWN, K_LEFT, K_RIGHT, QUIT, MOUSEBUTTONDOWN, KEYDOWN
from pygame.mouse import get_pos
from pygame.event import Event


class Menu(Scene):
    def __init__(self, screen: Screen) -> None:
        menu_scene_logger.info("Initializing the menu scene")
        super().__init__(screen)
        self.player_options: list[str] = list()


    def load_initial_frame(self) -> None:
        try:
            menu_scene_logger.info("Banner is about to be created and positioned")
            self.banner = Banner()

            menu_scene_logger.info("GuildOptions is about to be created and positioned")
            self.guild_options = GuildOptions()

            self.objects.append(self.banner)
            self.objects.append(self.guild_options)

            menu_scene_logger.info("All menu scene objects are about to be added to the display")
            self.screen.draw(*self.objects)
        except Exception as e:
            e.add_note(f"Failed when loading the menu: {type(e)}")
            raise e


    def check_event(self, event: Event) -> None:
        if event.type == ANIMATE:
            menu_scene_logger.info("ANIMATE event generated")
            r = self.guild_options.vibrate_selection()
            self.screen.queue(r)
        elif event.type == QUIT:
            menu_scene_logger.info("QUIT event generated")
            exit()
        elif event.type == MOUSEBUTTONDOWN:
            menu_scene_logger.info("MOUSEBUTTONDOWN event generated")
            if event.button == 1:
                x, y = get_pos()
                print(f"X: {x}, Y: {y}")
        elif event.type == KEYDOWN:
            menu_scene_logger.info("KEYDOWN event generated")
            r = None
            if event.key == K_UP:
                r = self.guild_options.go("up")
            elif event.key == K_DOWN:
                r = self.guild_options.go("down")
            elif event.key == K_LEFT:
                r = self.guild_options.go("left")
            elif event.key == K_RIGHT:
                r = self.guild_options.go("right")
            elif event.key == K_z:
                hero = self.guild_options.select()
                self.player_options.append(hero)
                menu_scene_logger.info("%s was chosen", hero)
                if len(self.player_options) == 3:
                    raise EndOfScene()
            if r:
                for rect in r:
                    self.screen.queue(rect)


    def erase(self) -> None:
        menu_scene_logger.info("Erasing %s from the Menu scene", self.guild_options.name)
        r = self.guild_options.erase()
        self.screen.queue(r)
        menu_scene_logger.info("Erasing %s from the Menu scene", self.banner.name)
        r = self.banner.erase()
        self.screen.queue(r)
        # no need to erase the bg, it will be reused in the next scene
        # r = self.background.erase()
        # self.screen.queue(r)


    def terminate(self) -> list[str]:
        menu_scene_logger.info("Terminating the menu scene")
        self.objects.pop() # guild_options out
        self.objects.pop() # banner out
        # self.objects.pop() # background out
        return self.player_options
