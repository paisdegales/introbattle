from App.Object.Ability import AttackAbility, DefenseAbility
from App.Object.Fighter import Fighter
from pygame.rect import Rect
from math import ceil

class Combat:
    """ This class bridges the Fighter class and the Ability class, so that
    cyclic dependency can be avoided.

    Details:
    One could argue that Fighters have abilities and abilities are owned by
    Fighters. When using type notations, this design becomes problematic in Python
    because of a cyclic dependency materialized as an import loop """

    def __init__(self):
        pass


    def attack(self, attacker: Fighter, target: Fighter, ability_name: str) -> list[Rect]:
        ability: AttackAbility = attacker.attacks[ability_name]
        rects: list[Rect] = list()
        r = attacker.cast_spell(ability.cost)
        rects.append(r)
        damage = ability.value * (50/(50+target.resistance))
        r = target.take_damage(ceil(damage))
        rects.append(r)
        return rects


    def defend(self, defender: Fighter, ability_name: str) -> Rect:
        ability: DefenseAbility = defender.defenses[ability_name]
        r = defender.cast_spell(ability.value)
        defender.resistance *= 2
        return r
