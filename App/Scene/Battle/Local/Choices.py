from App.Object.Fighter import Fighter


class Choices:
    def __init__(self, number_choices_per_turn: int):
        self.limit = number_choices_per_turn
        self.history: list[tuple[Fighter, str, str | None, Fighter | None]] = list()
        self.hero: Fighter | None = None
        self.action: str | None = None
        self.ability: str | None = None
        self.target: Fighter | None = None


    def pack(self) -> tuple[Fighter, str, str | None, Fighter | None]:
        if self.hero is None or self.action is None:
            raise Exception("choices: a choice hasn't been made")
        pack = self.hero, self.action, self.ability, self.target
        return pack


    def save(self) -> None:
        pack = self.pack()
        self.history.append(pack)


    def clear_history(self) -> None:
        self.history.clear()


    def clear(self) -> None:
        self.hero: Fighter | None = None
        self.action: str | None = None
        self.ability: str | None = None
        self.target: Fighter | None = None


    def nothing_left_to_choose(self) -> bool:
        number_choices = len(self.history)

        if number_choices > self.limit:
            raise Exception('max number of choices per turn was exceeded')

        return True if number_choices == self.limit else False
