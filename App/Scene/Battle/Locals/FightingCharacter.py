from App.Object.Object import Object
from App.Object.UserInterfaceImage import HealthBar, ManaBar, StaminaBar
from App.Object.CharacterImage import create_character_image
from App.Scene.Battle.Locals.FighterAttributes import FighterAttributes
from App.Scene.Battle.Locals.CharacterAbility import AttackAbility, DefenseAbility


class FightingCharacter(Object):
    def __init__(self, name: str, **kwargs):
        ch = create_character_image(name)
        if ch is None:
            raise Exception("FightingCharacter init error", f"No {name} is defined")
        self.character = ch
        self.attributes = FighterAttributes(**kwargs)
        self.attacks: list[AttackAbility] = list()
        self.defenses: list[DefenseAbility] = list()

        self.hp_img = HealthBar()
        self.mp_img = ManaBar()
        self.stamina_img = StaminaBar()

        widths = map(lambda x: x.rect.w, [self.character, self.hp_img, self.mp_img, self.stamina_img])
        width = max(widths)
        height = self.character.rect.h + self.hp_img.rect.h + self.mp_img.rect.h + self.stamina_img.rect.h

        self.hp_img.move("midtop", (int(width/2), 0))
        self.mp_img.move("midtop", (int(width/2), self.hp_img.rect.h))
        self.stamina_img.move("midtop", (int(width/2), self.hp_img.rect.h + self.mp_img.rect.h))
        self.character.move("midtop", (int(width/2), self.hp_img.rect.h + self.mp_img.rect.h + self.stamina_img.rect.h))

        super().__init__((width, height))
        self.alias = f"Fighting {self.character.name}"
        self.add("hp",  self.hp_img)
        self.add("mp",  self.mp_img)
        self.add("stamina",  self.stamina_img)
        self.add("character",  self.character)


class FightingHunter(FightingCharacter):
    def __init__(self):
        super().__init__("Hunter", attack=10, defense=10, hp=10, mp=10, stamina=10)
        self.attacks.append(AttackAbility(self.attributes, "Flanking Strike", description=""))
        self.attacks.append(AttackAbility(self.attributes, "Quickshot", description=""))
        self.defenses.append(DefenseAbility(self.attributes, "Hunt Instinct", description="", strength=10))


class FightingPaladin(FightingCharacter):
    def __init__(self):
        super().__init__("Paladin", attack=10, defense=10, hp=10, mp=10, stamina=10)
        self.attacks.append(AttackAbility(self.attributes, "Sword of Justice", description=""))
        self.attacks.append(AttackAbility(self.attributes, "Impale", description=""))
        self.attacks.append(AttackAbility(self.attributes, "Judgement", description=""))
        self.attacks.append(AttackAbility(self.attributes, "Strike", description=""))
        self.defenses.append(DefenseAbility(self.attributes, "Holy Spirit", description="", strength=10))


class FightingRogue(FightingCharacter):
    def __init__(self):
        super().__init__("Rogue", attack=10, defense=10, hp=10, mp=10, stamina=10)
        self.attacks.append(AttackAbility(self.attributes, "Stab", description=""))
        self.defenses.append(DefenseAbility(self.attributes, "Deceive", description="", strength=10))


class FightingPriest(FightingCharacter):
    def __init__(self):
        super().__init__("Priest", attack=10, defense=10, hp=10, mp=10, stamina=10)
        self.attacks.append(AttackAbility(self.attributes, "Curse", description=""))
        self.defenses.append(DefenseAbility(self.attributes, "Pray", description="", strength=10))


class FightingWizard(FightingCharacter):
    def __init__(self):
        super().__init__("Wizard", attack=10, defense=10, hp=10, mp=10, stamina=10)
        self.attacks.append(AttackAbility(self.attributes, "Fireball", description=""))
        self.defenses.append(DefenseAbility(self.attributes, "Energy Barrier", description="", strength=10))


class FightingSkull(FightingCharacter):
    def __init__(self):
        super().__init__("Skull", attack=10, defense=10, hp=10, mp=10, stamina=10)
        self.attacks.append(AttackAbility(self.attributes, "Quick stab", description=""))
        self.defenses.append(DefenseAbility(self.attributes, "Endure", description="", strength=10))


class FightingMage(FightingCharacter):
    def __init__(self):
        super().__init__("Mage", attack=10, defense=10, hp=10, mp=10, stamina=10)
        self.attacks.append(AttackAbility(self.attributes, "Avadakedabra", description=""))
        self.defenses.append(DefenseAbility(self.attributes, "Hocus Pocus", description="", strength=10))


def create_fighter_image(name: str) -> FightingCharacter | None:
    match name:
        case "Paladin":
            return FightingPaladin()
        case "Hunter":
            return FightingHunter()
        case "Wizard":
            return FightingWizard()
        case "Priest":
            return FightingPriest()
        case "Rogue":
            return FightingRogue()
        case "Skull":
            return FightingSkull()
        case "Mage":
            return FightingMage()
        case _:
            return None
