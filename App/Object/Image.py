from App.Object.Object import Object
from App.Setup.Globals import folders
from pygame.image import load
from pygame.surface import Surface

class Image(Object):
    def __init__(self, foldername: str, filename: str, *args):
        if not folders.file_exists(foldername, filename):
            raise Exception(f"{filename} not found in {foldername} folder")

        self.path = folders.get_filepath(foldername, filename)
        surface = load(self.path).convert_alpha()
        min_rect = surface.get_bounding_rect()
        cropped_surface = Surface(min_rect.size, flags=surface.get_flags(), depth=surface)
        cropped_surface.blit(surface, (0, 0), min_rect)
        super().__init__(surface=cropped_surface)
