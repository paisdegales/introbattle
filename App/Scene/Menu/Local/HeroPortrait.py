from App.Font.Family import FontFamily
from App.Font.Pen import Pen
from App.Object.CharacterImage import create_character_image
from App.Object.Object import SizedObject
from App.Scene.Menu.Local.Locals import HEROPORTRAIT_IMAGESIZE, HEROPORTRAIT_LITTLEBOX_SIDE
from App.Setup.Globals import GRAY, DARK_GRAY, WHITE
from App.Setup.Utils import menu_scene_heroportrait_logger as logger


class HeroPortrait(SizedObject):
    def __init__(self, heroname: str):
        logger.info("%s's portrait image is going to be created...", heroname)
        self.hero = create_character_image(heroname)
        if self.hero is None:
            raise Exception(f"HeroPortrait failed when creating {heroname} image")

        logger.info("%s's portrait title is going to be created...", heroname)
        self.pen = Pen(FontFamily("OpenSans"), "Regular", 24, WHITE)
        self.text = self.pen.write(self.hero.name)

        logger.info("%s's portrait itself is going to be created...", heroname)
        name = "{} portrait".format(self.hero.name)
        super().__init__(name, HEROPORTRAIT_IMAGESIZE)

        logger.info("%s's portrait background is going to be created...", heroname)
        self.hero_bg = SizedObject("hero_bg", (self.rect.w, self.rect.h - self.text.rect.h))
        self.hero_bg.move("topleft", (0, 0))
        self.hero_bg.image.fill(GRAY)

        logger.info("%s's portrait little decorations are going to be created...", heroname)
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

        logger.info("moving and drawing the %s's portrait background (no display just yet)", heroname)
        self.hero_bg.draw(self.image)

        logger.info("moving and drawing the %s's portrait image (no display just yet)", heroname)
        self.hero.move("center", self.hero_bg.rect.center)
        self.hero.draw(self.image)

        logger.info("moving and drawing the %s's portrait title (no display just yet)", heroname)
        self.text.move("center", (int(self.rect.w/2), self.rect.h - int(self.text.rect.h/2)))
        self.text.draw(self.image)
