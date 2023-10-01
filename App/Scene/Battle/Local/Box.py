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
        super().__init__("Player box", (450, 250))


    def clear(self) -> Rect:
        return self.image.fill(GRAY)


    def choose_hero(self) -> Rect:
        # 'selecting' a hero will be done by a separate object
        self.clear()
        text = self.pen.write("Choose a hero")
        text.move("center", self.rect.center)
        _, r = text.draw(self.image)
        return r.move(*self.rect.topleft)


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
    

    def choose_ability(self, abilities: list[Ability]):
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


    def choose_target(self):
        # 'selecting' a target will be done by a separate object
        self.clear()
        text = self.pen.write("Choose a target")
        text.move("center", self.rect.center)
        _, r = text.draw(self.image)
        return r.move(*self.rect.topleft)


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
