from App.Game import Game

def main() -> None:
    introbattle = Game()
    introbattle.load_scenes()
    introbattle.run()

if __name__ == "__main__":
    main()
