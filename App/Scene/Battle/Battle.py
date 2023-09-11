from App.Screen import Screen
from App.Scene.Battle.Locals.CharacterBand import HeroBand, EnemyBand
from App.Scene.Battle.Locals.OptionsBox import OptionsBox
from App.Scene.Battle.Locals.StatusBox import StatusBox
from App.Scene.Scene import Scene
from pygame.locals import K_z, K_UP, K_DOWN, K_LEFT, K_RIGHT, QUIT, MOUSEBUTTONDOWN, KEYDOWN
from pygame.event import Event
from pygame.mouse import get_pos


class Battle(Scene):
    def __init__(self, screen: Screen):
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

        self.status = StatusBox((275, 225), self.heros, "Dosis")

        self.heros.move("topleft", (230, 230))
        self.heros.draw(self.screen.screen)

        self.enemies.move("topleft", (650, 270))
        self.enemies.draw(self.screen.screen)

        self.box.move("bottomleft", (50, 725))
        self.box.draw(screen=self.screen)

        self.status.move("bottomleft", (675, 725))
        self.status.draw(self.screen)

        # removing the scene bg (it's the same as the Menu scene and it's already drawn)
        self.objects.pop()
        self.objects.append(self.box)
        self.objects.append(self.heros)
        self.objects.append(self.enemies)
        self.objects.append(self.status)


    def erase(self) -> None:
        pass


    def check_events(self, event: Event) -> None:
        if event.type == QUIT:
            exit()
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = get_pos()
                print(f"X: {x}, Y: {y}")
        elif event.type == KEYDOWN:
            pass


    def terminate(self) -> list[str]:
        for obj in self.objects:
            obj.erase("erased from main screen")
        return ["Win", "Lose"]
