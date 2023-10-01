from App.Font.Family import FontFamily
from App.Font.Pen import Pen
from App.Game import Game
from App.Object.CharacterImage import create_all_enemy_images
from App.Object.Fighter import Fighter, HunterFighter
from App.Object.Combat import Combat
from App.Object.Grid import Grid
from App.Object.Object import ImportedObject, SizedObject
from App.Object.Selector import DefaultSelector, Selector
from App.Object.Ability import Ability, AttackAbility
from App.Scene.Battle.Local.Box import Box
from App.Scene.Menu.Local.GuildOptions import GuildOptions
from App.Scene.Menu.Local.Banner import Banner
from App.Scene.Menu.Local.HeroPortrait import HeroPortrait
from App.Screen import Screen
from App.Setup.Globals import ANIMATE, GRAY, RED, SCREENSIZE, WHITE
from os.path import join
from pygame.event import clear, get, peek, poll, set_allowed, set_blocked, custom_type
from pygame.locals import KEYUP, KEYDOWN, K_LEFT, K_RIGHT, K_UP, K_DOWN, MOUSEBUTTONDOWN, MOUSEBUTTONUP, NOEVENT, QUIT, Color, K_a, K_b, K_c, K_d, K_e, K_f, K_g, K_h, K_j, K_k, K_l, K_z
from pygame.mouse import get_pos
from pygame.time import Clock, set_timer
from pygame.key import set_repeat
import tracemalloc


def main() -> None:
    tracemalloc.start(10)
    introbattle = Game(display_resolution=SCREENSIZE)
    introbattle.load_scenes()
    introbattle.run()
    tracemalloc.stop()


