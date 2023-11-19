import logging
import logging.handlers 

logfile = logging.handlers.RotatingFileHandler("introbattle.log", mode='w', maxBytes=1*1024*1024, backupCount=1)
#logfile = logging.FileHandler("introbattle.log", 'w')
logfile.setLevel(logging.DEBUG)
formatter = logging.Formatter( \
        fmt='%(asctime)s: %(name)-13s: %(levelname)s: %(message)s', \
        datefmt='%m/%d/%Y %I:%M:%S %p', \
        style='%')
logfile.setFormatter(formatter)

def new_logger(logger_name: str) -> logging.Logger:
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logfile)
    return logger

object_logger = new_logger("BaseObject")
screen_logger = new_logger("Screen")
fillingbar_logger = new_logger("FillingBar")

menu_scene_logger = new_logger("MenuScene")
menu_scene_guildoptions_logger = new_logger("GuildOptions")
menu_scene_heroportrait_logger = new_logger("HeroPortrait")

battle_scene_logger = new_logger("BattleScene")
battle_fight_logger = new_logger("Fight")
battle_box_logger = new_logger("Box")
battle_band_logger = new_logger("CharacterBand")

end_scene_logger = new_logger("EndScene")
