from App.Object.CharacterImage import PaladinImage, SkullImage
from App.Scene.End.Local.Banner import Banner
from App.Scene.Scene import Scene
from App.Setup.Globals import ANIMATE
from App.Screen import Screen
from pygame.event import Event
from pygame.constants import K_DOWN, K_LEFT, K_RIGHT, K_UP, KEYDOWN, QUIT

class End(Scene):
    def __init__(self, screen: Screen) -> None:
        super().__init__(screen)


    def load_initial_frame(self, *args) -> None:
        text = args[0]
        if not isinstance(text, str):
            raise Exception('In end scene: got something other than a str for banner')

        self.banner = Banner(text)
        self.hero = PaladinImage() if text == "Victory" else SkullImage()
        self.delta = 5

        self.screen.draw(self.hero)
        self.screen.draw(self.banner)


    def check_event(self, event: Event) -> None:
        if event.type == KEYDOWN:
            if event.key in [K_LEFT, K_RIGHT, K_DOWN, K_UP]:
                r = self.hero.erase()
                self.screen.queue(r)
                if event.key == K_LEFT:
                    self.hero.shift(-self.delta, 0)
                elif event.key == K_RIGHT:
                    self.hero.shift(self.delta, 0)
                elif event.key == K_UP:
                    self.hero.shift(0, -self.delta)
                else:
                    self.hero.shift(0, self.delta)
                _, r = self.hero.draw(self.screen.image)
                self.screen.queue(r)
        elif event.type == ANIMATE:
            _, r = self.hero.vibrate(self.screen.image)
            self.screen.queue(r)
        elif event.type == QUIT:
            exit()


    def terminate(self):
        pass


    def erase(self) -> None:
        pass
