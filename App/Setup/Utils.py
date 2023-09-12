import logging

logfile = logging.FileHandler("introbattle.log", 'w')
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
menu_scene_logger = new_logger("MenuScene")
menu_scene_guildoptions_logger = new_logger("GuildOptions")
menu_scene_heroportrait_logger = new_logger("HeroPortrait")

