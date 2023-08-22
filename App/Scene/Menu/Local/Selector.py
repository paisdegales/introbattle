from App.Scene.Scene import EndOfScene
from App.Object.Selector import DefaultSelector
from App.Scene.Menu.Local.GuildOptions import GuildOptions

class MenuSelector(DefaultSelector):
    def __init__(self, obj: GuildOptions, displacement: tuple[int, int]):
        anchors = obj.get_anchors()
        super().__init__(anchors, displacement)
        self.obj = obj


    def right(self) -> None:
        # erasing
        item = self.get_current_ref()
        self.obj.unhighlight_text(item)
        self.erase()

        # updating selector's position
        self.current += 1
        self.current %= self.max
        self.move_index(self.current)

        # drawing
        self.draw()
        item = self.get_current_ref()
        self.obj.highlight_text(item)


    def left(self) -> None:
        # erasing
        item = self.get_current_ref()
        self.obj.unhighlight_text(item)
        self.erase()

        # updating selector's position
        self.current -= 1
        self.current %= self.max
        self.move_index(self.current)

        # drawing
        self.draw()
        item = self.get_current_ref()
        self.obj.highlight_text(item)


    def up(self) -> None:
        # erasing
        item = self.get_current_ref()
        self.obj.unhighlight_text(item)
        self.erase()

        # updating selector's position
        if self.current >= 0 and self.current < 3:
            pass
        elif self.current == 3:
            self.current = 0
        else:
            self.current = 1
        self.move_index(self.current)

        # drawing
        self.draw()
        item = self.get_current_ref()
        self.obj.highlight_text(item)



    def down(self) -> None:
        # erasing
        item = self.get_current_ref()
        self.obj.unhighlight_text(item)
        self.erase()

        # updating selector's position
        if self.current >= 3 and self.current < self.max:
            pass
        elif self.current == 2:
            self.current = 4
        elif self.current == 1:
            self.current = 3
        else:
            self.current = 3
        self.move_index(self.current)

        # drawing
        self.draw()
        item = self.get_current_ref()
        self.obj.highlight_text(item)


    def select(self, storage: list) -> None:
        item = self.get_current_ref()
        storage.append(item)
        if len(storage) == 3:
            raise EndOfScene("The player chose: {}".format(storage))
        return item