def test() -> None:
    screen = Screen(SCREENSIZE)
    fps = Clock()
    movement = 5

    set_timer(ANIMATE, 500)
    set_blocked(None)
    set_allowed([QUIT, KEYUP, KEYDOWN, MOUSEBUTTONUP, MOUSEBUTTONDOWN, ANIMATE])
    set_repeat(1000, int(1000/60)) # keys being pressed start generating KEYDOWN_PRESSED

    paladin = ImportedObject("paladin", join("App", "Resource", "Character", "Hero", "Paladin.png"))
    paladin.scale_by(1.5)

    hunter = Fighter("Hunter", 10, 10, 10, 10)
    hunter.move("center", (400, 300))

    grid = Grid(3, 3, (40, 40))
    grid.move("topleft", (200, 200))
    grid.coordinates[1][1] = None

    heros_grid = Grid(2, 3, (150, 100))
    heros_grid.move("center", (400, 300))
    heros_grid.coordinates[1][2] = None
    heros_grid.shift((50, 0), 1, None)

    sel = DefaultSelector(heros_grid, (0, -8))
    sel.select("midtop")

    banner = Banner()
    banner.move("bottomleft", (0, 600))

    portrait = HeroPortrait("Wizard")
    portrait2 = HeroPortrait("Hunter")
    anchors = heros_grid.get_positions("midtop")
    portrait.move("midtop", anchors[0])
    portrait2.move("midtop", anchors[1])

    enemies = create_all_enemy_images()
    enemies_grid = Grid(2, 1, (100, 100))
    enemies_grid.move("center", screen.image.get_rect().center)
    enemies_grid.shift((50, 0), line_index=1, column_index=None)
    anchors = enemies_grid.get_positions("midtop")
    enemy1 = enemies[0]
    enemy1.move("midtop", anchors[0])
    enemy2 = enemies[1]
    enemy2.move("midtop", anchors[1])

    g = GuildOptions()


    attacker = HunterFighter()
    attacker.move("center", (400, 300))
    defender = Fighter("Skull", 50, 50, 50, 50)
    defender.move("topright", screen.image.get_rect().topright)

    golpe_sujo = AttackAbility("golpe sujo", 5, 3)
    combat = Combat()


    pen = Pen(FontFamily("OpenSans"), "Regular", 24, WHITE)
    textos = ["Attack", "Defend", "Limonada", "Sabao"]
    anchors = Grid(2, 2, (200, 100))
    anchors.move("topleft", (50, 50))
    box = SizedObject("box", (500, 300))
    posicoes = anchors.get_positions("midleft")
    sel = DefaultSelector(anchors, (-10, 0))
    sel.tip = "midright"
    sel.rotate(90)
    sel.right()
    sel.select("midleft")
    box.image.fill(GRAY)
    for texto, posicao in zip(textos, posicoes):
        obj = pen.write(texto)
        obj.move("midleft", posicao)
        obj.draw(box.image)
    sel.draw(box.image)
    sel.drawn = False

    box = Box()
    box.move("topleft", (100, 100))
    ability1 = Ability("sabao", 12, 15)
    ability2 = Ability("bisnaga", 12, 15)
    ability3 = Ability("salamandra", 12, 15)
    #r = box.choose_action(["Attack", "Defend"])
    r = box.choose_ability([ability1, ability2, ability3])

    screen.draw(paladin, box)


    while True:

        fps.tick(60)
        #print(fps.get_fps())

        # for event in get():
        event = poll()

        if event.type == ANIMATE:
            s, r = paladin.vibrate(screen.image)
            screen.queue(r)
            r = hunter.vibrate_component("character")
            screen.queue(r)
            r = portrait.vibrate_component("hero")
            screen.queue(r)
        elif event.type == QUIT:
            exit()
        elif event.type == KEYUP:
            if g.drawn:
                if event.key == K_UP:
                    r = g.go("up")
                    screen.queue(r)
                elif event.key == K_DOWN:
                    r = g.go("down")
                    screen.queue(r)
                elif event.key == K_LEFT:
                    r = g.go("left")
                    screen.queue(r)
                elif event.key == K_RIGHT:
                    r = g.go("right")
                    screen.queue(r)
                elif event.key == K_z:
                    print(g.select())

            if hunter.drawn:
                if event.key == K_a:
                    screen.erase(hunter.name)
                elif event.key == K_b:
                    r = hunter.take_damage(4)
                    screen.queue(r)
                elif event.key == K_c:
                    r = hunter.cast_spell(8)
                    screen.queue(r)
                elif event.key == K_d:
                    r = hunter.spend_energy(7)
                    screen.queue(r)

            if attacker.drawn and defender.drawn:
                if event.key == K_e:
                    rects = combat.attack(attacker, defender, "Quickshot")
                    for r in rects:
                        screen.queue(r)


            if box.drawn:
                if event.key == K_f:
                    rects = box.motion("right")
                    #print(rects)
                    for rect in rects:
                        screen.queue(rect)
                if event.key == K_g:
                    rects = box.motion("down")
                    for rect in rects:
                        screen.queue(rect)
                if event.key == K_h:
                    # option_selected = box.select()
                    rects = box.choose_action(["Attack", "Defend"])
                    for rect in rects:
                        # o rect desse metodo tem que ser relativo
                        box.refresh(rect)
                        # o rect desse metodo tem que ser a posicao absoluta na tela
                        # eis a merda
                        # nao eh dificil resolver ('rect.move(...)'), mas sla
                        screen.queue(rect)
                    print(rects)

        elif event.type == KEYDOWN:
            if event.key in [K_UP, K_DOWN, K_LEFT, K_RIGHT]:
                if event.key == K_UP:
                    paladin.shift(0, -movement)
                elif event.key == K_DOWN:
                    paladin.shift(0, movement)
                elif event.key == K_LEFT:
                    paladin.shift(-movement, 0)
                else:
                    paladin.shift(movement, 0)
                screen.erase(paladin.name)
                screen.draw(paladin)
            elif event.key in [K_h, K_j, K_k, K_l]:
                if not sel.drawn:
                    continue
                r = sel.erase()
                screen.queue(r)
                if event.key == K_h:
                    sel.left()
                elif event.key == K_j:
                    sel.down()
                elif event.key == K_k:
                    sel.up()
                elif event.key == K_l:
                    sel.right()
                sel.select("midtop")
                _, r = sel.draw(screen.image)
                screen.queue(r)
        elif event.type == MOUSEBUTTONDOWN:
            x, y = get_pos()
            print(x, y)

        screen.update()


if __name__ == "__main__":
    #main()
    test()
