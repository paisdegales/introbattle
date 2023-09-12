from App.Font.Family import FontFamily
from App.Object.Object import Object
from App.Scene.Battle.Locals.CharacterBand import HeroBand
from App.Scene.Battle.Locals.FightingCharacter import FightingCharacter
from App.Setup.Globals import BLACK, LIGHT_GRAY, WHITE


class StatusBox(Object):
    def __init__(self, size: tuple[int, int], heroband: HeroBand, font_name: str):
        super().__init__(size)
        self.heros = heroband.addons.values
        self.font = FontFamily(font_name)
        self.surface.fill(LIGHT_GRAY)
        self.make_contour(WHITE, 3)

    def new_section(self, hero: FightingCharacter, size: tuple[int, int]) -> None:
        section = Object(size)
        hero_name_text = self.font.render("Regular", hero.character.name, 20, BLACK)
        hero_status_text = self.font.render("Regular", f"{hero.attributes['hp']}", 20, BLACK)
