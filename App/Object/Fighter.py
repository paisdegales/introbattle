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
        self.current_hp = max_hp
        self.current_mp = max_mp
        self.current_stamina = max_stamina


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
