from App.Scene.Battle.Locals.FightingCharacter import FightingCharacter
from pygame.surface import Surface


class CharacterBand:
    def __init__(self, characters: list[str]):
        self.characters: list[FightingCharacter] = list()
        for character in characters:
            character = FightingCharacter(character)
            self.characters.append(character)


    def draw(self, screen: Surface) -> None:
        for character in self.characters:
            character.draw(screen=screen, transparent=True)


    def get_positions(self) -> dict[str, tuple[int,int]]:
        positions = dict()
        for character in self.characters:
            positions[character.character.name] = character.rect.midtop
        return positions


class HeroBand(CharacterBand):
    def __init__(self, heros: list[str]):
        if len(heros) != 3:
            return
        super().__init__(heros)
        self.heros = self.characters
        self.heros[0].move("topleft", (200, 370))
        self.heros[1].move("topleft", (200, 200))
        self.heros[2].move("topleft", (300, 270))


class EnemyBand(CharacterBand):
    def __init__(self):
        enemies = ["Skull", "Mage"]
        super().__init__(enemies)
        self.enemies = self.characters
        self.enemies[0].move("topleft", (700, 350))
        self.enemies[1].move("topleft", (750, 200))
