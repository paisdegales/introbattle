from App.Object.BackgroundImage import BackgroundImage
from App.Scene.Battle.Locals.CharacterBand import HeroBand, EnemyBand
from App.Scene.Battle.Locals.CharacterSelector import CharacterSelector
from App.Scene.Battle.Locals.Events import *
from App.Scene.Battle.Locals.OptionsBox import OptionsBox
from App.Scene.Scene import Scene
from pygame.locals import K_UP, K_DOWN, K_RETURN
from pygame.surface import Surface

class Battle(Scene):
    def __init__(self, screen: Surface):
        super().__init__(screen)


    def load_initial_frame(self, *args) -> None:
        self.background = BackgroundImage(self.screen.get_size())

        heros = args
        self.heros = HeroBand(heros)
        self.enemies = EnemyBand()
        self.options = OptionsBox(self.screen)

        self.selector = CharacterSelector(self.heros.get_positions(), (0, -10))


        #obj = AssembledUserInterfaceImage("introcomp_balao 1.png")
        #obj.move("topleft", (500, 500))
        #obj.screen = self.screen
        #self.obj = obj
        #health = HealthBar()
        #health.move("topleft", (600, 600))
        #health.screen = self.screen
        #health.draw()



    def draw_initial_frame(self) -> None:
        self.background.draw(screen=self.screen)
        self.options.draw()
        self.heros.draw(screen=self.screen)
        self.enemies.draw(screen=self.screen)

        self.selector.draw(screen=self.screen)
        self.keyboard.add_keydown(K_UP, MoveSelectorUp(self.selector))
        self.keyboard.add_keydown(K_DOWN, MoveSelectorDown(self.selector))
        self.keyboard.add_keydown(K_RETURN, SelectHero(self.keyboard, self.options))

        self.objects.append(self.options)
        self.objects.append(self.heros)
        self.objects.append(self.enemies)
        self.objects.append(self.selector)

        #self.obj.draw(transparent=True)


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
