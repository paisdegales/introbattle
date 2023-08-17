from App.Scene.Battle.Locals.FighterAttributes import FighterAttributes

class CharacterAbility:
    def __init__(self, name: str, description: str = "", character_attr: FighterAttributes | None = None):
        self.name = name
        self.description = description
        self.character_attr = character_attr


    @property
    def character_attr(self) -> FighterAttributes | None:
        return self.__character_attr


    @character_attr.setter
    def character_attr(self, character_attr: FighterAttributes | None) -> None:
        self.__character_attr = character_attr


    def cast(self) -> float:
        raise NotImplementedError()


class AttackAbility(CharacterAbility):
    def __init__(self, character_attr: FighterAttributes, name: str, description: str = ""):
        super().__init__(name, description, character_attr)


    def cast(self, enemy: FighterAttributes) -> float:
        value = self.character_attr.attack * (50 / (50 + enemy.defense))
        return value


class DefenseAbility(CharacterAbility):
    def __init__(self, character_attr: FighterAttributes, name: str, description: str = "", strength: int = 10):
        super().__init__(name, description, character_attr)
        self.strength = strength


    def cast(self) -> None:
        self.character_attr.defense += self.strength


    def restore(self) -> None:
        self.character_attr.defense -= self.strength
