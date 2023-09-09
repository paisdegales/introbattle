# from App.Game import Game
from os.path import join
from pygame.event import clear, get, peek, poll, set_allowed, set_blocked
from pygame.locals import KEYUP, KEYDOWN, K_LEFT, K_RIGHT, K_UP, K_DOWN, MOUSEBUTTONDOWN, MOUSEBUTTONUP, NOEVENT, QUIT, Color, K_a, K_b, K_c, K_d, K_e, K_h, K_j, K_k, K_l
from pygame.mouse import get_pos
from pygame.time import Clock
from pygame.key import set_repeat
from App.Object.Fighter import Fighter
from App.Object.Grid import Grid
from App.Object.Object import ImportedObject
from App.Object.Selector import DefaultSelector, Selector
from App.Scene.Menu.Local.GuildOptions import GuildOptions
from App.Scene.Menu.Local.HeroPortrait import HeroPortrait
from App.Screen import Screen
from App.Setup.Globals import SCREENSIZE

def main() -> None:
    pass
    # introbattle = Game(display_resolution=(1024, 768))
    # introbattle.load_scenes()
    # introbattle.run()

if __name__ == "__main__":
    main()

screen = Screen(SCREENSIZE)
fps = Clock()

movement = 5
bio = -2
dead_frames = 0


set_blocked(None)
set_allowed([QUIT, KEYUP, KEYDOWN, MOUSEBUTTONUP, MOUSEBUTTONDOWN])
set_repeat(1000, int(1000/60)) # keys being pressed start generating KEYDOWN_PRESSED


paladin = ImportedObject("paladin", join("App", "Resource", "Character", "Hero", "Paladin.png"))
paladin.scale_by(1.5)

hunter = Fighter("Hunter", 10, 10, 10)
hunter.move("center", (400, 300))

grid = Grid(3, 3, (40, 40))
grid.move("topleft", (200, 200))
grid.coordinates[1][1] = None
#print(grid)

heros_grid = Grid(2, 3, (150, 100))
heros_grid.move("center", (400, 300))
heros_grid.coordinates[1][2] = None
heros_grid.shift((50, 0), 1, None)
#print(heros_grid)

sel = DefaultSelector(heros_grid, (0, -8))
sel.select("midtop")

portrait = HeroPortrait("Wizard")
portrait2 = HeroPortrait("Hunter")
anchors = heros_grid.get_positions("midtop")
portrait.move("midtop", anchors[0])
portrait2.move("midtop", anchors[1])

g = GuildOptions((200, 200))
screen.draw(paladin, g)

while True:

    fps.tick(60)
    #print(fps.get_fps())

    # for event in get():
    event = poll()

    if event.type == NOEVENT:
        if dead_frames >= 30:
            bio *= -1
            s, r = paladin.vibrate(screen.screen)
            screen.queue(r)
            r = hunter.vibrate_component("character")
            screen.queue(r)
            dead_frames = 0
        dead_frames+=1
    elif event.type == QUIT:
        exit()
    elif event.type == KEYUP:
        if not hunter.drawn:
            continue
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
            _, r = sel.draw(screen.screen)
            screen.queue(r)
    elif event.type == MOUSEBUTTONDOWN:
        x, y = get_pos()
        print(x, y)

    screen.update()
