from App.Scene.Scene import Scene
from App.Screen.Screen import Screen
from App.Object.BackgroundImage import BackgroundImage
from App.Scene.Menu.Local.Banner import Banner
from App.Scene.Menu.Local.Positioning import *
from logging import warning

class Menu(Scene):
    def __init__(self, screen: Screen) -> None:
        super().__init__(screen)

    def load_initial_frame(self) -> None:
        try:
            self.background = BackgroundImage(self.screen.get_size())
            self.background.screen = self.screen
            self.background.move(*BACKGROUND_POSITION)
        except Exception as e:
            warning(f"Failed when loading the menu's background image: {type(e)}")
            raise e

        try:
            self.banner = Banner("OpenSans", self.screen)
            self.banner.load("Introbattle!", size=(300, 150), vertex="center", coordinates=(150, 75))
        except Exception as e:
            warning("Failed when loading the menu's banner: {type(e)}")
            raise e

        """
        try:
            path_to_heros = join("App", "Imagens", "Personagens", "Herois")
            nomes_herois = [heroi.replace(".png", "") for heroi in listdir(path_to_heros) if isfile(join(path_to_heros, heroi))]
            self.herois = list()
            for nome in nomes_herois:
                heroi = criar_personagem(nome, self.screen)
                self.herois.append(heroi)

        except Exception as e:
            warning("Erro ao carregar opcoes de heroi")
            raise e
        """


    def draw_initial_frame(self) -> None:
        try:
            self.background.draw()
        except Exception as e:
            warning("Failed when drawing the menu's background")
            raise e

        try:
            self.banner.move(*BANNER_POSITION)
            self.banner.draw()
        except Exception as e:
            warning("Failed when drawing the menu's banner")
            raise e
        
        """
        try:
            for index, heroi in enumerate(self.herois):
                heroi.pintar((100+100*index, 500))
        except Exception as e:
            warning("Erro ao desenhar heroi")
            raise e
        """

    def erase(self) -> None:
        try:
            #self.background.erase()
            self.banner.erase()
        except Exception as e:
            warning("Failed when trying to erase the menu scene!")
            raise e
