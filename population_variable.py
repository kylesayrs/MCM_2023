from typing import Optional, Callable


class PopulationVariable:
    def __init__(
        self,
        name: str,
        value: float,
        ddt: Optional[Callable] = None
    ):
        self.name = name
        self.value = value
        self.ddt = ddt

        self.new_value = None


    def step(self, h: Optional[float] = 1.0):
        if self.ddt is None:
            raise ValueError(f"ddt is not defined for {self.name}")

        self.new_value = max(self.value + (h * self.ddt()), 0.0)
        return self.new_value


    def update(self):
        self.value = self.new_value
        self.new_value = None


    def __str__(self):
        return f"PopulationVariable(name={self.name}, value={self.value})"
