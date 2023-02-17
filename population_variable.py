from typing import Callable


class PopulationVariable():
    def __init__(self, name: str, value: float, dy_func: Callable):
        self.name = name
        self.value = value
        self.dy_func = dy_func


    def step(self):
        self.value += self.dy_func()
        return self.value

