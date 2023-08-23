from App.Game import Game

def main() -> None:
    introbattle = Game(display_resolution=(1024, 768))
    introbattle.load_scenes()
    introbattle.run()

if __name__ == "__main__":
    main()
