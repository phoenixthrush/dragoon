class Entity:
    _money = 0
    _rank = 0
    _inventory = []
    _stamina = 20
    _playtime = 0
    _alive = True
    _horniness = 0
    _sleepiness = 0

    def __init__(self, name: str):
        self.name = name
