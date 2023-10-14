from App.Screen import Screen
from App.Scene.Scene import Scene, EndOfScene
from App.Scene.Menu.Menu import Menu
from App.Scene.Battle.Battle import Battle
from App.Setup.Globals import ANIMATE
from pygame.locals import KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEBUTTONUP, QUIT
from pygame.time import Clock, set_timer
from pygame.event import poll, set_blocked, set_allowed
from pygame.key import set_repeat
from logging import warning


class Game:
    def __init__(self, display_resolution: tuple[int, int], fps: int = 30) -> None:
        self.screen = Screen(display_resolution)
        self.scenes: list[Scene] = list()
        self.clock = Clock()
        self.fps = fps

    def load_scenes(self) -> None:
        self.scenes.append(Menu(self.screen))
        self.scenes.append(Battle(self.screen))
    
    def run(self) -> None:
        if len(self.scenes) == 0:
            warning("No game scenes available. The game won't start.")
            return

        # creating and setting a custom type to manage animations
        set_timer(ANIMATE, 500)
        # blocking all event types pygame has
        set_blocked(None)
        # allowing only a few types
        set_allowed([QUIT, KEYUP, KEYDOWN, MOUSEBUTTONUP, MOUSEBUTTONDOWN, ANIMATE])
        # keys being pressed start generating KEYDOWN_PRESSED
        set_repeat(1000, int(1000/60))

        scene_output: list  = list()
        #scene_output = ["Paladin", "Wizard", "Hunter"]
        for scene in self.scenes:
            # the output of the last scene serves as input to the next scene
            scene_input = scene_output
            scene.load_initial_frame(*scene_input)
            #print(scene)
            scene_output.clear()
            while True:
                self.clock.tick(self.fps)
                event = poll()
                try:
                    scene.check_event(event)
                except EndOfScene as e:
                    info = e.args
                    #print(info)
                    break
                except Exception as e:
                    raise e
                self.screen.update()
            scene_output = scene.terminate()
            scene.erase()
