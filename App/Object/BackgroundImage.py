from App.Object.Image import Image
from App.Setup.Globals import folders

class BackgroundImage(Image):
    def __init__(self, size: tuple[int, int]):
        w, h = size
        filename = f"{w}x{h}.png"
        super().__init__("Background", filename)
