from pygame.rect import Rect
from App.Object.Object import BaseObject, SizedObject
from App.Object.CharacterImage import create_character_image
from App.Object.UserInterfaceImage import HealthBar
from App.Object.UserInterfaceImage import ManaBar
from App.Object.UserInterfaceImage import StaminaBar
from App.Object.Ability import AttackAbility, DefenseAbility


class Fighter(SizedObject):
    def __init__(self, character_name: str, max_hp: int, max_mp: int, max_stamina: int, resistance: int):
        self.character = create_character_image(character_name)
        if self.character is None:
            raise Exception(f"No character named {character_name} was found!")

        self.hpbar = HealthBar()
        self.mpbar = ManaBar()
        self.staminabar = StaminaBar()
        self.components: list[BaseObject] = [self.character, self.hpbar, self.mpbar, self.staminabar]

        width = max(map(lambda x: x.rect.w, self.components))
        height = sum(map(lambda x: x.rect.h, self.components))

        # why +10? Answer: to ensure that this object will be able to vibrate without getting cropped by its surface's size
        super().__init__(character_name, (width+10, height+10))

        self.hpbar.move("midtop", (int(width/2), 0))
        self.mpbar.move("midtop", self.hpbar.rect.midbottom)
        self.staminabar.move("midtop", self.mpbar.rect.midbottom)
        self.character.move("midbottom", (int(width/2), height))

        for obj in self.components:
            obj.draw(self.image)

        self.max_hp = max_hp
        self.max_mp = max_mp
        self.max_stamina = max_stamina
        self.resistance = resistance
        self.current_hp = max_hp
        self.current_mp = max_mp
        self.current_stamina = max_stamina
        self.attacks: dict[str, AttackAbility] = dict()
        self.defenses: dict[str, DefenseAbility] = dict()


    def take_damage(self, damage: int) -> Rect:
        """ returns a rectangle (relative coordinates and size) of the area that has changed """

        self.current_hp -= damage
        percent = self.current_hp / self.max_hp
        area = self.hpbar.update(percent)
        self.hpbar.erase()
        _, position = self.hpbar.draw(self.image)
        changed = area.move(*position.topleft)
        _, changed = self.refresh(changed)
        return changed


    def cast_spell(self, mana: int) -> Rect:
        """ returns a rectangle (relative coordinates and size) of the area that has changed """

        self.current_mp -= mana
        percent = self.current_mp / self.max_mp
        area = self.mpbar.update(percent)
        self.mpbar.erase()
        _, position = self.mpbar.draw(self.image)
        changed = area.move(*position.topleft)
        _, changed = self.refresh(changed)
        return changed


    def spend_energy(self, energy: int) -> Rect:
        """ returns a rectangle (relative coordinates and size) of the area that has changed """

        self.current_stamina -= energy
        percent = self.current_stamina / self.max_stamina
        area = self.staminabar.update(percent)
        self.staminabar.erase()
        _, position = self.staminabar.draw(self.image)
        changed = area.move(*position.topleft)
        _, changed = self.refresh(changed)
        return changed


    def add_attack(self, name: str, value: int, cost: int):
        self.attacks[name] = AttackAbility(name, value, cost)


    def add_defense(self, name: str, value: int, cost: int):
        self.defenses[name] = DefenseAbility(name, value, cost)


class HunterFighter(Fighter):
    def __init__(self):
        super().__init__("Hunter", 30, 15, 20, 20)
        self.add_attack("Quickshot", 20, 5)
        self.add_defense("Camouflage", 5, 5)


class PaladinFighter(Fighter):
    def __init__(self):
        super().__init__("Paladin", 40, 10, 25, 30)
        self.add_attack("Charge", 15, 2)
        self.add_defense("Divine Shield", 5, 5)


class PriestFighter(Fighter):
    def __init__(self):
        super().__init__("Priest", 25, 40, 10, 10)
        self.add_attack("Curse", 10, 5)
        self.add_defense("Pray", 5, 5)
        self.add_defense("Heal", 20, 10)


class RogueFighter(Fighter):
    def __init__(self):
        super().__init__("Rogue", 25, 20, 30, 10)
        self.add_attack("Stab", 30, 4)
        self.add_defense("Evade", 5, 5)


class MageFighter(Fighter):
    def __init__(self):
        super().__init__("Mage", 25, 30, 15, 10)
        self.add_attack("Avadakedabra", 35, 10)
        self.add_defense("Hocus Pocus", 5, 5)


class SkullFighter(Fighter):
    def __init__(self):
        super().__init__("Skull", 100, 10, 10, 30)
        self.add_attack("Backbone", 5, 5)
        self.add_defense("Endurance", 5, 2)


class WizardFighter(Fighter):
    def __init__(self):
        super().__init__("Wizard", 50, 100, 50, 15)
        self.add_attack("Fireball", 10, 5)
        self.add_defense("Mana Shield", 5, 40)


def create_guild(names: list[str]) -> list[Fighter]:
    """ Create a group of fighters. There are no restrictions for what groups can be created.

        Return: list[Fighter] """

    guild = list()
    for name in names:
        name = name.capitalize()
        match name:
            case "Hunter":
                guild.append(HunterFighter())
            case "Priest":
                guild.append(PriestFighter())
            case "Paladin":
                guild.append(PaladinFighter())
            case "Mage":
                guild.append(MageFighter())
            case "Rogue":
                guild.append(RogueFighter())
            case "Skull":
                guild.append(SkullFighter())
            case "Wizard":
                guild.append(WizardFighter())
    return guild
