from pygame.rect import Rect
from App.Object.CharacterImage import HeroImage, create_all_hero_images
from App.Object.Grid import Grid
from App.Object.Object import SizedObject
from App.Object.Selector import DefaultSelector
from App.Scene.Menu.Local.HeroPortrait import HeroPortrait
from App.Scene.Menu.Local.Positioning import                \
        GUILDOPTIONS_GRID_SPACING, GUILDOPTIONS_POSITION,   \
        SELECTOR_DISPLACEMENT
from App.Setup.Globals import ALL_HERONAMES
from App.Setup.Utils import menu_scene_guildoptions_logger as logger


class GuildOptions(SizedObject):
    def __init__(self):
        self.grid = Grid(2, 3, GUILDOPTIONS_GRID_SPACING)
        self.grid.coordinates[1][2] = None
        self.grid.shift((75, 0), 1, None)
        self.grid.shift((0, 16)) # make room for the selector to move

        self.portraits: list[HeroPortrait] = list()

        for name, position in zip(ALL_HERONAMES, self.grid.get_positions("midtop")):
            name = name.replace(".png", "")
            logger.info("The %s's portrait is about to be created", name)
            h = HeroPortrait(name)
            h.move("midtop", position)
            self.portraits.append(h)
            setattr(self, name, h)
        self.selector = DefaultSelector(self.grid, SELECTOR_DISPLACEMENT)
        self.selector.select("midtop")

        super().__init__("guild options", self.grid.position.bottomright)
        for portrait in self.portraits:
            portrait.draw(self.image)
        self.selector.draw(self.image)
        self.move(*GUILDOPTIONS_POSITION)
        self.hide = True


    def go(self, direction: str) -> Rect:
        logger.info("Selector is moving %s", direction)
        erased = self.selector.erase()
        if direction == "left":
            self.selector.left()
        elif direction == "right":
            self.selector.right()
        elif direction == "up":
            self.selector.up()
        elif direction == "down":
            self.selector.down()
        self.selector.select(vertex="midtop")
        _, drawn = self.selector.draw(self.image)
        rect = erased.union(drawn)
        self.refresh(rect)
        rect = rect.move(self.rect.topleft)
        return rect


    def select(self) -> str:
        index = self.selector.line * self.selector.grid.number_columns + self.selector.column
        hero = self.portraits[index].hero
        if not isinstance(hero, HeroImage):
            raise Exception('Error when selecting hero: cant select non hero')
        return hero.name


    def vibrate_selection(self) -> Rect:
        component = getattr(self, self.select())
        if not isinstance(component, HeroPortrait):
            return Rect(0, 0, 0, 0)
        r = component.vibrate_component("hero")
        _, r = self.refresh(r)
        return r
