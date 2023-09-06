from App.Object.Object import ImportedObject
from App.Setup.Globals import bgpath

class BackgroundImage(ImportedObject):
    def __init__(self, size: tuple[int, int]):
        w, h = size
        filename = f"{w}x{h}.png"
        super().__init__("Background", bgpath(filename))
