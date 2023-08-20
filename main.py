# from App.Game import Game
from App.Object.Object import Object
from pygame.display import init, set_mode, update, list_modes, quit
from pygame.event import Event, get, pump, poll, peek, clear, set_blocked, set_allowed, get_blocked
from pygame.time import Clock
from pygame.locals import K_a, K_u, K_e, K_t, K_p, QUIT, K_RETURN, MOUSEBUTTONDOWN, KEYDOWN, NOEVENT
from pygame.mouse import get_pos
from pygame.rect import Rect
from pygame.surface import Surface
from pygame.color import Color

def new_obj() -> Object:
    surf = Object((200, 200))
    surf.surface.fill(Color(255, 0, 0))
    surf.make_contour(Color(0, 255, 255), 3)

    surf2 = Object((100,100))
    surf2.surface.fill(Color(0, 255, 0))

    surf3 = Object((50,50))
    surf3.surface.fill(Color(0,0,255))
    surf3.move("center", (50, 50))
    surf2.move("center", (100, 100))
    surf2.add("test2", surf3)
    surf.add("test1", surf2)

    surf.alias = "common rect"

    return surf

def main() -> None:
    # introbattle = Game(display_resolution=(1024, 768))
    # introbattle.load_scenes()
    # introbattle.run()

    init()
    print("Available sizes", list_modes())
    if (1280, 1024) in list_modes():
        print("Choosing 1280x1024")
        screen = set_mode((1280, 1024))
    cl = Clock()

    set_blocked(None)
    set_allowed([MOUSEBUTTONDOWN, KEYDOWN, QUIT])
    surf = new_obj()

    while True:
        time_elapsed = cl.tick(30)
        if peek(QUIT):
            exit()
        elif peek(MOUSEBUTTONDOWN):
            l = poll()
            print(l)
            surf.move("center", l.pos)
            surf.draw(screen, "drawn onto main screen")
        elif peek(KEYDOWN):
            k = poll()
            print(k)
            if not k == NOEVENT:
                if k.key == K_a:
                    surf.remove("test1", force_update=True)
                    #pass
                elif k.key == K_u:
                    surf.undo()
                elif k.key == K_e:
                    surf.erase("erased from main screen")
                elif k.key == K_t:
                    surf.toggle()
                elif k.key == K_p:
                    print(surf)
        else:
            #print(get())
            pass
        clear()


if __name__ == "__main__":
    main()
