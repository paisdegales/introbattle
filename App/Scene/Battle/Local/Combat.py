from pygame.rect import Rect
from App.Object.Ability import AttackAbility, DefenseAbility
from App.Object.Fighter import Fighter

class Combat:
    def __init__(self):
        pass


    def round(self):
        raise NotImplementedError()


    def act(self, attacker: Fighter, attack_name: str, defender: Fighter, defense_name: str | None = None) -> list[Rect]:
        rects = list()
        if defense_name is not None:
            rects.extend(self.defend(defender, defense_name))
        rects.extend(self.attack(attacker, defender, attack_name))
        if defense_name is not None:
            defender.resistance //= 2
        return rects


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
