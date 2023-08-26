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

        # 0, 1, 2
        self.state = 0


    def load_initial_frame(self, *args) -> None:
        heros = args
        self.heros = HeroBand(heros)
        self.enemies = EnemyBand()

        self.options = OptionsBox((600, 225))
        grid = Grid((50, 50), (100, 0), (2, 2))
        # self.idle = 
        self.actions = ActionOptions(grid, "Handjet")
        self.actions.camouflage = True
        box.add("idle", idle)
        box.add("actions", actions)
        # box.add("abilities", abilities)


    def draw_initial_frame(self) -> None:
        # self.background.draw(screen=self.screen)

        self.heros.move(("topleft", (230, 230))
        self.heros.draw(screen=self.screen, info="drawn onto main screen")

        self.enemies.move("topleft", (650, 270))
        self.enemies.draw(screen=self.screen, info="drawn onto main screen")

        self.options.move("topleft", (70, 470))
        self.options.draw(screen=self.screen, info="drawn onto main screen", addons="idle")

        #self.selector.draw(screen=self.screen)
        #self.keyboard.add_keydown(K_UP, MoveSelectorUp(self.selector))
        #self.keyboard.add_keydown(K_DOWN, MoveSelectorDown(self.selector))
        #self.keyboard.add_keydown(K_RETURN, SelectHero(self.keyboard, self.options))

        # removing the scene bg (it's the same as the Menu scene and it's already drawn)
        self.objects.pop()
        self.objects.append(self.options)
        self.objects.append(self.heros)
        self.objects.append(self.enemies)
        self.objects.append(self.selector)


    def erase(self) -> None:
        pass


    def choose_fighter_handler(self) -> None:
        pass


    def choose_action_handler(self, event: Event) -> None:
        if event.key == K_LEFT:
            self.actions.change_option(previous=True)
        elif event.key == K_RIGHT:
            self.actions.change_option()


    def choose_ability_handler(self) -> None:
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
                    if self.state == 0:
                        self.choose_fighter_handler(event)
                    elif self.state == 1:
                        self.choose_action_handler(event)
                    elif self.state == 2:
                        self.choose_ability_handler(event)

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
