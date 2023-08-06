from pygame.surface import Surface
from pygame.rect import Rect

class SurfaceSnapshot():
    def __init__(self, surface: Surface):
        self.snapshots = list()
        self.surface = surface

    def take(self, area: Rect | None = None) -> None:
        snap = self.surface.copy()
        snap.blit(self.surface, (0, 0), area)
        self.snapshots.append(snap)

    def restore(self, index: int = 0) -> None:
        if self.snapshots:
            snap = self.snapshots.pop(index)
            self.surface.blit(snap, (0, 0))
