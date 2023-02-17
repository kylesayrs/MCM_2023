from typing import Optional, Callable


class PopulationVariable:
    def __init__(self, name: str, value: float, ddt: Callable):
        self.name = name
        self.value = value
        self.ddt = ddt

        self.new_value = None


    def step(self, h: Optional[float] = 1.0):
        self.new_value = self.value + (h * self.ddt())
        return self.new_value


    def update(self):
        self.value = self.new_value
        self.new_value = None

