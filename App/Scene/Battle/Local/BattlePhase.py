from enum import Enum

class BattlePhase(Enum):
    SELECTING_HERO = 0
    SELECTING_ACTION = 1
    SELECTING_ABILITY = 2
    SELECTING_ENEMY = 3
    BATTLE_TIME = 4


