from App.Font.Family import FontFamily
from App.Font.Pen import Pen
from App.Object.Object import BaseObject
from App.Scene.Menu.Local.Positioning import    \
            BANNER_BGCOLOR, BANNER_FONTCOLOR,   \
            BANNER_FONTSIZE, BANNER_POSITION,   \
            BANNER_SIZE, BANNER_TEXT,           \
            BANNER_FONTFAMILY


class Banner(BaseObject):
    def __init__(self):
        self.pen = Pen(FontFamily(BANNER_FONTFAMILY), "BoldItalic", BANNER_FONTSIZE, BANNER_FONTCOLOR, BANNER_BGCOLOR, BANNER_SIZE, "center")
        surface = self.pen.write(BANNER_TEXT)
        super().__init__("Game banner", surface.image)
        self.make_contour(BANNER_FONTCOLOR, 3)
        self.move(*BANNER_POSITION)
