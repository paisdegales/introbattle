from App.Game import Game
from App.Scene.Menu.Local.Banner import Banner
from App.Scene.Menu.Local.HeroPortrait import HeroPortrait
from App.Scene.Menu.Local.GuildOptions import GuildOptions
from App.Scene.Menu.Local.Selector import MenuSelector
from App.Object.BackgroundImage import BackgroundImage
from App.Scene.Menu.Local.Positioning import *
from App.Object.Grid import Grid
from App.Scene.Menu.Local.GuildOptions import GuildOptions
from App.Object.Object import Object
from pygame.display import init, set_mode, update, list_modes, quit
from pygame.event import Event, get, pump, poll, peek, clear, set_blocked, set_allowed, get_blocked
from pygame.time import Clock
from pygame.locals import *
# from pygame.locals import K_a, K_u, K_e, K_t, K_p, QUIT, K_RETURN, MOUSEBUTTONDOWN, KEYDOWN, NOEVENT
from pygame.mouse import get_pos
from pygame.rect import Rect
from pygame.surface import Surface
from pygame.color import Color

def new_obj() -> Object:
    # surf = Object((200, 200))
    # surf.surface.fill(Color(255, 0, 0))
    # surf.make_contour(Color(0, 255, 255), 3)

    # surf2 = Object((100,100))
    # surf2.surface.fill(Color(0, 255, 0))

    # surf3 = Object((50,50))
    # surf3.surface.fill(Color(0,0,255))
    # surf3.move("center", (50, 50))
    # surf2.move("center", (100, 100))
    # surf2.add("test2", surf3)
    # surf.add("test1", surf2)

    # surf.alias = "common rect"

    #surf = Banner("OpenSans")
    #surf.load("Introbattle!", size=(280, 80), vertex="center")
    #surf.move(*BANNER_POSITION)
    #surf.camouflage = False

    #surf = HeroPortrait("Priest", "Dosis")
    #surf.move("center", (100, 100))

    surf = GuildOptions()
    #grid = Grid((0, 0), (50, 50), (200, 200), (3, 3))
    #grid.get_coords(True)

    return surf

def test() -> None:
    init()
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
            #surf.move("center", l.pos)
            #surf.draw(screen, "drawn onto main screen")
            surf.draw(screen)
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
        else:
            pass
        clear()



def main() -> None:
    introbattle = Game(display_resolution=(1024, 768))
    introbattle.load_scenes()
    introbattle.run()

if __name__ == "__main__":
    main()
