from App.Object.Image import Image
from App.Setup.Globals import folders
from pygame.transform import scale_by, flip
from os.path import join

class CharacterImage(Image):
    def __init__(self, folder_name: str, character_name: str):
        super().__init__(folder_name, character_name)
        self.scale_by(2)
        self.name = character_name.replace(".png", "")

    def scale_by(self, factor: float):
        surface = scale_by(self, factor)
        # reinitializing the object's state by calling the parent class of Image, using the __mro__ defined for the class of self
        super(Image, self).__init__(surface=surface)

    def flip(self, x_flip: bool, y_flip: bool):
        surface = flip(self, x_flip, y_flip)
        # reinitializing the object's state by calling the parent class of Image, using the __mro__ defined for the class of self
        super(Image, self).__init__(surface=surface)

class HeroImage(CharacterImage):
    def __init__(self, hero_name: str):
        super().__init__("Hero", hero_name)

class EnemyImage(CharacterImage):
    def __init__(self, enemy_name: str):
        super().__init__("Enemy", enemy_name)

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

class MageImage(EnemyImage):
    def __init__(self):
        super().__init__("Mage.png")

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
    hero_files = folders.get_files("Hero")
    for herofile in hero_files:
        heros.append(create_character_image(herofile))
    return heros

def create_all_enemy_images() -> list[EnemyImage]:
    enemies: list[EnemyImage] = list()
    enemy_files = folders.get_files("Enemy")
    for enemyfile in enemy_files:
        enemys.append(create_character_image(enemyfile))
    return enemies

def create_all_character_images() -> list[CharacterImage]:
    heros = create_all_hero_images()
    enemies = create_all_enemy_images()
    characters: list[CharacterImage] = list()
    characters.extend(heros).extend(enemies)
    return characters
