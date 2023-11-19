from App.Font.Pen import Pen
from App.Object.Object import BaseObject, SizedObject
from App.Setup.Globals import BLUE, RED
from pygame.draw import circle


class Ability:
    def __init__(self, ability_name: str, value: int, cost: int):
        self.name = ability_name
        self.value = value
        self.cost = cost
        self.description = ""


    def generate_text(self, pen: Pen) -> BaseObject:
        name = pen.write(self.name)
        value = pen.write(str(self.value))
        strength_symbol = SizedObject('strength', (15, 15))
        cost = pen.write(str(self.cost))
        mana_symbol = SizedObject('mana', (15, 15))

        circle(strength_symbol.image, RED, strength_symbol.rect.center, 4)
        circle(mana_symbol.image, BLUE, mana_symbol.rect.center, 4)

        components: list[BaseObject] = [name, value, strength_symbol, cost, mana_symbol]
        w = sum(list(map(lambda x: x.rect.w, components)))
        h = max(list(map(lambda x: x.rect.h, components)))

        text = SizedObject(self.name, (w+16, h))
        text.hide = True
        name.rect.x = 0
        value.rect.x = name.rect.x + name.rect.w + 8
        strength_symbol.rect.x = value.rect.x + value.rect.w
        strength_symbol.rect.centery = value.rect.h // 2
        cost.rect.x = strength_symbol.rect.x + strength_symbol.rect.w + 8
        mana_symbol.rect.x = cost.rect.w + cost.rect.x
        mana_symbol.rect.centery = cost.rect.h // 2

        for component in components:
            component.hide = True
            component.draw(text.image)

        return text


    def __str__(self) -> str:
        return self.description


    def add_description(self, description: str):
        self.description = description


class AttackAbility(Ability):
    def __init__(self, ability_name: str, value: int, cost: int):
        super().__init__(ability_name, value, cost)


class DefenseAbility(Ability):
    def __init__(self, ability_name: str, value: int, cost: int):
        super().__init__(ability_name, value, cost)


