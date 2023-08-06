from App.Screen.Screen import Screen
from App.Scene.Scene import Scene
from App.Scene.Menu.Menu import Menu
from pygame.time import Clock
from logging import warning

class Game:
    def __init__(self, display_resolution: tuple[int, int], fps: int = 30, flags: int = 0) -> None:
        self.screen = Screen().new_display(display_resolution, flags)
        self.scenes: list[Scene] = list()
        self.clock = Clock()
        self.fps = fps

    def load_scenes(self) -> None:
        self.scenes.append(Menu(self.screen))
    
    def run(self) -> None:
        if len(self.scenes) == 0:
            warning("No game scenes available. The game won't start.")
            return

        for scene in self.scenes:
            scene.load_initial_frame()
            scene.draw_initial_frame()

            while True:
                try:
                    scene.check_events()
                except Exception as e:
                    raise e

                self.clock.tick(self.fps)

            scene.erase()
