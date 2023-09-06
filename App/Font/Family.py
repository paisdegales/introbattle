from pygame.font import init, get_init
from pygame.color import Color
from pygame.surface import Surface
from App.Font.Style import FontStyle

class FontFamily():
    """
        Class responsible for all font families used in this project (OpenSans, Arial ...)
    """
    def __init__(self, family_name: str) -> None:
        if get_init() == False:
            init()

        self.family_name = family_name
        self.styles: dict[str, FontStyle] = dict()

    def load_style(self, style_name: str, style_size: int) -> None:
        if style_name not in self.styles.keys():
            self.styles[style_name] = FontStyle(self.family_name, style_name, size=style_size)
        else:
            self.styles[style_name].size = style_size

    def render(self, style: str, text: str, font_size: int, text_color: Color, background_color: Color | None = None, area: tuple[int,int] | None = None, vertex: str = "center") -> Surface:
        try:
            self.load_style(style, font_size)
        except Exception as e:
            print(f"Failed when attempting to write '{text}'! Failed to fetch/use '{style}'! Make sure the stylename is right and its file exists")
            raise e

        return self.styles[style].render(text, text_color, background_color, area, vertex)


    def get_render_size(self, style: str, text: str, font_size: int) -> tuple[int, int]:
        try:
            self.load_style(style, font_size)
        except Exception as e:
            print(e.args, type(e))
            raise e

        return self.styles[style].get_render_size(text)
