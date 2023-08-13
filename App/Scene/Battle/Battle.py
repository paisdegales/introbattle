from App.Object.BackgroundImage import BackgroundImage
from App.Object.Object import Object
from App.Object.UserInterfaceImage import *
from App.Object.Selector import DefaultSelector
from App.Scene.Scene import Scene
from App.Scene.Battle.Locals.CharacterBand import HeroBand, EnemyBand
from App.Scene.Battle.Locals.OptionsBox import OptionsBox
from App.Setup.Globals import LIGHT_GRAY, WHITE, DARK_GRAY, GRAY
from App.Scene.Battle.Locals.Events import *
from pygame.surface import Surface

class Battle(Scene):
    def __init__(self, screen: Surface):
        super().__init__(screen)


    def load_initial_frame(self, *args) -> None:
        self.background = BackgroundImage(self.screen.get_size())

        heros = args
        self.heros = HeroBand(heros)
        self.enemies = EnemyBand()
        self.options = OptionsBox()

        arrow = DefaultSelector(self.heros.get_positions(), (0, 0))
        arrow.draw(screen=self.screen)

        obj = AssembledUserInterfaceImage("introcomp_balao 1.png")
        obj.move("topleft", (500, 500))
        obj.screen = self.screen
        self.obj = obj
        health = HealthBar()
        health.move("topleft", (600, 600))
        health.screen = self.screen
        #health.draw()



    def draw_initial_frame(self) -> None:
        pass
        #self.background.draw(screen=self.screen)
        self.options.draw(screen=self.screen)
        self.heros.draw(screen=self.screen)
        self.enemies.draw(screen=self.screen)
        self.obj.draw(transparent=True)


    def erase(self) -> None:
        pass


    def terminate(self) -> list[str]:
        pass


    def __str__(self) -> str:
        string = list()
        string.append("Battle Scene Overview:")
        for obj in self.objects:
            string.append(obj.__str__())
        string = "\n".join(string)
        return string
