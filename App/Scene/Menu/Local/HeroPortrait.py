from App.Object.Object import Object
from App.Object.CharacterImage import create_character_image
from App.Setup.Globals import LIGHT_GRAY, GRAY, DARK_GRAY, WHITE, BLACK
from App.Font.Family import FontFamily
from pygame.surface import Surface

class HeroPortrait(Object):
    def __init__(self, heroname: str, font_family: str):
        w, h = 100, 100
        lbox = 8
        wbar, hbar = w, lbox

        image = Object((w, h))
        image.fill(LIGHT_GRAY)

        topbar = Object((wbar, hbar))
        topbar.fill(GRAY)
        image.add("topbar", "topleft", topbar, (0, 0), None)

        little_box = Object((lbox, lbox))
        little_box.fill(LIGHT_GRAY)
        little_box.make_contour(DARK_GRAY, 3)
        little_box = little_box.to_surface()
        image.add("little_box_topleft", "topleft", little_box, (0, 0), None)
        image.add("little_box_topright", "topright", little_box, (w, 0), None)
        image.add("little_box_bottomleft", "bottomleft", little_box, (0, h), None)
        image.add("little_box_bottomright", "bottomright", little_box, (w, h), None)

        hero = create_character_image(heroname)
        hero_surf = hero.to_surface()
        image.add("hero", "center", hero_surf, (w/2, h/2), None)

        font = FontFamily(font_family)
        text: Surface = font.render("Regular", hero.name, 22, WHITE)
        text_w, text_h = text.get_size()

        super().__init__((w, h + text_h))
        self.set_colorkey(BLACK)
        self.add("image", "topleft", image, (0, 0), None)
        self.add("text", "midtop", text, (w/2, h), None)
