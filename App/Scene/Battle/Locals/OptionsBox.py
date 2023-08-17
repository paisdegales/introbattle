from App.Object.Object import Object
from App.Setup.Globals import LIGHT_GRAY, WHITE, DARK_GRAY, GRAY, BLACK
from App.Font.Family import FontFamily
from App.Scene.Battle.Locals.FightingCharacter import FightingCharacter
from App.Scene.Battle.Locals.OptionsSelector import OptionsSelector
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


    def erase(self) -> None:
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
        self.add("defend", "center", surface, displacement, None)

        positions = self.get_addons_positions("midleft", mode="absolute")
        positions.pop("little_box_topleft")
        positions.pop("little_box_topright")
        positions.pop("little_box_bottomleft")
        positions.pop("little_box_bottomright")
        self.option_selector = OptionsSelector(positions, (-10, 6))


    def draw(self, screen: Surface) -> None:
        super().draw(screen=screen)
        self.option_selector.draw(screen=screen)


    def erase(self) -> None:
        self.remove("attack", pop=True, force_update=True)
        self.remove("defend", pop=True, force_update=True)
        self.option_selector.erase()


class OptionsBoxStateSelectingOptions(OptionsBoxState):
    def __init__(self):
        super().__init__("OpenSans")


    def load(self, fighter: FightingCharacter) -> None:
        fontsize = 30
        height = self.rect.h/4
        x1 = self.rect.w/4
        x2 = 3*x1

        for index, attack in enumerate(fighter.attacks):
            surface = self.font.render("Bold", attack.name, fontsize, BLACK, None)
            quoc, rest = divmod(index, 2)
            displacement = x2 if rest else x1, height * quoc
            self.add(attack.name, "center", surface, displacement, None)


    def erase(self) -> None:
        pass



class OptionsBox:
    def __init__(self, screen: Surface):
        self.screen = screen
        self.states: list[OptionBoxState] = [OptionsBoxStateIDLE(), OptionsBoxStateSelectingAction(), OptionsBoxStateSelectingOptions()]
        self.current_state = 0
        self.state = self.states[0]
        self.number_states = len(self.states)


    def get_positions(self, vertex: str) -> dict[str, tuple[int, int]]:
        return self.state.get_addons_positions(vertex)


    def draw(self) -> None:
        self.state.draw(screen=self.screen)

 
    def erase(self) -> None:
        self.state.erase()


    def load(self, *args) -> None:
        self.state.load(*args)

    
    def next_state(self) -> None:
        self.current_state += 1
        self.current_state %= self.number_states
        self.state = self.states[self.current_state]
