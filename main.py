from App.Game import Game
from App.Setup.Globals import folders

def main() -> None:
    introbattle = Game(display_resolution=(1024, 768))
    introbattle.load_scenes()
    introbattle.run()


if __name__ == "__main__":
    main()
