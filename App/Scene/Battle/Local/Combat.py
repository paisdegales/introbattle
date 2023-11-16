from pygame.rect import Rect
from App.Object.Ability import AttackAbility, DefenseAbility
from App.Object.Fighter import Fighter

class Combat:
    def __init__(self):
        pass


    def attack(self, attacker: Fighter, target: Fighter, ability_name: str) -> list[Rect]:
        ability: AttackAbility = attacker.attacks[ability_name]
        rects: list[Rect] = list()
        r = attacker.cast_spell(ability.cost)
        rects.append(r)
        r = target.take_damage(ability.value)
        rects.append(r)
        return rects


    def defend(self, defender: Fighter, ability_name: str) -> Rect:
        ability: DefenseAbility = defender.defenses[ability_name]
        r = defender.cast_spell(ability.value)
        defender.resistance *= 2
        return r
