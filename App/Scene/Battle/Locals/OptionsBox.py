from App.Object.Object import Object
from App.Setup.Globals import LIGHT_GRAY, WHITE, DARK_GRAY, GRAY, BLACK
from App.Font.Family import FontFamily
from pygame.surface import Surface

class OptionsBoxState(Object):
    def __init__(self, family_name: str):
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
        self.move("topleft", (40, 500))
        self.font = FontFamily(family_name)


class OptionsBoxStateIDLE(OptionsBoxState):
    def __init__(self):
        super().__init__("Dosis")
        surface = self.font.render("Bold", "Choose a character", 40, BLACK, None)
        relative_coordinates = self.get_rect().center
        self.add("text", "center", surface, relative_coordinates, None)


    def erase(self):
        self.remove("text", pop=True, force_update=True)
        

class OptionsBoxStateSelectingAction(OptionsBoxState):
    def __init__(self):
        super().__init__("OpenSans")
        fontsize = 30
        height = self.rect.h/4
        x1 = self.rect.w/4
        x2 = x1*3

        surface = self.font.render("Bold", "Attack", fontsize, BLACK, None)
        displacement = x1, height
        self.add("attack", "center", surface, displacement, None)

        surface = self.font.render("Bold", "Defend", fontsize, BLACK, None)
        displacement = x2, height
        self.add("defense", "center", surface, displacement, None)


class OptionsBoxStateSelectingOptions(OptionsBoxState):
    def __init__(self):
        super().__init__("OpenSans")


class OptionsBox:
    def __init__(self, screen: Surface):
        self.screen = screen
        self.states = [OptionsBoxStateIDLE(), OptionsBoxStateSelectingAction(), OptionsBoxStateSelectingOptions]
        self.current_state = 0
        self.state = self.states[0]
        self.number_states = len(self.states)


    def draw(self):
        self.state.draw(screen=self.screen)

 
    def erase(self):
        self.state.erase()


    def next_state(self):
        self.current_state += 1
        self.current_state %= self.number_states
        self.state = self.states[self.current_state]
