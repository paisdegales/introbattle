from pygame.rect import Rect
from App.Font.Family import FontFamily
from App.Font.Pen import Pen
from App.Object.Ability import Ability
from App.Object.Grid import Grid
from App.Object.Object import SizedObject
from App.Object.Selector import DefaultSelector
from App.Setup.Globals import GRAY, LIGHT_GRAY, WHITE


class Box(SizedObject):
    def __init__(self):
        self.pen = Pen(FontFamily("OpenSans"), "Regular", 24, WHITE)
        self.grid = Grid(2, 2, (200, 100))
        self.grid.move("topleft", (50, 50))
        self.selector = DefaultSelector(self.grid, (-10, 0))
        self.selector.tip = "midright"
        self.selector.rotate(90)
        self.selector.select("midleft")
        # 0: choosing a hero
        # 1: choosing an action
        # 2: choosing an ability
        # 3: choosing a target
        self.state_counter = 0
        super().__init__("Player box", (450, 250))
        self.clear()


    def clear(self) -> Rect:
        return self.image.fill(GRAY)


    def choose_hero(self) -> list[Rect]:
        # 'selecting' a hero will be done by a separate object
        rects: list[Rect] = list()
        r = self.clear()
        rects.append(r)
        text = self.pen.write("Choose a hero")
        # it's not possible to use 'self.rect.center' to center the text in the box, because
        # 'self.rect.center' does not reference the box's topleft point, but rather the screen's topleft point
        # this is a problem, because the text needs a relative reference to its parental object so it gets positioned inside of it
        text.move("center", (self.rect.w//2, self.rect.h//2))
        _, r = text.draw(self.image)
        rects.append(r)
        return rects


    def choose_action(self, actions: list[str]) -> list[Rect]:
        rects: list[Rect] = list()
        r = self.clear()
        rects.append(r)
        self.options = actions
        positions = self.grid.get_positions("midleft")

        for text, position in zip(self.options, positions):
            obj = self.pen.write(text)
            obj.move("midleft", position)
            _, r = obj.draw(self.image)
            rects.append(r)

        if self.selector.drawn:
            r = self.selector.erase()
            rects.append(r)
            self.selector.line = 0
            self.selector.column = 0
            self.selector.select("midleft")

        _, r = self.selector.draw(self.image)
        rects.append(r)

        return rects
    

    def choose_ability(self, abilities: list[Ability]) -> list[Rect]:
        rects: list[Rect] = list()
        rects.append(self.clear())

        self.options = [ability.name for ability in abilities]
        positions = self.grid.get_positions("midleft")

        for text, position in zip(self.options, positions):
            obj = self.pen.write(text)
            obj.move("midleft", position)
            _, r = obj.draw(self.image)
            rects.append(r)

        if self.selector.drawn:
            r = self.selector.erase()
            rects.append(r)
            self.selector.line = 0
            self.selector.column = 0
            self.selector.select("midleft")

        _, r = self.selector.draw(self.image)
        rects.append(r)

        return rects


    def choose_target(self) -> list[Rect]:
        # 'selecting' a target will be done by a separate object
        rects: list[Rect] = list()
        r = self.clear()
        rects.append(r)
        text = self.pen.write("Choose a target")
        text.move("center", (self.rect.w//2, self.rect.h//2))
        _, r = text.draw(self.image)
        rects.append(r)
        return rects


    def next_state(self, *args) -> list[Rect]:
        """ easily transition between the four stages the box can under go during a turn

            1st stage: waiting for the player to choose a hero
            2nd stage: waiting for the player to select what kind of action he wants to perform (attack, defend, etc)
            3rd stage: waiting for the player to choose an ability to cast
            4th stage: waiting for the player to choose a target (if possible)

            Return: list[Rect]
                * a list of all the areas that have changed in self's surface in order to go to the next state """

        rects: list[Rect] = list()
        if self.state_counter == 0:
            rects = self.choose_hero()
        elif self.state_counter == 1:
            rects = self.choose_action(args[0])
        elif self.state_counter == 2:
            rects = self.choose_ability(args[0])
        elif self.state_counter == 3:
            rects = self.choose_target()
        self.state_counter += 1
        self.state_counter %= 4
        return rects


    def motion(self, direction: str) -> list[Rect]:
        rects: list[Rect] = list()
        r = self.selector.erase()
        _, r = self.refresh(r)
        rects.append(r)

        movement = getattr(self.selector, direction)
        movement()
        self.selector.select("midleft")

        _, r = self.selector.draw(self.image)
        _, r = self.refresh(r)
        rects.append(r)
        return rects


    def select(self) -> str:
        if not self.selector.drawn:
            raise Exception('Nothing can be selected because the selector is not drawn')
        index = self.selector.line * self.selector.grid.number_columns + self.selector.column
        option = self.options[index]
        return option
