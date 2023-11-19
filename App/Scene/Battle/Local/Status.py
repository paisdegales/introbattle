from App.Object.Grid import Grid
from App.Object.Object import SizedObject
from App.Scene.Battle.Local.CharacterBand import CharacterBand
from App.Scene.Battle.Local.Locals import STATUS_FONTFAMILY, STATUS_FONTSIZE, STATUS_SIZE 
from App.Setup.Globals import GRAY, GREEN, RED, WHITE
from App.Font.Pen import Pen
from App.Font.Family import FontFamily
from pygame.rect import Rect


class Status(SizedObject):
    def __init__(self, band: CharacterBand):
        super().__init__("Status box", STATUS_SIZE)
        self.band = band
        number_fighters = len(self.band.fighters)
        spacing = STATUS_SIZE[0], int(STATUS_SIZE[1]/number_fighters)
        self.grid = Grid(number_fighters, 1, spacing)


    def update(self) -> Rect:
        rect = self.image.fill(GRAY)
        self.make_contour(WHITE, 5)

        align = "center"
        positions = self.grid.get_positions(align)

        for fighter, position in zip(self.band.fighters, positions):
            if fighter.alive:
                writing_color = GREEN
            else:
                writing_color = RED
            pen = Pen(FontFamily(STATUS_FONTFAMILY), "Regular", STATUS_FONTSIZE, writing_color)
            text = "* {} {}/{} {}/{} *".format(fighter.name, fighter.hp.value, fighter.hp.max, fighter.mp.value, fighter.mp.max)
            obj = pen.write(text)
            obj.move(align, position)
            obj.draw(self.image)

        return rect

