from App.Screen import Screen
from App.Scene.Scene import Scene
from App.Scene.Battle.Local.CharacterBand import HeroBand, EnemyBand
from App.Scene.Battle.Local.Box import Box
from App.Scene.Battle.Local.Combat import Combat
from App.Scene.Battle.Local.BattlePhase import BattlePhase
from App.Setup.Globals import ANIMATE, SCREENSIZE 
from pygame.locals import K_z, K_UP, K_DOWN, K_LEFT, K_RIGHT, QUIT, MOUSEBUTTONDOWN, KEYDOWN
from pygame.event import Event
from pygame.mouse import get_pos


class Battle(Scene):
    def __init__(self, screen: Screen):
        super().__init__(screen)

        self.chosen_hero = None
        self.chosen_action = None
        self.chosen_ability = None
        self.chosen_target = None
        self.turn_packer = list()
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
        elif event.type == ANIMATE:
            match self.box.state:
                case BattlePhase.SELECTING_HERO:
                    pass
                case BattlePhase.SELECTING_ENEMY:
                    pass
        elif event.type == KEYDOWN:
            match self.box.state:
                case BattlePhase.SELECTING_HERO:
                    if event.key == K_z:
                        choose_hero(self)
                    elif event.key == K_UP:
                        move_hero_indicator(self, "up")
                    elif event.key == K_DOWN:
                        move_hero_indicator(self, "down")
                case BattlePhase.SELECTING_ACTION:
                    if event.key == K_z:
                        choose_action(self)
                    elif event.key in [K_UP, K_DOWN, K_LEFT, K_RIGHT]:
                        if event.key == K_UP:
                            move_action_indicator(self, "up")
                        elif event.key == K_DOWN:
                            move_action_indicator(self, "down")
                        elif event.key == K_LEFT:
                            move_action_indicator(self, "left")
                        else:
                            move_action_indicator(self, "right")
                case BattlePhase.SELECTING_ABILITY:
                    if event.key == K_z:
                        choose_ability(self)
                    elif event.key in [K_UP, K_DOWN, K_LEFT, K_RIGHT]:
                        if event.key == K_UP:
                            move_ability_indicator(self, "up")
                        elif event.key == K_DOWN:
                            move_ability_indicator(self, "down")
                        elif event.key == K_LEFT:
                            move_ability_indicator(self, "left")
                        else:
                            move_ability_indicator(self, "right")
                case BattlePhase.SELECTING_ENEMY:
                    if event.key == K_z:
                        choose_enemy(self)
                    elif event.key in [K_UP, K_DOWN]:
                        if event.key == K_UP:
                            move_enemy_indicator(self, "up")
                        else:
                            move_enemy_indicator(self, "down")
                case BattlePhase.BATTLE_TIME:
                    pack = (self.chosen_hero, self.chosen_action, self.chosen_ability, self.chosen_enemy)
                    self.turn_packer.append(pack)

                    if len(self.turn_packer) == 3:
                        for pack in self.turn_packer:
                            self.chosen_hero, self.chosen_action, self.chosen_ability, self.chosen_enemy = pack
                            if self.chosen_enemy is not None:
                                rects = self.combat.attack(self.chosen_hero, self.chosen_enemy, self.chosen_ability)  
                                _, rect = self.heros.refresh(rects[0])
                                self.screen.queue(rect)
                                _, rect = self.enemies.refresh(rects[1])
                                self.screen.queue(rect)
                            else:
                                rect = self.combat.defend(self.chosen_hero, self.chosen_ability)
                                _, rect = self.heros.refresh(rect)
                                self.screen.queue(rect)
                        self.chosen_action = None
                        self.chosen_ability = None
                        self.chosen_hero = None
                        self.chosen_enemy = None
                        self.turn_packer.clear()
                    rects = self.box.set_state(BattlePhase.SELECTING_HERO)
                    for rect in rects:
                        _, rect = self.box.refresh(rect)
                        self.screen.queue(rect)


    def terminate(self) -> list[str]:
        raise NotImplementedError()




def choose_hero(scene: Battle) -> None:
    scene.chosen_hero = scene.heros.select()
    chosen_heros = map(lambda x: x[0], scene.turn_packer)

    if scene.chosen_hero in chosen_heros:
        return

    rects = scene.box.set_state(BattlePhase.SELECTING_ACTION, ["Attack", "Defend", "Use Item", "Pass"])
    for rect in rects:
        _, rect = scene.box.refresh(rect)
        scene.screen.queue(rect)



def move_hero_indicator(scene: Battle, direction: str) -> None:
    rects = scene.heros.go(direction)
    for rect in rects:
        _, rect = scene.heros.refresh(rect)
        scene.screen.queue(rect)



def choose_action(scene: Battle) -> None:
    if scene.chosen_hero is None:
        return

    scene.chosen_action = scene.box.select()

    if scene.chosen_action == "Attack":
        abilities = scene.chosen_hero.attacks.values()
    else:
        abilities = scene.chosen_hero.defenses.values()

    rects = scene.box.set_state(BattlePhase.SELECTING_ABILITY, abilities)
    for rect in rects:
        _, rect = scene.box.refresh(rect)
        scene.screen.queue(rect)



def move_action_indicator(scene: Battle, direction: str) -> None:
    rects = scene.box.go(direction)
    for rect in rects:
        _, rect = scene.box.refresh(rect)
        scene.screen.queue(rect)



def choose_ability(scene: Battle) -> None:
    scene.chosen_ability = scene.box.select()
    rects = list()
    if scene.chosen_action == "Attack":
        rects = scene.box.set_state(BattlePhase.SELECTING_ENEMY)
    elif scene.chosen_action == "Defend":
        scene.chosen_enemy = None
        rects = scene.box.set_state(BattlePhase.BATTLE_TIME)
    for rect in rects:
        _, rect = scene.box.refresh(rect)
        scene.screen.queue(rect)



def move_ability_indicator(scene: Battle, direction: str) -> None:
    rects = scene.box.go(direction)
    for rect in rects:
        _, rect = scene.box.refresh(rect)
        scene.screen.queue(rect)



def choose_enemy(scene: Battle) -> None:
    scene.chosen_enemy = scene.enemies.select()
    scene.box.set_state(BattlePhase.BATTLE_TIME)



def move_enemy_indicator(scene: Battle, direction: str) -> None:
    rects = scene.enemies.go(direction)
    for rect in rects:
        _, rect = scene.enemies.refresh(rect)
        scene.screen.queue(rect)
