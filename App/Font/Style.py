from App.Setup.Globals import folders
from pygame.font import Font, get_init, init
from pygame.color import Color
from pygame.surface import Surface
from logging import warning

class FontStyle():
    """
        Basic interface to manage new font styles
    """
    def __init__(self, family_name: str, style_name: str, file_extension: str = ".ttf", size: int = 12) -> None:
        if get_init() == False:
            init()

        self.family_name = family_name
        self.style_name = style_name
        filename = style_name + file_extension
        self.path = folders.get_filepath(family_name, filename)
        self.size = size

    @property
    def size(self) -> int:
        return self.__size

    @size.setter
    def size(self, size: int) -> None:
        try:
            self.font = Font(self.path, size)
            self.__size = size
        except Exception as e:
            warning(f"Failed when loading {self.style_name} of {self.family_name} from {self.path}")
            raise e

    def render(self, text: str, text_color: Color, background_color: Color | None = None) -> Surface:
        return self.font.render(text, True, text_color, background_color)

    def get_render_size(self, text: str) -> tuple[int, int]:
        return self.font.size(text)
