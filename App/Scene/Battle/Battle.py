from App.Object.BackgroundImage import BackgroundImage
from App.Object.Grid import Grid
from App.Scene.Battle.Locals.CharacterBand import HeroBand, EnemyBand
from App.Scene.Battle.Locals.CharacterSelector import CharacterSelector
from App.Scene.Battle.Locals.OptionsBox import OptionsBox, IDLE, HeroOptions 
from App.Scene.Scene import Scene
from pygame.locals import K_z, K_UP, K_DOWN, K_LEFT, K_RIGHT, QUIT, MOUSEBUTTONDOWN, KEYDOWN
from pygame.surface import Surface
from pygame.event import poll, peek, clear, set_blocked, set_allowed, get as get_events, Event
from pygame.mouse import get_pos

class Battle(Scene):
    def __init__(self, screen: Surface):
        super().__init__(screen)

        # 0, 1, 2
        self.state = 0


    def load_initial_frame(self, *args) -> None:
        heros = args
        self.heros = HeroBand(heros)
        self.enemies = EnemyBand()

        self.idle = IDLE("Dosis")

        grid = Grid((50, 50), (300, 0), (2, 2))
        self.actions = HeroOptions(grid, "SourceCodePro")

        self.box = OptionsBox((600, 225))
        self.box.add("idle", self.idle)
        self.box.add("actions", self.actions)
        # box.add("abilities", abilities)


    def draw_initial_frame(self) -> None:
        # self.background.draw(screen=self.screen)

        self.heros.move("topleft", (230, 230))
        self.heros.draw(screen=self.screen, info="drawn onto main screen")

        self.enemies.move("topleft", (650, 270))
        self.enemies.draw(screen=self.screen, info="drawn onto main screen")

        self.box.move("bottomleft", (50, 725))
        self.idle.move("center", (self.box.rect.w/2, self.box.rect.h/2))
        self.actions.move("topleft", (0, 0))

        addons = ["little_box_topleft", "little_box_topright", "little_box_bottomleft", "little_box_bottomright", "actions"]
        self.box.draw(screen=self.screen, info="drawn onto main screen", addons=addons)

        # removing the scene bg (it's the same as the Menu scene and it's already drawn)
        self.objects.pop()
        self.objects.append(self.box)
        self.objects.append(self.heros)
        self.objects.append(self.enemies)


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
