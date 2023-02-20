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
        self.extinct = False


    def step(self, h: Optional[float] = 1.0):
        if self.ddt is None:
            raise ValueError(f"ddt is not defined for {self.name}")

        if self.extinct:
            self.new_value = 0.0
        else:
            self.new_value = max(self.value + (h * self.ddt()), 0.0)
            
        return self.new_value


    def update(self):
        self.value = self.new_value
        self.new_value = None

        if self.value <= 0.0:
            self.extinct = True


    def __str__(self):
        return f"PopulationVariable(name={self.name}, value={self.value})"
