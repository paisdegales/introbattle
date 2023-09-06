from pygame.rect import Rect
from pygame.surface import Surface
from App.Object.Object import BaseObject, SizedObject
from App.Object.CharacterImage import create_character_image
from App.Object.UserInterfaceImage import HealthBar
from App.Object.UserInterfaceImage import ManaBar
from App.Object.UserInterfaceImage import StaminaBar

class Fighter(SizedObject):
    def __init__(self, character_name: str, max_hp: int, max_mp, max_stamina: int):
        self.character = create_character_image(character_name)
        if self.character is None:
            raise Exception(f"No character named {character_name} was found!")
        self.hpbar = HealthBar()
        self.mpbar = ManaBar()
        self.staminabar = StaminaBar()
        self.components: list[BaseObject] = [self.character, self.hpbar, self.mpbar, self.staminabar]

        padding = 5
        width = max(map(lambda x: x.rect.w, self.components)) + 4*padding
        height = sum(map(lambda x: x.rect.h, self.components)) + 4*padding
        super().__init__(character_name, (width, height))

        self.hpbar.move("midtop", (int(width/2), 0))
        self.mpbar.move("midtop", self.hpbar.rect.midbottom)
        self.staminabar.move("midtop", self.mpbar.rect.midbottom)
        self.character.move("midbottom", (int(width/2), height))

        self.eraser: dict[str, tuple[Surface, Rect]] = dict()
        for component in self.components:
            value = component.draw(self.image)
            self.eraser.update({component.name: value})

        self.max_hp = max_hp
        self.max_mp = max_mp
        self.max_stamina = max_stamina
        self.current_hp = max_hp
        self.current_mp = max_mp
        self.current_stamina = max_stamina

        self.vibration = -3


    def take_damage(self, damage: int) -> Rect:
        """ returns a rectangle (relative coordinates and size) of the area that has changed """

        self.current_hp -= damage
        percent = self.current_hp / self.max_hp
        # rect = the relative area of 'hpbar' surface's that has changed
        rect = self.hpbar.update(percent)
        self.hpbar.erase(self.image, *self.eraser[self.hpbar.name])
        self.eraser[self.hpbar.name] = self.hpbar.draw(self.image)
        return self.hpbar.rect.move(*rect.topleft)


    def cast_spell(self, mana: int) -> Rect:
        """ returns a rectangle (relative coordinates and size) of the area that has changed """

        self.current_mp -= mana
        percent = self.current_mp / self.max_mp
        rect = self.mpbar.update(percent)
        self.mpbar.erase(self.image, *self.eraser[self.mpbar.name])
        self.eraser[self.mpbar.name] = self.mpbar.draw(self.image)
        return self.mpbar.rect.move(*rect.topleft)


    def spend_energy(self, energy: int) -> Rect:
        """ returns a rectangle (relative coordinates and size) of the area that has changed """

        self.current_stamina -= energy
        percent = self.current_stamina / self.max_stamina
        rect = self.staminabar.update(percent)
        self.staminabar.erase(self.image, *self.eraser[self.staminabar.name])
        self.eraser[self.staminabar.name] = self.staminabar.draw(self.image)
        return self.staminabar.rect.move(*rect.topleft)


    def vibrate(self, objname: str) -> Rect:
        obj = getattr(self, objname)
        if not isinstance(obj, BaseObject):
            return self.rect
        r = obj.erase(self.image, *self.eraser[obj.name])
        obj.shift(self.vibration, self.vibration)
        self.eraser[obj.name] = obj.draw(self.image)
        self.vibration *= -1
        return obj.rect.move(*r.topleft)
