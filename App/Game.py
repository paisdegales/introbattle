from App.Screen.Screen import Screen
from App.Scene.Scene import Scene
from App.Scene.Menu.Menu import Menu
from App.Scene.Battle.Battle import Battle
from App.Screen.GameEvent import EndOfScene
from pygame.time import Clock
from logging import warning
from time import sleep

class Game:
    def __init__(self, display_resolution: tuple[int, int], fps: int = 30, flags: int = 0) -> None:
        self.screen = Screen().new_display(display_resolution, flags)
        self.scenes: list[Scene] = list()
        self.clock = Clock()
        self.fps = fps

    def load_scenes(self) -> None:
        self.scenes.append(Menu(self.screen))
        #self.scenes.append(Battle(self.screen))
    
    def run(self) -> None:
        if len(self.scenes) == 0:
            warning("No game scenes available. The game won't start.")
            return

        scene_output = list()
        #scene_output = ["Paladin", "Wizard", "Hunter"]
        for scene in self.scenes:
            # the output of the last scene serves as input to the next scene
            scene_input = scene_output
            scene.load_initial_frame(*scene_input)
            scene.draw_initial_frame()
            #print(scene)
            scene_output.clear()

            while True:
                try:
                    scene.check_events()
                except EndOfScene as e:
                    info = e.args
                    #print(info)
                    break
                except Exception as e:
                    raise e

                self.clock.tick(self.fps)

            scene_output = scene.terminate()
            scene.erase()
