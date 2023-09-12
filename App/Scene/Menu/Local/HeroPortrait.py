from App.Font.Family import FontFamily
from App.Font.Pen import Pen
from App.Object.CharacterImage import create_character_image
from App.Object.Object import BaseObject, SizedObject
from App.Scene.Menu.Local.Positioning import HEROPORTRAIT_IMAGESIZE, HEROPORTRAIT_LITTLEBOX_SIDE
from App.Setup.Globals import GRAY, DARK_GRAY, WHITE
from pygame.rect import Rect


class HeroPortrait(SizedObject):
    def __init__(self, heroname: str):
        self.hero = create_character_image(heroname)
        if self.hero is None:
            raise Exception(f"HeroPortrait failed when creating {heroname} image")

        self.pen = Pen(FontFamily("OpenSans"), "Regular", 24, WHITE)
        self.text = self.pen.write(self.hero.name)

        name = "{} portrait".format(self.hero.name)
        super().__init__(name, HEROPORTRAIT_IMAGESIZE)

        self.hero_bg = SizedObject("hero_bg", (self.rect.w, self.rect.h - self.text.rect.h))
        self.hero_bg.move("topleft", (0, 0))
        self.hero_bg.image.fill(GRAY)

        decoration = SizedObject("little box", (HEROPORTRAIT_LITTLEBOX_SIDE, HEROPORTRAIT_LITTLEBOX_SIDE))
        decoration.image.fill(GRAY)
        decoration.make_contour(DARK_GRAY, 4)
        decoration.move("topleft", self.hero_bg.rect.topleft)
        decoration.draw(self.hero_bg.image)
        decoration.drawn = False
        decoration.move("topright", self.hero_bg.rect.topright)
        decoration.draw(self.hero_bg.image)
        decoration.drawn = False
        decoration.move("bottomright", self.hero_bg.rect.bottomright)
        decoration.draw(self.hero_bg.image)
        decoration.drawn = False
        decoration.move("bottomleft", self.hero_bg.rect.bottomleft)
        decoration.draw(self.hero_bg.image)
        decoration.drawn = False

        self.hero_bg.draw(self.image)

        self.hero.move("center", self.hero_bg.rect.center)
        self.hero.draw(self.image)

        self.text.move("center", (int(self.rect.w/2), self.rect.h - int(self.text.rect.h/2)))
        self.text.draw(self.image)
