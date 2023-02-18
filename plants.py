from typing import List, Dict, Any, Optional

import numpy

from config import Config
from smc import StochasticMarkovChain
from population_variable import PopulationVariable


def plant_ddt(_config, _variable_i, _variables, _environment_variables):
    variables_values = numpy.array([var.value for var in _variables.values()])
    self_value = variables_values[_variable_i]

    normal_ddt = (
        _config.growth[_variable_i] * self_value +
        (
            _config.interactions[_variable_i] @
            variables_values *
            self_value
        )
    )

    return normal_ddt


def make_plant_environment_variables(
    drought_state: int,
    drought_names: List[str],
    drought_transitions: numpy.ndarray,
    seed: Optional[int] = None,
):
    return {
        "drought": StochasticMarkovChain(
            drought_state,
            drought_names,
            drought_transitions,
            seed,
        )
    }


def make_plant_population_variables(
        config: Config,
        environment_variables: Dict[str, Any],
):
    # initialize variables
    variables = {
        f"plant_{plant_i}": PopulationVariable(f"plant_{plant_i}", initial_i)
        for plant_i, initial_i in zip(range(config.num_plants), config.initial)
    }

    # define derivative equations (variables is mutable)
    for variable_i, variable in enumerate(variables.values()):
        def _lambda_closure(
            _config=config.copy(),
            _variable_i=variable_i,
        ):
            return plant_ddt(_config, _variable_i, variables, environment_variables)

        variable.ddt = _lambda_closure

    return variables
