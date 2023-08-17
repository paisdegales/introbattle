from App.Object.Object import Object
from App.Object.UserInterfaceImage import HealthBar, ManaBar, StaminaBar
from App.Object.CharacterImage import create_character_image
from App.Scene.Battle.Locals.FighterAttributes import FighterAttributes
from App.Scene.Battle.Locals.CharacterAbility import AttackAbility, DefenseAbility
from pygame.surface import Surface


class FightingCharacter(Object):
    def __init__(self, name: str, **kwargs):
        self.character = create_character_image(name)
        self.attributes = FighterAttributes(**kwargs)
        self.attacks: list[AttackAbility] = list()
        self.defenses: list[DefenseAbility] = list()

        self.hp_img = HealthBar()
        self.hp_img.screen = Surface(self.hp_img.rect.size)
        self.hp_img.draw()

        self.mp_img = ManaBar()
        self.mp_img.screen = Surface(self.mp_img.rect.size)
        self.mp_img.draw()

        self.stamina_img = StaminaBar()
        self.stamina_img.screen = Surface(self.stamina_img.rect.size)
        self.stamina_img.draw()

        width = max(self.character.rect.width, self.hp_img.rect.width, self.mp_img.rect.width, self.stamina_img.rect.width)
        height = self.character.rect.height + self.hp_img.rect.height + self.mp_img.rect.height + self.stamina_img.rect.height
        super().__init__((width, height))

        self.add("hp", "midtop", self.hp_img.to_surface(), (width/2, 0), None)
        self.add("mp", "midtop", self.mp_img.to_surface(), (width/2, self.hp_img.rect.h), None)
        self.add("stamina", "midtop", self.stamina_img.to_surface(), (width/2, self.hp_img.rect.h + self.mp_img.rect.h), None)
        self.add("character", "bottomleft", self.character.to_surface(), (0, height), None)


class FightingHunter(FightingCharacter):
    def __init__(self):
        super().__init__("Hunter", attack=10, defense=10, hp=10, mp=10, stamina=10)
        self.attacks.append(AttackAbility(self.attributes, "Flanking Strike", description=""))
        self.attacks.append(AttackAbility(self.attributes, "Quickshot", description=""))
        self.defenses.append(DefenseAbility(self.attributes, "Hunt Instinct", description="", strength=10))


class FightingPaladin(FightingCharacter):
    def __init__(self):
        super().__init__("Paladin", attack=10, defense=10, hp=10, mp=10, stamina=10)
        self.attacks.append(AttackAbility(self.attributes, "Impale", description=""))
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
