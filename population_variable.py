from typing import Optional, Callable

import numpy


def make_plant_population_variables(
    num_plants: int,
    initial: numpy.ndarray,
    growth: numpy.ndarray,
    interactions: numpy.ndarray,
):
    # initialize variables
    variables = {
        f"plant_{plant_i}": PopulationVariable(f"plant_{plant_i}", initial_i)
        for plant_i, initial_i in zip(range(num_plants), initial)
    }

    # deep copy arguments for lambda closure
    _growth = growth.copy()
    _interactions = interactions.copy()

    # define derivative equations (variables is mutable)
    for variable_i, variable in enumerate(variables.values()):
        variable.ddt = (
            lambda _variable_i=variable_i, _variable=variable:
            _growth[_variable_i] * _variable.value +
            (
                _interactions[_variable_i] @
                numpy.array([var.value for var in variables.values()]) *
                _variable.value
            )
        )

    return variables


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
