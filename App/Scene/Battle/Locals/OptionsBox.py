from App.Object.Object import Object
from App.Object.Grid import Grid
from App.Setup.Globals import LIGHT_GRAY, WHITE, DARK_GRAY, GRAY, BLACK
from App.Font.Family import FontFamily
from App.Scene.Battle.Locals.FightingCharacter import FightingCharacter
from App.Scene.Battle.Locals.OptionsSelector import OptionsSelector

"""
class OptionsBoxStateIDLE(Object):
    def __init__(self):
        super().__init__("Dosis")
        text = self.font.render("Bold", "Choose a character", 40, BLACK, None)
        text = Object(surface=text)
        text.move("center", self.rect.center)
        self.add("text", text)
        

class OptionsBoxStateSelectingAction(Object):
    def __init__(self):
        super().__init__("OpenSans")
        fontsize = 30
        height = self.rect.h/4
        x1 = self.rect.w/4
        x2 = x1*3

        text = self.font.render("Bold", "Attack", fontsize, BLACK, None)
        text = Object(text=text)
        displacement = x1, height
        text.move("center", displacement)
        self.add("attack", text)

        text = self.font.render("Bold", "Defend", fontsize, BLACK, None)
        text = Object(text=text)
        displacement = x2, height
        text.move("center", displacement)
        self.add("defend", text)

        positions = self.get_addons_positions("midleft", mode="relative")
        positions.pop("little_box_topleft")
        positions.pop("little_box_topright")
        positions.pop("little_box_bottomleft")
        positions.pop("little_box_bottomright")

        # self.option_selector = OptionsSelector(positions, (-10, 6))
        selector = OptionsSelector(positions, (-10, 6))
        self.add("selector", selector)


    def draw(self, screen: Surface) -> None:
        super().draw(screen=screen)
        self.option_selector.draw(screen=screen)


    def erase(self) -> None:
        self.remove("attack", pop=True, force_update=True)
        self.remove("defend", pop=True, force_update=True)
        self.option_selector.erase()


class OptionsBoxStateSelectingOptions(Object):
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
"""

class ActionOptions(Object):
    def __init__(self, grid: Grid, family_name: str):
        coords = grid.coordinates()
        self.font = FontFamily(family_name)

        text1 = self.font.render("Regular", "Attack", 30, BLACK, None)
        text1 = Object(surface=text1)
        text1.alias = "Action box attack text"
        text1.move("topleft", coords[0])

        text2 = self.font.render("Regular", "Defend", 30, BLACK, None)
        text2 = Object(surface=text2)
        text2.alias = "Action box defend text"
        text2.move("topleft", coords[1])

        super().__init__(text2.rect.bottomright)

        self.add("attack", text1)
        self.add("defend", text2)
        arrow = OptionsSelector(self.get_addons_positions("midleft"), (-10, 5))
        self.add("arrow", arrow)

        self.arrow = arrow
        self.text1 = text1
        self.text2 = text2


    def select_next(self) -> None:
        raise NotImplementedError()


class OptionsBox(Object):
    def __init__(self, size: tuple[int, int]):
        super().__init__(size)
        self.alias = "OptionsBox"

        l = 15
        linethickness = 3

        self.surface.fill(LIGHT_GRAY)
        self.make_contour(WHITE, linethickness)
        self.move("topleft", (40, 500))

        little_box_topleft = Object((l,l))
        little_box_topleft.surface.fill(DARK_GRAY)
        little_box_topleft.make_contour(GRAY, linethickness)
        little_box_topleft.move("topleft", (0, 0))

        little_box_topright = Object((l,l))
        little_box_topright.surface.fill(DARK_GRAY)
        little_box_topright.make_contour(GRAY, linethickness)
        little_box_topright.move("topright", (size[0], 0))

        little_box_bottomleft = Object((l,l))
        little_box_bottomleft.surface.fill(DARK_GRAY)
        little_box_bottomleft.make_contour(GRAY, linethickness)
        little_box_bottomleft.move("bottomleft", (0, size[1]))

        little_box_bottomright = Object((l,l))
        little_box_bottomright.surface.fill(DARK_GRAY)
        little_box_bottomright.make_contour(GRAY, linethickness)
        little_box_bottomright.move("bottomright", size)

        self.add("little_box_topleft", little_box_topleft)
        self.add("little_box_topright", little_box_topright)
        self.add("little_box_bottomleft", little_box_bottomleft)
        self.add("little_box_bottomright", little_box_bottomright)

        # grid
