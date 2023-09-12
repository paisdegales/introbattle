from App.Scene.Battle.Locals.FightingCharacter import create_fighter_image
from App.Object.Object import Object
from pygame.surface import Surface


class CharacterBand(Object):
    def __init__(self, characters: list[str]):
        fighters = list()
        for character in characters:
            character = create_fighter_image(character)
            fighters.append(character)
        heights = map(lambda x: x.rect.h, fighters)
        widths = list(map(lambda x: x.rect.w, fighters))
        height = sum(heights)
        width = 2*max(widths)

        super().__init__((width, height))
        self.alias = f"Character Band"
        self.camouflage = True
        for index, fighter in enumerate(fighters):
            fighter.camouflage = True
            self.add(index, fighter)


class HeroBand(CharacterBand):
    def __init__(self, heros: list[str]):
        if len(heros) != 3:
            return
        super().__init__(heros)
        self.addons[0].move("topleft", (0, 0))
        self.addons[1].move("topleft", self.addons[0].rect.bottomright)
        self.addons[2].move("topleft", (0, self.addons[1].rect.bottom))


class EnemyBand(CharacterBand):
    def __init__(self):
        enemies = ["Skull", "Mage"]
        super().__init__(enemies)
        self.addons[0].move("topleft", (0, 0))
        self.addons[1].move("topleft", self.addons[0].rect.bottomright)
