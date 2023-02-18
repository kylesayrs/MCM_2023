from typing import List

import numpy

from smc import StochasticMarkovChain
from population_variable import PopulationVariable


def make_plant_environment_variables(
    drought_state: int,
    drought_names: List[str],
    drought_transitions: numpy.ndarray,
):
    return {
        "drought": StochasticMarkovChain(
            drought_state,
            drought_names,
            drought_transitions,
        )
    }


def make_plant_population_variables(
        num_plants: int,
        initial: numpy.ndarray,
        growth: numpy.ndarray,
        interactions: numpy.ndarray,
        environment_variables: Dict[str, Any],
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
            ) +
        )

    return variables
