from App.Object.Object import Object
from App.Setup.Globals import LIGHT_GRAY, WHITE, DARK_GRAY, GRAY
from pygame.surface import Surface

class OptionsBox(Object):
    def __init__(self):
        little_box = Object((15,15))
        little_box.fill(DARK_GRAY)
        little_box.make_contour(GRAY, 3)
        super().__init__((600, 225))
        self.fill(LIGHT_GRAY)
        self.make_contour(WHITE, 3)
        self.add("little_box_topleft", "topleft", little_box, (0, 0), None)
        self.add("little_box_topright", "topright", little_box, (600, 0), None)
        self.add("little_box_bottomleft", "bottomleft", little_box, (0, 225), None)
        self.add("little_box_bottomright", "bottomright", little_box, (600, 225), None)
        # action_box.remove("little_box_bottomright", pop=True, force_update=True)
        # action_box.toggle_addon("little_box_bottomright")
        self.move("topleft", (40, 500))


    def draw(self, screen: Surface) -> None:
        self.screen = screen
        super().draw()
