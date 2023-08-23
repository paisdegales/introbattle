from App.Object.BackgroundImage import BackgroundImage
from App.Scene.Battle.Locals.CharacterBand import HeroBand, EnemyBand
from App.Scene.Battle.Locals.CharacterSelector import CharacterSelector
from App.Scene.Battle.Locals.Events import *
from App.Scene.Battle.Locals.OptionsBox import OptionsBox
from App.Scene.Scene import Scene
from pygame.locals import K_z, K_UP, K_DOWN, K_LEFT, K_RIGHT, QUIT, MOUSEBUTTONDOWN, KEYDOWN
from pygame.surface import Surface
from pygame.event import poll, peek, clear, set_blocked, set_allowed, get as get_events

class Battle(Scene):
    def __init__(self, screen: Surface):
        super().__init__(screen)


    def load_initial_frame(self, *args) -> None:
        heros = args
        self.heros = HeroBand(heros)
        self.enemies = EnemyBand()
        self.options = OptionsBox(self.screen)

        self.selector = CharacterSelector(self.heros.get_positions(), (0, -10))


        #obj = AssembledUserInterfaceImage("introcomp_balao 1.png")
        #obj.move("topleft", (500, 500))
        #obj.screen = self.screen
        #self.obj = obj
        #health = HealthBar()
        #health.move("topleft", (600, 600))
        #health.screen = self.screen
        #health.draw()



    def draw_initial_frame(self) -> None:
        self.background.draw(screen=self.screen)
        self.options.draw()
        self.heros.draw(screen=self.screen)
        self.enemies.draw(screen=self.screen)

        self.selector.draw(screen=self.screen)
        self.keyboard.add_keydown(K_UP, MoveSelectorUp(self.selector))
        self.keyboard.add_keydown(K_DOWN, MoveSelectorDown(self.selector))
        self.keyboard.add_keydown(K_RETURN, SelectHero(self.keyboard, self.options))

        # removing the scene bg (it's the same as the Menu scene and it's already drawn)
        self.objects.pop()
        self.objects.append(self.options)
        self.objects.append(self.heros)
        self.objects.append(self.enemies)
        self.objects.append(self.selector)

        #self.obj.draw(transparent=True)


    def erase(self) -> None:
        pass


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
            err.add_note(f"Battle Scene failed at check_events: {type(err)=}")
            raise err


    def terminate(self) -> list[str]:
        pass


    def __str__(self) -> str:
        string = list()
        string.append("Battle Scene Overview:")
        for obj in self.objects:
            string.append(obj.__str__())
        string = "\n".join(string)
        return string
