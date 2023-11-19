from App.Setup.Globals import GRAY, WHITE, SCREENSIZE


ATTACK_ACTION = "Attack"
DEFEND_ACTION = "Defend"
PASS_ACTION = "Pass"
ACTION_LIST: list[str] = [ATTACK_ACTION, DEFEND_ACTION, PASS_ACTION, "Use Item"]


ENEMIES = ["Skull", "Mage", "Skull"]


VICTORY_TEXT = "Victory"
DEFEAT_TEXT = "Defeat"


REPEATED_HERO_WARNING = "This hero has already been selected in this turn! Please, choose another one"
DEAD_ENEMY_WARNING = "This enemy is dead! Please, choose another one" 
DEAD_HERO_WARNING = "This hero is dead :skull_emoji: It can't be selected"
INSUFFICIENT_MANA_WARNING = "No mana left for this ability, choose another one"


BOX_FONTFAMILY = "OpenSans"
BOX_FONTSIZE = 24
BOX_FONTCOLOR = WHITE
BOX_SIZE = 550, 250
BOX_GRID_POSITION = "topleft", (90, 25)
BOX_BGCOLOR = GRAY
BOX_POSITION = "bottomleft", (0, SCREENSIZE[1])
BOX_SHIFT = 50, -50
BOX_CHOOSE_HERO_TEXT = "Choose a hero"
BOX_CHOOSE_ENEMY_TEXT = "Choose a target"


HEROBAND_POSITION = "topleft", (240, 80)
ENEMYBAND_POSITION = "topleft", (600, 80)


STATUS_FONTFAMILY = "OpenSans"
STATUS_FONTSIZE = 20
STATUS_SIZE = 325, 125
HERO_STATUS_POSITION = "topleft", (650, 465)
ENEMY_STATUS_POSITION = "topleft", (650, 590)
