class Entity:
    __money = 0
    __rank = 0
    __inventory = []
    __stamina = 20
    __playtime = 0
    __alive = True
    __horniness = 0
    __sleepiness = 0

    def __init__(self, name: str):
        self.name = name
