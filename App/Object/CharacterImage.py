from App.Object.Object import ImportedObject
from App.Setup.Globals import heropath, enemypath, ALL_HERONAMES, ALL_ENEMYNAMES


class CharacterImage(ImportedObject):
    def __init__(self, name: str, filepath: str):
        name = name.replace(".png", "").replace(".jpg", "").replace(".gif", "")
        super().__init__(name, filepath)
        self.scale_by(2)


class HeroImage(CharacterImage):
    def __init__(self, hero_name: str):
        super().__init__(hero_name, heropath(hero_name))


class EnemyImage(CharacterImage):
    def __init__(self, enemy_name: str):
        super().__init__(enemy_name, enemypath(enemy_name))


class PaladinImage(HeroImage):
    def __init__(self):
        super().__init__("Paladin.png")


class RogueImage(HeroImage):
    def __init__(self):
        super().__init__("Rogue.png")


class WizardImage(HeroImage):
    def __init__(self):
        super().__init__("Wizard.png")
        self.flip(True, False)


class HunterImage(HeroImage):
    def __init__(self):
        super().__init__("Hunter.png")


class PriestImage(HeroImage):
    def __init__(self):
        super().__init__("Priest.png")


class SkullImage(EnemyImage):
    def __init__(self):
        super().__init__("Skull.png")
        self.flip(True, False)


class MageImage(EnemyImage):
    def __init__(self):
        super().__init__("Mage.png")
        self.flip(True, False)


def create_character_image(character_name: str) -> CharacterImage | None:
    match character_name:
        case "Paladin.png" | "Paladin":
            return PaladinImage()
        case "Rogue.png" | "Rogue":
            return RogueImage()
        case "Wizard.png" | "Wizard":
            return WizardImage()
        case "Hunter.png" | "Hunter":
            return HunterImage()
        case "Priest.png" | "Priest":
            return PriestImage()
        case "Skull.png" | "Skull":
            return SkullImage()
        case "Mage.png" | "Mage":
            return MageImage()
        case _:
            return None


def create_all_hero_images() -> list[HeroImage]:
    heros: list[HeroImage] = list()
    for herofile in ALL_HERONAMES:
        hero = create_character_image(herofile)
        if hero and isinstance(hero, HeroImage):
            heros.append(hero)
    return heros


def create_all_enemy_images() -> list[EnemyImage]:
    enemies: list[EnemyImage] = list()
    for enemyfile in ALL_ENEMYNAMES:
        enemy = create_character_image(enemyfile)
        if enemy and isinstance(enemy, EnemyImage):
            enemies.append(enemy)
    return enemies


def create_all_character_images() -> list[CharacterImage]:
    heros = create_all_hero_images()
    enemies = create_all_enemy_images()
    characters: list[CharacterImage] = list()
    characters.extend(heros)
    characters.extend(enemies)
    return characters
