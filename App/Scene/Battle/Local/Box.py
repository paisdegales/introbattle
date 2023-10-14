from pygame.rect import Rect
from App.Font.Family import FontFamily
from App.Font.Pen import Pen
from App.Object.Ability import Ability
from App.Object.Grid import Grid
from App.Object.Object import SizedObject, BaseObject
from App.Object.Selector import DefaultSelector
from App.Setup.Globals import GRAY, LIGHT_GRAY, WHITE


class Box(SizedObject):
    def __init__(self):
        super().__init__("Player box", (450, 250))
        self.clear()

        # configuring how all texts of this class will look like
        self.pen = Pen(FontFamily("OpenSans"), "Regular", 24, WHITE)

        # creating the grid where all texts will get positioned
        self.grid = Grid(2, 2, (200, 100))
        self.grid.move("topleft", (50, 50))

        self.selector = DefaultSelector(self.grid, (-10, 0))
        # setting where the tip of the selector is (it will get modified after
        # rotating it next)
        self.selector.tip = "midright"
        # setting the selector to face east
        self.selector.rotate(90)
        # initially positioning the selector
        self.selector.jump("midleft")

        # 0: Choosing a hero
        # 1: Choosing an action
        # 2: Choosing an ability
        # 3: Choosing a target
        self.state_counter = 0


    def clear(self) -> Rect:
        return self.image.fill(GRAY)


    def choose_hero(self) -> list[Rect]:
        """ This is the first intended state of this object (self.state_counter = 0)

            In this state, the box remains still until the player chooses a
            hero. At this point, the box only has a central text, indicating
            that the player should choose a hero.

            Choosing a hero is controled by another object (See HeroBand in
            /App/Scene/Battle/Local/CharacterBand for more info)

            After a hero has been chosen, the method 'choose_action' should be
            called. This will update the box to display all currently available
            actions that the player can perform with that hero.

            Return: a list of (relative) areas that have changed in this
            objects surface, in order to draw this state """

        rects: list[Rect] = list()

        # repaint the box with its background (effectively, everything gets erased)
        r = self.clear()
        rects.append(r)

        # no linking is done, because the selector is not meant to be drawn yet.
        # hence, it points to nothing
        self.selector.link([None, None, None, None])

        # the text is created 
        text: BaseObject = self.pen.write("Choose a hero")
        # centering the text inside its parent is kinda problematic:
        #   its not possible to use 'self.rect.center' to center the text
        #   inside the box (text's parent), because that attribute stores
        #   absolute coordinates and not relative ones. Here we need relative
        #   coordinates, because the text is positioned around its parent's
        #   origin (self.rect.topleft), not the screen's origin
        #   (screen.get_rect().topleft)
        text.move("center", (self.rect.w//2, self.rect.h//2))

        # the text gets drawn on its parental surface
        _, r = text.draw(self.image)
        rects.append(r)
        return rects


    def choose_action(self, actions: list[str]) -> list[Rect]:
        """ This is the second intended state of this object (self.state_counter = 1)

            In this state, the box displays the actions the player can perform
            with the chosen hero.

            Choosing an action requires modifying the box's surface constantly,
            since the player can move the selector undetermingly. But this
            method only takes care of drawing the initial frame for this state.
            To erase/draw the selector, use the 'go' method and refresh the
            box's visual by calling 'box.refresh(box.go("left"))' (for example)

            After an action has been chosen, the method 'choose_ability' should
            be called. This will update the box to display all currently
            available abilities that the player can use with that hero.

            Return: a list of (relative) areas that have changed in this
            objects surface, in order to draw this state """

        rects: list[Rect] = list()

        # repaint the box with its background (effectively, everything gets erased)
        r = self.clear()
        rects.append(r)

        # the selector is set to (symbolicly) point to all the available actions
        # that is, the selector is always facing an action in the screen, no matter
        # where it gets positioned
        self.selector.link(actions)

        # positioning all actions in the screen
        # an action is simply a text object
        positions = self.grid.get_positions("midleft")
        for text, position in zip(actions, positions):
            obj: BaseObject = self.pen.write(text)
            obj.move("midleft", position)
            _, r = obj.draw(self.image)
            rects.append(r)

        # this is not necessarily right?
        # logically, the selector would never be drawn on the screen when
        # 'choose_action' gets called, but since i messed up and didn't erase
        # it correctly in 'choose_heros', this if statement is needed 
        if self.selector.drawn:
            r = self.selector.erase()
            rects.append(r)
            self.selector.line = 0
            self.selector.column = 0
            self.selector.jump("midleft")

        _, r = self.selector.draw(self.image)
        rects.append(r)

        return rects
    

    def choose_ability(self, abilities: list[Ability]) -> list[Rect]:
        """ This is the third intended state of this object (self.state_counter = 2)

            In this state, the box displays all the available abilities bounded
            to the previously chosen action.

            Choosing an ability requires modifying the box's surface constantly,
            since the player can move the selector undetermingly. But this
            method only takes care of drawing the initial frame for this state.
            To erase/draw the selector, use the 'go' method and refresh the
            box's visual by calling 'box.refresh(box.go("left"))' (for example)

            After an action has been chosen, the method 'choose_target' should
            be called. This will make the box display a text while it waits for
            the player to choose a target/enemy to cast its ability (in case it's
            an attack).

            Return: a list of (relative) areas that have changed in this
            objects surface, in order to draw this state """

        rects: list[Rect] = list()

        # repaint the box with its background (effectively, everything gets erased)
        rects.append(self.clear())

        # the selector is set to (symbolicly) point to all the available ability names
        # shown in the screen
        abilities = [ability.name for ability in abilities]
        self.selector.link(abilities)

        # positioning all ability names in the screen
        positions = self.grid.get_positions("midleft")
        for text, position in zip(abilities, positions):
            obj: BaseObject = self.pen.write(text)
            obj.move("midleft", position)
            _, r = obj.draw(self.image)
            rects.append(r)

        # even though the 'clear' method was called in the beginning of this
        # method, the selector is still drawn at the screen! WHAT?
        # well, that's because an object only gets effectively erased if its
        # 'erase' method gets called (its 'drawn' attribute is set to False').
        # For this reason, this if statement is necessary.
        if self.selector.drawn:
            r = self.selector.erase()
            rects.append(r)
            self.selector.line = 0
            self.selector.column = 0
            self.selector.jump("midleft")

        _, r = self.selector.draw(self.image)
        rects.append(r)

        return rects


    def choose_target(self) -> list[Rect]:
        """ This is the forth and (usually) the final intended state of the box
            (self.state_counter = 3)

            In this state, the box displays a text while it waits for the
            player to choose a target/enemy to cast its ability in case it's
            an attack. If the player chose a defensive ability, this method shouldn't
            be called.

            After a target has been chosen, the turn should take place and then
            a call to 'choose_hero' should be made. This will enable cycling through
            all four states again, until the battle is over.

            Return: a list of (relative) areas that have changed in this
            objects surface, in order to draw this state """

        # 'selecting' a target will be done by a separate object
        rects: list[Rect] = list()

        # repaint the box with its background (effectively, everything gets erased)
        r = self.clear()
        rects.append(r)

        # no linking is done, because the selector is not meant to be visible
        # on the screen. hence, it points to nothing
        self.selector.link([None, None, None, None])

        text = self.pen.write("Choose a target")
        text.move("center", (self.rect.w//2, self.rect.h//2))

        _, r = text.draw(self.image)
        rects.append(r)

        return rects


    def next_state(self, *args) -> list[Rect]:
        """ Easily transition between the four stages the box can under go during a turn

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
            rects = self.choose_action(["Attack", "Defense", "Action 3", "Action 4"])
        elif self.state_counter == 2:
            rects = self.choose_ability(args[0])
        elif self.state_counter == 3:
            rects = self.choose_target()
        self.state_counter += 1
        self.state_counter %= 4
        return rects


    def go(self, direction: str) -> list[Rect]:
        return tuple(self.selector.redraw_upon_movement(direction, "midleft"))


    def select(self) -> str:
        if not self.selector.drawn:
            raise Exception('Nothing can be selected because the selector is not drawn')

        if self.state_counter == 1:
            pass
        elif self.state_counter == 2:
            pass

        return self.selector.select()
