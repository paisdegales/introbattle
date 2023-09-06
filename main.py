# from App.Game import Game
from os.path import join
from pygame.event import clear, get, peek, poll, set_allowed, set_blocked
from pygame.locals import KEYUP, KEYDOWN, K_LEFT, K_RIGHT, K_UP, K_DOWN, MOUSEBUTTONDOWN, MOUSEBUTTONUP, NOEVENT, QUIT, Color, K_a, K_b, K_c, K_d, K_e
from pygame.mouse import get_pos
from pygame.time import Clock
from pygame.key import set_repeat
from App.Object.Fighter import Fighter
from App.Object.Object import ImportedObject
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
screen.draw(paladin, hunter)

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
    elif event.type == MOUSEBUTTONDOWN:
        x, y = get_pos()
        print(x, y)

    screen.update()
