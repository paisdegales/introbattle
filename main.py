# from App.Game import Game
from pygame.display import update
from pygame.event import clear, get, peek, poll, set_allowed, set_blocked
from pygame.locals import KEYUP, KEYDOWN, K_LEFT, K_RIGHT, K_UP, K_DOWN, MOUSEBUTTONDOWN, MOUSEBUTTONUP, NOEVENT, QUIT, Color, K_a, K_b, K_c, K_d, K_e
from pygame.rect import Rect
from pygame.mouse import get_pos
from pygame.time import Clock
from pygame.key import set_repeat
from App.Object.Fighter import Fighter
from App.Screen import Screen
from App.Object.CharacterImage import PaladinImage
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


# paladin = ImportedObject("paladin", join("App", "Resource", "Character", "Hero", "Paladin.png"))
# paladin.scale_by(1.5)
paladin = PaladinImage()
hunter = Fighter("Hunter", 10, 10, 10)
hunter.move("topleft", (200, 200))

rects = screen.draw(paladin, hunter)
update(rects)

while True:

    fps.tick(60)
    #print(fps.get_fps())

    # for event in get():
    event = poll()

    if event.type == NOEVENT:
        if dead_frames >= 30:
            bio *= -1
            # pos = paladin.rect.topleft
            # paladin.move("topleft", (pos[0] + bio, pos[1] + bio))
            # erased.extend(screen.erase(paladin.name))
            # drawn.extend(screen.draw(paladin))
            r = hunter.vibrate("staminabar")
            #hunter.shift(bio, bio)
            screen.erase(hunter.name)
            screen.draw(hunter)
            dead_frames = 0
        dead_frames+=1
    elif event.type == QUIT:
        exit()
    elif event.type == KEYUP:
        if event.key == K_a:
            area = hunter.take_damage(3)
            screen.refresh(hunter.name, area)
        elif event.key == K_b:
            area = hunter.cast_spell(4)
            screen.refresh(hunter.name, area)
        elif event.key == K_c:
            area = hunter.spend_energy(8)
            screen.refresh(hunter.name, area)
        elif event.key == K_d:
            screen.erase(hunter.name)
        elif event.key == K_e:
            pass
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

