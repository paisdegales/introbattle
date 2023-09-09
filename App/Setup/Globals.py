from pygame.color import Color
from os.path import join
from os import listdir


SCREENSIZE = 800, 600


APP_FOLDER = "App"
RESOURCE_FOLDER = "Resource"
CHARACTER_FOLDER = "Character"
HERO_FOLDER = "Hero"
ENEMY_FOLDER = "Enemy"
UI_FOLDER = "UI"
BACKGROUND_FOLDER = "Background"
FONT_FOLDER = "Fonts"


def enemypath(enemy_filename: str) -> str:
    return join(APP_FOLDER, RESOURCE_FOLDER, CHARACTER_FOLDER, ENEMY_FOLDER, enemy_filename)

def heropath(hero_filename: str) -> str:
    return join(APP_FOLDER, RESOURCE_FOLDER, CHARACTER_FOLDER, HERO_FOLDER, hero_filename)

def uipath(ui_filename: str) -> str:
    return join(APP_FOLDER, RESOURCE_FOLDER, UI_FOLDER, ui_filename)

def bgpath(bg_filename: str) -> str:
    return join(APP_FOLDER, RESOURCE_FOLDER, BACKGROUND_FOLDER, bg_filename)

def fontpath(familyname: str, stylename: str) -> str:
    return join(APP_FOLDER, RESOURCE_FOLDER, FONT_FOLDER, familyname, stylename)


ALL_HERONAMES = [ heroname for heroname in listdir(heropath("")) ]
ALL_ENEMYNAMES = [ enemyname for enemyname in listdir(enemypath("")) ]


RED = Color(255, 0, 0)
GREEN = Color(0, 255, 0)
BLUE = Color(0, 0, 255)
WHITE = Color(255, 255, 255)
BLACK = Color(0, 0, 0)
GRAY = Color(120, 120, 120)
DARK_GRAY = Color(50, 50, 50)
LIGHT_GRAY = Color(150, 150, 150)
