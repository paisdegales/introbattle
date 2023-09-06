from pygame.color import Color
from App.Font.Family import FontFamily
from App.Object.Object import BaseObject


class Pen():
    def __init__(self, family: FontFamily, style: str, size: int, text_color: Color, background_color: Color | None = None, area: tuple[int, int] | None = None, vertex: str = "center"):
        self.family = family
        self.style = style
        self.size = size
        self.text_color = text_color
        self.background_color = background_color
        self.area = area
        self.vertex = vertex


    def write(self, text: str) -> BaseObject:
        surface = self.family.render(self.style, text, self.size, self.text_color, self.background_color, self.area, self.vertex)
        return BaseObject(text, surface)
