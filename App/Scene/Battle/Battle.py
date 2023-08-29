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
        self.current_hero = None
        self.current_action = None
        self.current_ability = None


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
        self.background.draw(screen=self.screen)

        self.heros.move("topleft", (230, 230))
        self.heros.draw(screen=self.screen, info="drawn onto main screen")

        self.enemies.move("topleft", (650, 270))
        self.enemies.draw(screen=self.screen, info="drawn onto main screen")

        self.selector = CharacterSelector(anchors=self.heros.get_addons_positions("midtop", mode="absolute"), displacement=(0, -10))
        self.selector.draw(screen=self.screen, info="drawn onto main screen")

        self.box.move("bottomleft", (50, 725))
        self.idle.move("center", (self.box.rect.w/2, self.box.rect.h/2))
        self.actions.move("topleft", (0, 0))

        addons = ["little_box_topleft", "little_box_topright", "little_box_bottomleft", "little_box_bottomright", "idle"]
        self.box.draw(screen=self.screen, info="drawn onto main screen", addons=addons)

        # removing the scene bg (it's the same as the Menu scene and it's already drawn)
        self.objects.pop()
        self.objects.append(self.selector)
        self.objects.append(self.box)
        self.objects.append(self.heros)
        self.objects.append(self.enemies)


    def erase(self) -> None:
        pass


    def choose_fighter_handler(self, event: Event) -> int | None:
        if event.key in (K_UP, K_DOWN):
            self.selector.erase("erased from main screen")
            if event.key == K_UP:
                self.selector.up()
            elif event.key == K_DOWN:
                self.selector.down()
            self.selector.draw(info="drawn onto main screen")
        elif event.key == K_z:
            hero_index: int = self.selector.get_current_ref()
            return hero_index
        return None


    def choose_action_handler(self, event: Event) -> str | None:
        if event.key in (K_LEFT, K_RIGHT):
            if event.key == K_LEFT:
                self.actions.change_option(previous=True)
            elif event.key == K_RIGHT:
                self.actions.change_option()
        elif event.key == K_z:
            action_index: int = self.actions.arrow.get_current_ref()
            return action_index
        return None


    def choose_ability_handler(self, event: Event) -> None:
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
                    # STATES COULD BE BETTER MANAGED.
                    # MAYBE CREATE SOME ADDTIONAL METHODS TO TAKE CARE OF CHANGING STATES
                    if self.state == 0:
                        self.current_hero = self.choose_fighter_handler(event)
                        if self.current_hero is not None:
                            erased_area = self.idle.erase("erased from mainscreen")
                            self.box.update(erased_area)
                            self.box.draw(info="drawn onto mainscreen", addons="actions")
                            self.state = 1
                    elif self.state == 1:
                        self.current_action = self.choose_action_handler(event)
                        if self.current_action is not None:
                            erased_area = self.actions.erase("erased from mainscreen")
                            self.box.update(erased_area)
                            # self.box.draw(info="drawn onto mainscreen", addons="abilities")
                            # self.state = 2
                    elif self.state == 2:
                        self.choose_ability_handler(event)
                        self.state = 0

            clear()
        except Exception as err:
            err.add_note(f"Battle Scene failed at check_events: {type(err)=}")
            raise err


    def terminate(self) -> list[str]:
        pass
