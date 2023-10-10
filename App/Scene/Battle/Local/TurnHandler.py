from App.Object.Ability import Ability
from App.Object.Fighter import Fighter
from App.Scene.Battle.Local.Combat import Combat
from App.Scene.Battle.Local.CharacterBand import HeroBand, EnemyBand
from App.Scene.Battle.Local.Box import Box


class TurnHandler:
    def __init__(self, heros: HeroBand, enemies: EnemyBand, box: Box):
        self.heros = heros
        self.enemies = enemies
        self.box = box
        self.combat = Combat()

    def routine(self, heroname: str, action: str, ability: Ability, target: str):
        self.combat.act(self.chosen_hero, self.chosen_ability, self.chosen_target, None)  
