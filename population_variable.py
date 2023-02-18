from typing import Optional, Callable

import numpy


def make_plant_population_variables(
    num_plants: int,
    initial: numpy.ndarray,
    growth: numpy.ndarray,
    interactions: numpy.ndarray,
):
    population_variables = {
        f"plant_{plant_i}": PopulationVariable(f"plant_{plant_i}", initial_i)
        for plant_i, initial_i in zip(range(num_plants), initial)
    }

    for variable_i, variable in enumerate(population_variables.values()):
        variable.ddt = (
            lambda:
            growth[variable_i] * variable.value +
            (
                interactions[variable_i] @
                numpy.array([var.value for var in population_variables.values()]) *
                variable.value
            )
        )

    return population_variables


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
            raise ValueError("ddt is not defined!")

        self.new_value = max(self.value + (h * self.ddt()), 0.0)
        return self.new_value


    def update(self):
        self.value = self.new_value
        self.new_value = None

