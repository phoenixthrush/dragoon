from .entity import Entity


class Hero(Entity):
    def __init__(self, name: str):
        super().__init__(name)

    def __str__(self):
        return f"Hero(Name: {self.name}, Money: {self._money}, Rank: {self._rank}, Stamina: {self._stamina}, Alive: {self._alive})"
