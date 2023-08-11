from App.Object.CharacterImage import CharacterImage, create_character_image
from App.Object.Object import Object
from App.Object.UserInterfaceImage import *
from App.Scene.Battle.Locals.FightingCharacter import FightingCharacter
from App.Scene.Scene import Scene
from App.Setup.Globals import LIGHT_GRAY, WHITE, DARK_GRAY, GRAY
from App.Scene.Menu.Local.Selector import Selector
from pygame.surface import Surface

class Battle(Scene):
    def __init__(self, screen: Surface):
        super().__init__(screen)


    def load_initial_frame(self, *args) -> None:
        heros = args
        self.heros = list()
        for hero in heros:
            hero = create_character_image(hero)
            self.heros.append(hero)
        self.heros[0].move("topleft", (200, 400))
        self.heros[1].move("topleft", (200, 200))
        self.heros[2].move("topleft", (300, 300))

        self.enemies = list()
        enemies = ["Skull", "Mage"]
        for enemy in enemies:
            enemy = create_character_image(enemy)
            self.enemies.append(enemy)
        self.enemies[0].move("topleft", (600, 350))
        self.enemies[1].move("topleft", (650, 200))

        
        little_box = Object((15,15))
        little_box.fill(DARK_GRAY)
        little_box.make_contour(GRAY, 3)
        action_box = Object((600, 225))
        action_box.fill(LIGHT_GRAY)
        action_box.make_contour(WHITE, 3)
        action_box.add("little_box_topleft", "topleft", little_box, (0, 0), None)
        action_box.add("little_box_topright", "topright", little_box, (600, 0), None)
        action_box.add("little_box_bottomleft", "bottomleft", little_box, (0, 225), None)
        action_box.add("little_box_bottomright", "bottomright", little_box, (600, 225), None)
        action_box.move("topleft", (40, 500))
        action_box.screen = self.screen
        action_box.draw()
        # action_box.remove("little_box_bottomright", pop=True, force_update=True)
        action_box.toggle_addon("little_box_bottomright")

        test = {"1": (100, 100), "2": (200, 200), "3": (300, 300)}
        arrow = Selector(test, (0, 0))
        arrow.screen = self.screen
        #arrow.draw()

        obj = AssembledUserInterfaceImage("introcomp_balao 1.png")
        obj.move("topleft", (500, 500))
        obj.screen = self.screen
        self.obj = obj
        health = HealthBar()
        health.move("topleft", (600, 600))
        health.screen = self.screen
        surf = health.to_surface()
        #health.draw()
        self.screen.blit(surf, (50, 500))

        f = FightingCharacter(self.heros[0].name)
        f.move("topleft", (100, 200))
        f.screen = self.screen
        print(f)
        f.draw()




    def draw_initial_frame(self) -> None:
        for hero in self.heros:
            hero.screen = self.screen
            hero.draw()
        for enemy in self.enemies:
            enemy.screen = self.screen
            enemy.draw()
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
