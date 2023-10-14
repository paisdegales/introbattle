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
        self.selector.jump("midtop")
        self.selector.link(map(lambda x: x.hero, self.portraits))

        super().__init__("guild options", self.grid.position.bottomright)
        for portrait in self.portraits:
            portrait.draw(self.image)
        self.selector.draw(self.image)
        self.move(*GUILDOPTIONS_POSITION)
        self.hide = True


    def go(self, direction: str) -> list[Rect]:
        """ moves the selector up, down, left or right

            Return: all areas that have changed in this object """

        logger.info("Selector is moving %s", direction)
        # relative areas: areas relative to this objects layout
        # absolute areas: areas relative to the screen layout
        areas: list[Rect] = list()
        relative_areas = self.selector.redraw_upon_movement(direction)
        for relative_area in relative_areas:
            # since the GuildOptions object is meant to be drawn on the screen,
            # any call to its 'refresh' will return absolute areas/coordinates,
            # that is, this object is positioned around the window's topleft corner
            _, absolute_areas = self.refresh(relative_area)
            areas.append(absolute_areas)
        return areas


    def select(self) -> str:
        """ select the hero that is currently selected by the cursor

            Return: all areas that have changed in this object """

        hero = self.selector.select()
        if not isinstance(hero, HeroImage):
            raise Exception('Error when selecting hero: cant select non hero')
        return hero.name


    def vibrate_selection(self) -> Rect:
        """ vibrate the hero that is currently selected by the cursor

            Return: all areas that have changed in this object """

        component = getattr(self, self.select())
        if not isinstance(component, HeroPortrait):
            return Rect(0, 0, 0, 0)
        r = component.vibrate_component("hero")
        # since the GuildOptions object is meant to be drawn on the screen,
        # any call to its 'refresh' will return absolute areas/coordinates,
        # that is, this object is positioned around the window's topleft corner
        _, r = self.refresh(r)
        return r
