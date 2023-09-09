from pygame.draw import line
from App.Font.Family import FontFamily
from App.Font.Pen import Pen
from App.Object.CharacterImage import create_character_image
from App.Object.Object import SizedObject
from App.Setup.Globals import BLACK, GRAY, DARK_GRAY, WHITE


class HeroPortrait(SizedObject):
    def __init__(self, heroname: str):
        self.hero = create_character_image(heroname)
        if self.hero is None:
            raise Exception(f"HeroPortrait failed when creating {heroname} image")

        self.pen = Pen(FontFamily("OpenSans"), "Regular", 24, BLACK)
        self.text = self.pen.write(self.hero.name)

        line_width = 3
        padding = line_width + 5
        name = "{} portrait".format(self.hero.name)
        content_width = max(self.hero.rect.w, self.text.rect.w) 
        content_height = self.hero.rect.h + self.text.rect.h
        size = content_width + 2*padding, content_height + 2*padding

        super().__init__(name, size)
        self.image.fill(GRAY)
        line(self.image, WHITE, (line_width, line_width), (size[0]+line_width, line_width), width=2)
        self.make_contour(DARK_GRAY, line_width)
        self.move("topleft", (padding, padding))

        self.hero.move("midtop", (padding+int(content_width/2), padding))
        self.hero.draw(self.image)
        self.text.move("midtop", self.hero.rect.midbottom)
        self.text.draw(self.image)
