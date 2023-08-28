from App.Scene.Battle.Locals.FightingCharacter import FightingCharacter, create_fighter_image
from App.Scene.Battle.Locals.OptionsBox import OptionsBox, HeroOptions
from App.Scene.Battle.Locals.CharacterBand import HeroBand, EnemyBand
from App.Scene.Battle.Locals.CharacterSelector import CharacterSelector
from App.Object.BackgroundImage import BackgroundImage
from App.Object.Object import Object
from App.Object.Grid import Grid
from pygame.color import Color
from pygame.display import init, set_mode, update, list_modes, quit, set_caption
from pygame.event import Event, get, pump, poll, peek, clear, set_blocked, set_allowed, get_blocked, event_name
from pygame.locals import *
from pygame.mouse import get_pos
from pygame.rect import Rect
from pygame.surface import Surface
from pygame.time import Clock
from pygame.key import name as keyname

"""
    This is a playground file
    It's intended to test things quickly and get a sense of new ideas
    I think this playground file alongside with the python REPL is a great tool to
    learn the basics and advance with slow pace on certain topics
"""

def main() -> None:
    init()
    set_caption("Introbattle")
    screen = set_mode((1024, 768))
    cl = Clock()
    set_blocked(None)
    set_allowed([MOUSEBUTTONDOWN, KEYDOWN, QUIT])
    background = BackgroundImage(screen.get_size())
    background.draw(screen=screen)


    objs = list()

    while True:
        time_elapsed = cl.tick(30)

        if peek(QUIT):
            exit()
        elif peek(MOUSEBUTTONDOWN):
            k = poll()
            print(k)
            if k.button == 1:
                box = OptionsBox((600, 225))
                box.move("topleft", k.pos)
                grid = Grid((50, 50), (100, 0), (2, 2))
                actions = HeroOptions(grid, "Handjet")
                actions.camouflage = True
                arrow = actions.addons["arrow"]

                box.add("actions", actions)
                box.draw(screen, "drawn onto main screen")
                objs.append(box)
                objs.append(grid)
                objs.append(actions)
            else:
                pass
        elif peek(KEYDOWN):
            k = poll()
            if not k == NOEVENT:
                print(keyname(k.key), k)
                if k.key == K_a:
                    pass
                elif k.key == K_t:
                    print(box)
                    if arrow.drawn:
                        erased_area = actions.remove("arrow")
                        drawn_area = actions.update(erased_area)
                        box.update(drawn_area)
                    else:
                        arrow.draw(info="drawn onto actions's surface")
                        drawn_area = actions.update(arrow.drawn_area)
                        box.update(drawn_area)
                elif k.key == K_e:
                    for obj in objs:
                        if isinstance(obj, Object):
                            obj.erase("erased from main screen")
                        del obj
                elif k.key == K_b:
                    pass
                elif k.key == K_c:
                    pass
                elif k.key == K_r:
                    area = box.remove("actions")
                    box.update(area)
                elif k.key == K_p:
                    print(get_pos())
                elif k.key == K_RIGHT:
                    actions.change_option()
                elif k.key == K_LEFT:
                    actions.change_option(previous=True)
                elif k.key == K_RETURN:
                    print(actions.select())
        else:
            pass

        clear()

if __name__ == "__main__":
    main()
