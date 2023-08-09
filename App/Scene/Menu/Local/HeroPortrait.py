from App.Object.Object import Object
from App.Object.CharacterImage import create_character_image
from App.Setup.Globals import LIGHT_GRAY, GRAY, DARK_GRAY, WHITE, BLACK
from App.Font.Family import FontFamily
from pygame.surface import Surface
from pygame.rect import Rect
from pygame import SRCALPHA

class HeroPortrait(Object):
    def __init__(self, heroname: str, font_family: str):
        self.font = FontFamily(font_family)

        image = self.load_image(heroname)
        text = self.load_text("Regular")

        text_w, text_h = text.get_size()
        super().__init__((self.w, self.h + text_h))
        self.alias = "{} portrait".format(self.hero.name)
        """
        explanation for why this surface should set the colorkey to black, but
        it cannot do it at the same time: 'super().__init__()' creates a proxy
        of 'Object' (the parent class of self) and calls its initializer, which
        in turn implicitly calls Surface(). This method creates a black
        rectangle by default, and the black color can be set transparent if the
        colorkey is set to black. Eventhough ideal, this cannot be done because
        setting the whole rectangle to transparent makes the 'erase' method for
        addons useless. Explanation for this: the 'erasor' attr is created when
        'draw' is called, by copying the surface's screen and keeping track of
        what would be beneath the surface to be drawn. For addons, the screen
        would be the Object's surface itself, but if this surface is transparent,
        then the 'erasor' is also gonna be transparent, thus not erasing a thing
        when needed.
        """
        # self.set_colorkey(BLACK)
        self.add("image", "topleft", image, (0, 0), None)
        self.add("text", "midtop", text, (self.w/2, self.h), None)


    def load_image(self, heroname: str) -> Object:
        self.w, self.h = 100, 100
        lbox = 8
        wbar, hbar = self.w, lbox

        image = Object((self.w, self.h))
        image.fill(LIGHT_GRAY)

        topbar = Object((wbar, hbar))
        topbar.fill(GRAY)
        image.add("topbar", "topleft", topbar, (0, 0), None)

        little_box = Object((lbox, lbox))
        little_box.fill(LIGHT_GRAY)
        little_box.make_contour(DARK_GRAY, 3)
        little_box = little_box.to_surface()
        image.add("little_box_topleft", "topleft", little_box, (0, 0), None)
        image.add("little_box_topright", "topright", little_box, (self.w, 0), None)
        image.add("little_box_bottomleft", "bottomleft", little_box, (0, self.h), None)
        image.add("little_box_bottomright", "bottomright", little_box, (self.w, self.h), None)

        self.hero = create_character_image(heroname)
        hero_surf = self.hero.to_surface()
        image.add("hero", "center", hero_surf, (self.w/2, self.h/2), None)

        return image


    def load_text(self, style: str) -> Surface:
        text: Surface = self.font.render(style, self.hero.name, 22, WHITE)

        return text


    def highlight_text(self):
        self.remove("text", pop=True, force_update=True)
        text = self.load_text("Bold")
        self.add("text", "midtop", text, (self.w/2, self.h), None)


    def unhighlight_text(self):
        self.remove("text", pop=True, force_update=False)
        text = self.load_text("Regular")
        self.add("text", "midtop", text, (self.w/2, self.h), None)
