from App.Object.Object import Object
from App.Object.UserInterfaceImage import HealthBar, ManaBar, StaminaBar
from App.Object.CharacterImage import create_character_image

class FightingCharacter(Object):
    def __init__(self, name: str):
        self.character = create_character_image(name)
        self.hp = HealthBar()
        self.mp = ManaBar()
        self.stamina = StaminaBar()
        width = max(self.character.rect.width, self.hp.rect.width, self.mp.rect.width, self.stamina.rect.width)
        height = self.character.rect.height + self.hp.rect.height + self.mp.rect.height + self.stamina.rect.height
        super().__init__((width, height))
        self.add("hp", "midtop", self.hp.to_surface(), (width/2, 0), None)
        self.add("mp", "midtop", self.mp.to_surface(), (width/2, self.hp.rect.h), None)
        self.add("stamina", "midtop", self.stamina.to_surface(), (width/2, self.hp.rect.h + self.mp.rect.h), None)
        self.add("character", "bottomleft", self.character.to_surface(), (0, height), None)

