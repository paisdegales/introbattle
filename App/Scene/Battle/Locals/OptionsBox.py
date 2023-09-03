from App.Object.Object import Object
from App.Object.Grid import Grid
from App.Setup.Globals import LIGHT_GRAY, WHITE, DARK_GRAY, GRAY, BLACK
from App.Font.Family import FontFamily
from App.Scene.Battle.Locals.FightingCharacter import FightingCharacter
from App.Scene.Battle.Locals.OptionsSelector import OptionsSelector


class IDLE(Object):
    def __init__(self, family_name: str):
        self.font = FontFamily(family_name)
        text = self.font.render("Bold", "Choose a character", 40, BLACK, None)
        super().__init__(surface=text)
        self.alias = "IDLE"


class HeroOptions(Object):
    def __init__(self, grid: Grid, family_name: str):
        coords = grid.coordinates()
        self.font = FontFamily(family_name)

        fontsize = 30

        text1 = self.font.render("Regular", "Attack", fontsize, BLACK, None)
        text1 = Object(surface=text1)
        text1.alias = "Action box attack text"
        text1.move("topleft", coords[0])

        text2 = self.font.render("Regular", "Defend", fontsize, BLACK, None)
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
        self.camouflage = True


    def change_option(self, previous: bool = True) -> None:
        erased_area = self.remove("arrow")
        drawn_area = self.update(erased_area)
        self.parent.update(drawn_area)
        if previous:
            self.arrow.left()
        else:
            self.arrow.right()
        self.arrow.draw(info="drawn onto Option's surface")
        drawn_area = self.update(self.arrow.drawn_area)
        self.parent.update(drawn_area)

    def select(self) -> str:
        return self.arrow.get_current_ref()


class AbilityOptions(Object):
    def __init__(self, size: tuple[int, int], grid: Grid, family_name: str):
        """
            this class can only be loaded once a hero and action were both chosen. For this reason,
            it's impossible to tell the size that it should initially have.
        """
        super().__init__(size)
        self.camouflage = True
        self.font = FontFamily(family_name)
        self.coords = grid.coordinates()


    def load(self, fighter: FightingCharacter, action: str) -> None:
        fontsize = 20
        for ability, pos in zip(fighter.attacks if action == "Attack" else fighter.defenses, self.coords):
            surface = self.font.render("Regular", ability.name, fontsize, BLACK, None)
            obj = Object(surface=surface)
            obj.move("topleft", pos)
            self.add(f"{ability.name} text", obj)
        self.arrow = OptionsSelector(self.get_addons_positions("midleft"), (-10, 5))
        self.add("arrow", self.arrow)


    def change_option(self, previous: bool = True) -> None:
        erased_area = self.remove("arrow")
        drawn_area = self.update(erased_area)
        self.parent.update(drawn_area)
        if previous:
            self.arrow.left()
        else:
            self.arrow.right()
        self.arrow.draw(info="drawn onto AbilityOptions' surface")
        drawn_area = self.update(self.arrow.drawn_area)
        self.parent.update(drawn_area)


    def select(self) -> str:
        return self.arrow.get_current_ref()


class TargetOptions(Object):
    def __init__(self, family_name: str):
        self.font = FontFamily(family_name)
        text = self.font.render("Bold", "Choose a target", 40, BLACK, None)
        super().__init__(surface=text)
        self.alias = "TargetBox"


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
