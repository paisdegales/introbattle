from App.Screen import Screen
from App.Scene.Scene import Scene
from App.Scene.Battle.Local.CharacterBand import HeroBand, EnemyBand
from App.Scene.Battle.Local.Box import Box
from App.Scene.Battle.Local.Combat import Combat
from App.Setup.Globals import ANIMATE, GRAY, RED, SCREENSIZE, WHITE
from pygame.locals import K_z, K_UP, K_DOWN, K_LEFT, K_RIGHT, QUIT, MOUSEBUTTONDOWN, KEYDOWN, KEYUP, K_RETURN
from pygame.event import Event
from pygame.mouse import get_pos
from enum import Enum


class BattlePhase(Enum):
    SELECTING_HERO = 0
    SELECTING_ACTION = 1
    SELECTING_ABILITY = 2
    SELECTING_ENEMY = 3
    BATTLE_TIME = 4


class Battle(Scene):
    def __init__(self, screen: Screen):
        super().__init__(screen)

        self.state: BattlePhase = BattlePhase.SELECTING_HERO
        self.next_phase = True
        self.chosen_hero = None
        self.chosen_action = None
        self.chosen_ability = None
        self.chosen_target = None
        self.combat = Combat()


    def load_initial_frame(self, *args) -> None:
        self.box = Box()
        self.box.move("bottomleft", (0, SCREENSIZE[1]))
        self.box.shift(50, -50)

        heros: list[str] = list(args)
        self.heros = HeroBand(heros)
        self.heros.move("topleft", (240, 80))

        enemies = ["Skull", "Mage", "Skull"]
        self.enemies = EnemyBand(enemies)
        self.enemies.move("topleft", (600, 80))

        self.objects.pop()
        self.objects.append(self.box)
        self.objects.append(self.heros)
        self.objects.append(self.enemies)

        self.screen.draw(*self.objects)


    def erase(self) -> None:
        raise NotImplementedError()


    def check_event(self, event: Event) -> None:
        if event.type == QUIT:
            exit()
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = get_pos()
                print(f"X: {x}, Y: {y}")
                return

        if self.next_phase:
            rects = list()
            match self.state:
                case BattlePhase.SELECTING_HERO:
                    rects = self.box.next_state()
                case BattlePhase.SELECTING_ACTION:
                    rects = self.box.next_state(["Attack", "Defense", "Action 3", "Action 4"])
                case BattlePhase.SELECTING_ABILITY:
                    action = "attacks" if self.chosen_action == "Attack" else "defenses"
                    d = getattr(self.chosen_hero, action)
                    abilities = d.values()
                    rects = self.box.next_state(abilities)
                case BattlePhase.SELECTING_ENEMY:
                    rects = self.box.next_state()
                case _:
                    raise Exception('Unknown battle state')
            for rect in rects:
                _, rect = self.box.refresh(rect)
                self.screen.queue(rect)
            self.next_phase = False
            return 

        # if the code gets pass the last if statement,
        # then no phase-transition is made and we can 
        # test for keyboard/mouse events related to the battle itself
        match self.state:
            case BattlePhase.SELECTING_HERO:
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        self.chosen_hero = self.heros.select()
                        self.state = BattlePhase.SELECTING_ACTION
                        self.next_phase = True
                    if event.key in [K_UP, K_DOWN]:
                        rects: list[Rect] = list()
                        if event.key == K_UP:
                            rects = self.heros.go("up")
                        else:
                            rects = self.heros.go("down")
                        for rect in rects:
                            _, rect = self.heros.refresh(rect)
                            self.screen.queue(rect)
            case BattlePhase.SELECTING_ACTION:
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        self.chosen_action = self.box.select()
                        self.state = BattlePhase.SELECTING_ABILITY
                        self.next_phase = True
                    if event.key in [K_UP, K_DOWN, K_LEFT, K_RIGHT]:
                        rects: list[Rect] = list()
                        if event.key == K_UP:
                            rects = self.box.go("up")
                        elif event.key == K_DOWN:
                            rects = self.box.go("down")
                        elif event.key == K_LEFT:
                            rects = self.box.go("left")
                        else:
                            rects = self.box.go("right")
                        for rect in rects:
                            _, rect = self.box.refresh(rect)
                            self.screen.queue(rect)
            case BattlePhase.SELECTING_ABILITY:
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        self.chosen_ability = self.box.select()
                        self.state = BattlePhase.SELECTING_ENEMY
                        self.next_phase = True
                    if event.key in [K_UP, K_DOWN, K_LEFT, K_RIGHT]:
                        rects: list[Rect] = list()
                        if event.key == K_UP:
                            rects = self.box.go("up")
                        elif event.key == K_DOWN:
                            rects = self.box.go("down")
                        elif event.key == K_LEFT:
                            rects = self.box.go("left")
                        else:
                            rects = self.box.go("right")
                        for rect in rects:
                            _, rect = self.box.refresh(rect)
                            self.screen.queue(rect)
            case BattlePhase.SELECTING_ENEMY:
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        self.chosen_enemy = self.enemies.select()
                        self.state = BattlePhase.BATTLE_TIME
                    if event.key in [K_UP, K_DOWN]:
                        rects: list[Rect] = list()
                        if event.key == K_UP:
                            rects = self.enemies.go("up")
                        else:
                            rects = self.enemies.go("down")
                        for rect in rects:
                            _, rect = self.enemies.refresh(rect)
                            self.screen.queue(rect)
            case BattlePhase.BATTLE_TIME:
                rects = self.combat.act(self.chosen_hero, self.chosen_ability, self.chosen_enemy, None)  
                _, rect = self.heros.refresh(rects[-2])
                self.screen.queue(rect)
                _, rect = self.enemies.refresh(rects[-1])
                self.screen.queue(rect)
                self.state = BattlePhase.SELECTING_HERO
                self.next_phase = True
            case _:
                raise Exception("Unmatched state in battle scene")


    def terminate(self) -> list[str]:
        raise NotImplementedError()
