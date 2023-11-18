from App.Object.Object import BaseObject, SizedObject
from App.Object.CharacterImage import create_character_image
from App.Object.UserInterfaceImage import FillingBar, HealthBar, ManaBar, StaminaBar
from App.Object.Ability import AttackAbility, DefenseAbility
from App.Setup.Globals import RED
from pygame.rect import Rect
from pygame.draw import line


class Fighter(SizedObject):
    def __init__(self, character_name: str, max_hp: int, max_mp: int, max_stamina: int, resistance: int, speed: int):
        self.character = create_character_image(character_name)
        self.hp = HealthBar(max_hp, max_hp // 10)
        self.mp = ManaBar(max_mp, max_mp // 5)
        self.stamina = StaminaBar(max_stamina, max_stamina // 4)
        self.resistance = resistance
        self.speed = speed
        self.attacks: dict[str, AttackAbility] = dict()
        self.defenses: dict[str, DefenseAbility] = dict()
        self.alive = True

        components: list[BaseObject] = [self.character, self.hp, self.mp, self.stamina]

        width = max(map(lambda x: x.rect.w, components))
        height = sum(map(lambda x: x.rect.h, components))

        # why +10? Answer: to ensure that this object will be able to vibrate without getting cropped by its surface's size
        super().__init__(character_name, (width+10, height+10))
        self.hide = True
        self.hp.move("midtop", (width//2, 0))
        self.mp.move("midtop", self.hp.rect.midbottom)
        self.stamina.move("midtop", self.mp.rect.midbottom)
        self.character.move("midbottom", (width//2, height))
        for obj in components:
            obj.draw(self.image)


    def take_damage(self, damage: int) -> Rect:
        r = self.hp.update(-damage)
        if self.hp.value == 0:
            self.alive = False
        _, r = self.hp.refresh(r)
        _, r = self.refresh(r)
        return r


    def cast_spell(self, mana: int) -> Rect:
        r = self.mp.update(-mana)
        _, r = self.mp.refresh(r)
        _, r = self.refresh(r)
        return r


    def spend_energy(self, energy: int) -> Rect:
        r = self.stamina.update(-energy)
        _, r = self.stamina.refresh(r)
        _, r = self.refresh(r)
        return r


    def add_attack(self, name: str, value: int, cost: int) -> None:
        self.attacks[name] = AttackAbility(name, value, cost)


    def add_defense(self, name: str, value: int, cost: int) -> None:
        self.defenses[name] = DefenseAbility(name, value, cost)


    def regen_attribute(self, attribute: str) -> Rect:
        """ regenerates the hp/mp/stamina bar by some amount

            Parameters: attribute: str ('hp', 'mp' or 'stamina')

            Return: * A rectangle which represents the relative area of the fighter's surface that has changed """

        bar = getattr(self, attribute)
        if not isinstance(bar, FillingBar):
            raise Exception('regen_status: got something other than what was expected')

        r = bar.update(bar.regen) # updating the mp to some %
        _, r = bar.refresh(r) # repaiting the mp to the fighter's surface
        _, r = self.refresh(r) # repainting the fighter to the character band's surface
        return r


    def die(self) -> Rect:
        self.alive = False
        rect = line(self.image, RED, (0, 0), self.rect.size, 4)
        rect = line(self.image, RED, (self.rect.size[0], 0), (0, self.rect.size[1]), 4)
        _, rect = self.refresh(rect)
        return rect


    @property
    def dead(self) -> bool:
        return not self.alive



class HunterFighter(Fighter):
    def __init__(self):
        super().__init__("Hunter", 30, 15, 20, 20, 4)
        self.add_attack("Stab", 10, 2)
        self.add_attack("Quickshot", 20, 5)
        self.add_attack("Trap", 15, 6)
        self.add_attack("Longshot", 40, 10)
        self.add_defense("Run", 5, 5)
        self.add_defense("Sniff", 5, 5)
        self.add_defense("Preparation", 5, 5)
        self.add_defense("Camouflage", 5, 5)


class PaladinFighter(Fighter):
    def __init__(self):
        super().__init__("Paladin", 40, 10, 25, 30, 1)
        self.add_attack("Charge", 15, 2)
        self.add_attack("Impale", 15, 2)
        self.add_attack("Strike", 15, 2)
        self.add_attack("Holysword", 15, 2)
        self.add_defense("Run", 5, 5)
        self.add_defense("Battlecry", 5, 5)
        self.add_defense("Endurance", 5, 5)
        self.add_defense("Divine Shield", 5, 5)


class PriestFighter(Fighter):
    def __init__(self):
        super().__init__("Priest", 25, 40, 10, 10, 2)
        self.add_attack("Curse", 10, 5)
        self.add_attack("Codemn", 10, 5)
        self.add_attack("Slur", 10, 5)
        self.add_attack("Repent", 10, 5)
        self.add_defense("Pray", 5, 5)
        self.add_defense("Run", 20, 10)
        self.add_defense("Heal", 20, 10)
        self.add_defense("Faith", 20, 10)


class RogueFighter(Fighter):
    def __init__(self):
        super().__init__("Rogue", 25, 20, 30, 10, 5)
        self.add_attack("Stab", 30, 12)
        self.add_attack("Threaten", 30, 4)
        self.add_attack("Strike", 30, 4)
        self.add_attack("Pickpocket", 30, 4)
        self.add_defense("Evade", 5, 5)
        self.add_defense("Run", 5, 5)
        self.add_defense("Fadeaway", 5, 5)
        self.add_defense("Facade", 5, 5)


class WizardFighter(Fighter):
    def __init__(self):
        super().__init__("Wizard", 30, 20, 25, 15, 3)
        self.add_attack("Fireball", 10, 5)
        self.add_attack("Lightining", 10, 5)
        self.add_attack("Icecold", 10, 5)
        self.add_attack("Imprison", 10, 5)
        self.add_defense("Run", 5, 5)
        self.add_defense("Mana Shield", 5, 5)
        self.add_defense("Improve", 5, 5)
        self.add_defense("Slowtime", 5, 5)


class MageFighter(Fighter):
    def __init__(self):
        super().__init__("Mage", 50, 100, 50, 15, 3)
        self.add_attack("Avis", 10, 10)
        self.add_attack("Avadakedabra", 10, 10)
        self.add_attack("Momentum", 10, 10)
        self.add_attack("Expelliarmus", 10, 10)
        self.add_defense("Run", 5, 5)
        self.add_defense("Hocus Pocus", 5, 5)
        self.add_defense("Ascendio", 5, 5)
        self.add_defense("Aguamenti", 5, 5)


class SkullFighter(Fighter):
    def __init__(self):
        super().__init__("Skull", 100, 10, 10, 30, 1)
        self.add_attack("Backbone", 5, 3)
        self.add_attack("Bonebone", 5, 3)
        self.add_attack("Boneattack", 5, 3)
        self.add_attack("Bigbone", 5, 3)
        self.add_defense("Run", 5, 2)
        self.add_defense("Endurance", 5, 2)
        self.add_defense("Repair", 5, 2)
        self.add_defense("Reflect", 5, 2)


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
