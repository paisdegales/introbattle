from App.Font.Family import FontFamily
from App.Object.CharacterImage import create_character_image
from App.Object.Object import Object
from App.Scene.Menu.Local.Positioning import HEROPORTRAIT_IMAGESIZE, HEROPORTRAIT_LITTLEBOX_SIDE
from App.Setup.Globals import LIGHT_GRAY, GRAY, DARK_GRAY, WHITE

class HeroPortrait(Object):
    def __init__(self, heroname: str, font_family: str):
        self.font = FontFamily(font_family)

        image = self.load_image(heroname)
        image.move("topleft", (0, 0))
        text = self.load_text("Regular")
        text.move("midtop", (image.rect.w/2, image.rect.h))

        super().__init__((image.rect.w, image.rect.h + text.rect.h))
        self.alias = "{} portrait".format(self.hero.name)
        self.add("image", image)
        self.add("text", text)


    def load_image(self, heroname: str) -> Object:
        w, h = HEROPORTRAIT_IMAGESIZE
        lbox = HEROPORTRAIT_LITTLEBOX_SIDE
        wbar, hbar = w, lbox

        image = Object((w, h))
        image.surface.fill(LIGHT_GRAY)

        topbar = Object((wbar, hbar))
        topbar.surface.fill(GRAY)
        topbar.move("topleft", (0, 0))

        little_box_topleft = Object((lbox, lbox))
        little_box_topleft.surface.fill(LIGHT_GRAY)
        little_box_topleft.make_contour(DARK_GRAY, 3)
        little_box_topleft.move("topleft", (0, 0))

        little_box_topright = Object((lbox, lbox))
        little_box_topright.surface.fill(LIGHT_GRAY)
        little_box_topright.make_contour(DARK_GRAY, 3)
        little_box_topright.move("topright", (w, 0))

        little_box_bottomleft = Object((lbox, lbox))
        little_box_bottomleft.surface.fill(LIGHT_GRAY)
        little_box_bottomleft.make_contour(DARK_GRAY, 3)
        little_box_bottomleft.move("bottomleft", (0, h))

        little_box_bottomright = Object((lbox, lbox))
        little_box_bottomright.surface.fill(LIGHT_GRAY)
        little_box_bottomright.make_contour(DARK_GRAY, 3)
        little_box_bottomright.move("bottomright", (w, h))

        hero = create_character_image(heroname)
        hero.move("center", image.rect.center)
        self.hero = hero

        image.add("topbar", topbar)
        image.add("little_box_topleft", little_box_topleft)
        image.add("little_box_topright", little_box_topright)
        image.add("little_box_bottomleft", little_box_bottomleft)
        image.add("little_box_bottomright", little_box_bottomright)
        image.add("hero", hero)

        return image


    def load_text(self, style: str) -> Object:
        text = self.font.render(style, self.hero.name, 22, WHITE)
        text = Object(surface=text)

        return text


    def highlight_text(self):
        self.remove("text", pop=True, force_update=True)
        text = self.load_text("Bold")
        text.move("midtop", (self.rect.w/2, self.addons["image"].rect.h))
        self.add("text", text)


    def unhighlight_text(self):
        self.remove("text", pop=True, force_update=True)
        text = self.load_text("Regular")
        text.move("midtop", (self.rect.w/2, self.addons["image"].rect.h))
        self.add("text", text)
