from App.Scene.Battle.Locals.FightingCharacter import FightingCharacter, create_fighter_image
from App.Object.BackgroundImage import BackgroundImage
from App.Object.Object import Object
from pygame.color import Color
from pygame.display import init, set_mode, update, list_modes, quit, set_caption
from pygame.event import Event, get, pump, poll, peek, clear, set_blocked, set_allowed, get_blocked
from pygame.locals import *
from pygame.mouse import get_pos
from pygame.rect import Rect
from pygame.surface import Surface
from pygame.time import Clock

"""
    This is a playground file
    It's intended to test things quickly and get a sense of new ideas
    I think this playground file alongside with the python REPL is a great tool to
    learn the basics and advance with slow pace on certain topics
"""

def new_obj() -> Object:
    #surf = Object((200, 200))
    #surf.surface.fill(Color(255, 0, 0))
    #surf.make_contour(Color(0, 255, 255), 3)

    #surf2 = Object((100,100))
    #surf2.surface.fill(Color(0, 255, 0))

    #surf3 = Object((50,50))
    #surf3.surface.fill(Color(0,0,255))
    #surf3.move("center", (50, 50))
    #surf2.move("center", (100, 100))
    #surf2.add("test2", surf3)
    #surf.add("test1", surf2)

    #surf.alias = "common rect"

    surf = create_fighter_image("Paladin")

    return surf

def main() -> None:
    init()
    set_caption("Introbattle")
    screen = set_mode((1024, 768))
    cl = Clock()

    set_blocked(None)
    set_allowed([MOUSEBUTTONDOWN, KEYDOWN, QUIT])
    surf = new_obj()
    background = BackgroundImage(screen.get_size())
    background.draw(screen=screen)

    while True:
        time_elapsed = cl.tick(30)
        if peek(QUIT):
            exit()
        elif peek(MOUSEBUTTONDOWN):
            l = poll()
            print(l)
            surf.move("center", l.pos)
            surf.camouflage = True
            surf.draw(screen, "drawn onto main screen")
        elif peek(KEYDOWN):
            k = poll()
            print(k)
            if not k == NOEVENT:
                if k.key == K_a:
                    surf.remove("test1", force_update=True)
                elif k.key == K_t:
                    surf.scale_by(2)
                elif k.key == K_e:
                    surf.erase("erased from main screen")
                elif k.key == K_p:
                    print(surf)
                elif k.key == K_b:
                    surf.addons["hp"].remove("right piece", pop=True, force_update=True)
                elif k.key == K_c:
                    surf.addons["hp"].remove("central piece", pop=True, force_update=True)
                elif k.key == K_r:
                    surf.erase()
                    surf.draw()
        else:
            pass
        clear()

if __name__ == "__main__":
    main()
