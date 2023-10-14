from App.Font.Family import FontFamily
from App.Font.Pen import Pen
from App.Game import Game
from App.Scene.Battle.Local.Combat import Combat
from App.Object.CharacterImage import create_all_enemy_images
from App.Object.Fighter import Fighter, HunterFighter, PaladinFighter, SkullFighter
from App.Object.Grid import Grid
from App.Object.Object import ImportedObject, SizedObject
from App.Object.Selector import DefaultSelector, Selector
from App.Object.Ability import Ability, AttackAbility
from App.Scene.Battle.Local.Box import Box
from App.Scene.Battle.Local.CharacterBand import EnemyBand, HeroBand
from App.Scene.Menu.Local.GuildOptions import GuildOptions
from App.Scene.Menu.Local.Banner import Banner
from App.Scene.Menu.Local.HeroPortrait import HeroPortrait
from App.Screen import Screen
from App.Setup.Globals import ANIMATE, GRAY, RED, SCREENSIZE, WHITE
from pygame.event import clear, get, peek, poll, set_allowed, set_blocked, custom_type
from pygame.mouse import get_pos
from pygame.time import Clock, set_timer
from pygame.key import set_repeat
from pygame.rect import Rect
from pygame.locals import KEYUP, KEYDOWN, K_LEFT, K_RIGHT, K_UP, K_DOWN, \
MOUSEBUTTONDOWN, MOUSEBUTTONUP, NOEVENT, QUIT, Color, K_a, K_b, K_c, K_d, K_e, \
K_f, K_g, K_h, K_j, K_k, K_l, K_z, K_p, K_RETURN
from enum import Enum
from os.path import join


def main() -> None:
    introbattle = Game(display_resolution=SCREENSIZE)
    introbattle.load_scenes()
    introbattle.run()


class BattlePhase(Enum):
    SELECTING_HERO = 0
    SELECTING_ACTION = 1
    SELECTING_ABILITY = 2
    SELECTING_ENEMY = 3
    BATTLE_TIME = 4


def test_combat() -> None:
    screen = Screen(SCREENSIZE)
    fps = Clock()

    set_timer(ANIMATE, 500)
    set_blocked(None)
    set_allowed([QUIT, KEYUP, KEYDOWN, MOUSEBUTTONUP, MOUSEBUTTONDOWN, ANIMATE])
    set_repeat(1000, int(1000/60)) # keys being pressed start generating KEYDOWN_PRESSED

    box = Box()
    box.move("bottomleft", (0, SCREENSIZE[1]))
    box.shift(50, -50)

    heros = HeroBand(["Hunter", "Wizard", "Priest"])
    heros.move("topleft", (240, 80))

    enemies = EnemyBand(["Skull", "Mage", "Paladin"])
    enemies.move("topleft", (600, 80))

    combat = Combat()
    screen.draw(box, heros, enemies)
    state = BattlePhase.SELECTING_HERO
    next_phase = True

    while True:

        fps.tick(60)
        #print(fps.get_fps())

        event = poll()
        if event.type == ANIMATE:
            pass
        elif event.type == QUIT:
            exit()
        elif event.type == KEYUP:
            if event.key == K_a:
                pass
            elif event.key == K_b:
                pass
            elif event.key == K_c:
                pass
            elif event.key == K_d:
                pass
        elif event.type == KEYDOWN:
            pass
        elif event.type == MOUSEBUTTONDOWN:
            x, y = get_pos()
            print(x, y)

        if next_phase:
            rects = list()
            match state:
                case BattlePhase.SELECTING_HERO:
                    rects = box.next_state()
                case BattlePhase.SELECTING_ACTION:
                    rects = box.next_state(["Attack", "Defense", "Action 3", "Action 4"])
                case BattlePhase.SELECTING_ABILITY:
                    action = "attacks" if action_chosen == "Attack" else "defenses"
                    d = getattr(hero_chosen, action)
                    abilities = d.values()
                    rects = box.next_state(abilities)
                case BattlePhase.SELECTING_ENEMY:
                    rects = box.next_state()
                case _:
                    raise Exception('Unknown battle state')
            for rect in rects:
                _, rect = box.refresh(rect)
                screen.queue(rect)
            next_phase = False
            screen.update()
            continue


        match state:
            case BattlePhase.SELECTING_HERO:
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        hero_chosen = heros.select()
                        state = BattlePhase.SELECTING_ACTION
                        next_phase = True
                    if event.key in [K_UP, K_DOWN]:
                        rects: list[Rect] = list()
                        if event.key == K_UP:
                            rects = heros.go("up")
                        else:
                            rects = heros.go("down")
                        for rect in rects:
                            _, rect = heros.refresh(rect)
                            screen.queue(rect)
            case BattlePhase.SELECTING_ACTION:
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        action_chosen = box.select()
                        state = BattlePhase.SELECTING_ABILITY
                        next_phase = True
                    if event.key in [K_UP, K_DOWN, K_LEFT, K_RIGHT]:
                        rects: list[Rect] = list()
                        if event.key == K_UP:
                            rects = box.go("up")
                        elif event.key == K_DOWN:
                            rects = box.go("down")
                        elif event.key == K_LEFT:
                            rects = box.go("left")
                        else:
                            rects = box.go("right")
                        for rect in rects:
                            _, rect = box.refresh(rect)
                            screen.queue(rect)
            case BattlePhase.SELECTING_ABILITY:
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        ability_chosen = box.select()
                        state = BattlePhase.SELECTING_ENEMY
                        next_phase = True
                    if event.key in [K_UP, K_DOWN, K_LEFT, K_RIGHT]:
                        rects: list[Rect] = list()
                        if event.key == K_UP:
                            rects = box.go("up")
                        elif event.key == K_DOWN:
                            rects = box.go("down")
                        elif event.key == K_LEFT:
                            rects = box.go("left")
                        else:
                            rects = box.go("right")
                        for rect in rects:
                            _, rect = box.refresh(rect)
                            screen.queue(rect)
            case BattlePhase.SELECTING_ENEMY:
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        enemy_chosen = enemies.select()
                        state = BattlePhase.BATTLE_TIME
                    if event.key in [K_UP, K_DOWN]:
                        rects: list[Rect] = list()
                        if event.key == K_UP:
                            rects = enemies.go("up")
                        else:
                            rects = enemies.go("down")
                        for rect in rects:
                            _, rect = enemies.refresh(rect)
                            screen.queue(rect)
            case BattlePhase.BATTLE_TIME:
                rects = combat.act(hero_chosen, ability_chosen, enemy_chosen, None)  

                _, rect = heros.refresh(rects[-2])
                screen.queue(rect)

                _, rect = enemies.refresh(rects[-1])
                screen.queue(rect)

                state = BattlePhase.SELECTING_HERO
                next_phase = True

        screen.update()


if __name__ == "__main__":
    #main()
    test_combat()
