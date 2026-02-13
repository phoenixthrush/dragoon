from .entity import Entity


class Hero(Entity):
    def __init__(self, name: str):
        super().__init__(name)
