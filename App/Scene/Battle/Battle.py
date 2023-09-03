from App.Object.Grid import Grid
from App.Scene.Battle.Locals.CharacterBand import HeroBand, EnemyBand
from App.Scene.Battle.Locals.CharacterSelector import CharacterSelector
from App.Scene.Battle.Locals.OptionsBox import OptionsBox, IDLE, HeroOptions, AbilityOptions, TargetOptions
from App.Scene.Battle.Locals.StatusBox import StatusBox
from App.Scene.Scene import Scene
from pygame.locals import K_z, K_UP, K_DOWN, K_LEFT, K_RIGHT, QUIT, MOUSEBUTTONDOWN, KEYDOWN
from pygame.surface import Surface
from pygame.event import clear, Event
from pygame.mouse import get_pos

class Battle(Scene):
    def __init__(self, screen: Surface):
        super().__init__(screen)

        # 0, 1, 2
        self.state = 0
        self.current_hero = None
        self.current_action = None
        self.current_ability = None
        self.current_target_selector = None
        self.turn_play: list[tuple[int|None,str|None,str|None,str|None]] = list()


    def load_initial_frame(self, *args) -> None:
        heros: list[str] = list(args)
        self.heros = HeroBand(heros)
        self.enemies = EnemyBand()

        size = 600, 225
        self.box = OptionsBox(size)
        self.idle = IDLE("Dosis")
        grid = Grid((50, 50), (300, 70), (2, 2))
        self.actions = HeroOptions(grid, "SourceCodePro")
        self.abilities = AbilityOptions(size, grid, "SourceCodePro")
        self.target = TargetOptions("Dosis")

        self.box.add("idle", self.idle)
        self.box.add("actions", self.actions)
        self.box.add("abilities", self.abilities)
        self.box.add("target", self.target)

        self.status = StatusBox((275, 225), self.heros, "Dosis")


    def draw_initial_frame(self) -> None:
        self.background.draw(screen=self.screen)

        self.heros.move("topleft", (230, 230))
        self.heros.draw(screen=self.screen, info="drawn onto main screen")

        self.enemies.move("topleft", (650, 270))
        self.enemies.draw(screen=self.screen, info="drawn onto main screen")

        self.selector = CharacterSelector(anchors=self.heros.get_addons_positions("midtop", mode="absolute"), displacement=(0, -10))
        self.selector.draw(screen=self.screen, info="drawn onto main screen")

        self.target_selector = CharacterSelector(anchors=self.enemies.get_addons_positions("midtop", mode="absolute"), displacement=(0, -10))

        self.box.move("bottomleft", (50, 725))
        self.idle.move("center", (int(self.box.rect.w/2), int(self.box.rect.h/2)))
        self.actions.move("topleft", (0, 0))
        self.abilities.move("topleft", (0, 0))
        self.target.move("center", (int(self.box.rect.w/2), int(self.box.rect.h/2)))

        addons = ["little_box_topleft", "little_box_topright", "little_box_bottomleft", "little_box_bottomright", "idle"]
        self.box.draw(screen=self.screen, info="drawn onto main screen", addons=addons)

        self.status.move("bottomleft", (675, 725))
        self.status.draw(self.screen, info="drawn onto main screen")

        # removing the scene bg (it's the same as the Menu scene and it's already drawn)
        self.objects.pop()
        self.objects.append(self.selector)
        self.objects.append(self.target_selector)
        self.objects.append(self.box)
        self.objects.append(self.heros)
        self.objects.append(self.enemies)
        self.objects.append(self.status)


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
            hero_index: int = int(self.selector.get_current_ref())
            return hero_index
        return None


    def choose_action_handler(self, event: Event) -> str | None:
        if event.key in (K_LEFT, K_RIGHT):
            if event.key == K_LEFT:
                self.actions.change_option(previous=True)
            elif event.key == K_RIGHT:
                self.actions.change_option()
        elif event.key == K_z:
            action_index = self.actions.arrow.get_current_ref()
            return str(action_index)
        return None


    def choose_ability_handler(self, event: Event) -> str | None:
        if event.key in (K_LEFT, K_RIGHT, K_UP, K_DOWN):
            if event.key == K_LEFT:
                self.abilities.change_option(previous=True)
            elif event.key == K_RIGHT:
                self.abilities.change_option(previous=False)
            elif event.key == K_UP:
                self.abilities.change_option(previous=True)
                self.abilities.change_option(previous=True)
            elif event.key == K_DOWN:
                self.abilities.change_option(previous=False)
                self.abilities.change_option(previous=False)
        elif event.key == K_z:
            ability = self.abilities.select()
            return ability
        return None


    def choose_target_selector_handler(self, event: Event) -> str | None:
        if event.key in (K_UP, K_DOWN):
            self.target_selector.erase("erased from main screen")
            if event.key == K_UP:
                self.target_selector.up()
            elif event.key == K_DOWN:
                self.target_selector.down()
            self.target_selector.draw(info="drawn onto main screen")
        elif event.key == K_z:
            enemyname = self.target_selector.get_current_ref()
            return enemyname
        return None


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
                            fighter = self.heros.addons[self.current_hero]
                            self.abilities.load(fighter, self.current_action)
                            self.box.draw(info="drawn onto mainscreen", addons="abilities")
                            self.state = 2
                    elif self.state == 2:
                        self.current_ability = self.choose_ability_handler(event)
                        if self.current_ability is not None:
                            erased_area = self.abilities.erase("erased from mainscreen")
                            self.box.update(erased_area)
                            number_keys = len(self.abilities.addons)
                            for addon in range(number_keys):
                                self.abilities.addons.popitem()
                            if self.current_action == "attack":
                                drawn_area = self.box.draw(info="drawn onto mainscreen", addons="target")
                                self.target_selector.draw(screen=self.screen, info="drawn onto main screen")
                                self.state = 3
                            else:
                                drawn_area = self.box.draw(info="drawn onto mainscreen", addons="idle")
                                self.current_target_selector = "self"
                                play = self.prepare_new_play()
                    elif self.state == 3:
                        self.current_target_selector = self.choose_target_selector_handler(event)
                        if self.current_target_selector is not None:
                            erased_area = self.target.erase("erased from mainscreen")
                            self.box.update(erased_area)
                            self.target_selector.erase(info="erased from main screen")
                            drawn_area = self.box.draw(info="drawn onto mainscreen", addons="idle")
                            self.prepare_new_play()
            clear()
        except Exception as err:
            err.add_note(f"Battle Scene failed at check_events: {type(err)=}")
            raise err


    def prepare_new_play(self) -> None:
        play = self.current_hero, self.current_action, self.current_ability, self.current_target_selector
        self.turn_play.append(play)
        self.current_hero = None
        self.current_action = None
        self.current_ability = None
        self.current_target_selector = None
        self.state = 0

    def terminate(self) -> list[str]:
        for obj in self.objects:
            obj.erase("erased from main screen")
        return ["Win", "Lose"]
