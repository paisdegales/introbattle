class Ability:
    def __init__(self, ability_name: str, value: int, cost: int):
        self.name = ability_name
        self.value = value
        self.cost = cost
        self.description = ""


    def __str__(self) -> str:
        return self.description


    def add_description(self, description: str):
        self.description = description


class AttackAbility(Ability):
    def __init__(self, ability_name: str, value: int, cost: int):
        super().__init__(ability_name, value, cost)


class DefenseAbility(Ability):
    def __init__(self, ability_name: str, value: int, cost: int):
        super().__init__(ability_name, value, cost)


