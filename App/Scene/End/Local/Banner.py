from App.Font.Family import FontFamily
from App.Font.Pen import Pen
from App.Object.Object import BaseObject
from App.Scene.End.Local.Locals import     \
            BANNER_BGCOLOR, BANNER_FONTCOLOR,   \
            BANNER_FONTSIZE, BANNER_SIZE,       \
            BANNER_FONTFAMILY, SCREENSIZE


class Banner(BaseObject):
    def __init__(self, text: str):
        self.pen = Pen(FontFamily(BANNER_FONTFAMILY), "BoldItalic", BANNER_FONTSIZE, BANNER_FONTCOLOR, BANNER_BGCOLOR, BANNER_SIZE, "center")
        surface = self.pen.write(text)
        super().__init__("Gameover banner", surface.image)
        self.make_contour(BANNER_FONTCOLOR, 3)
        x, y = SCREENSIZE
        x, y = x//2, y//2
        self.move("center", (x, y))

