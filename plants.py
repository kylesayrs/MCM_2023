from typing import List, Dict, Any, Optional

import numpy
from collections import OrderedDict

from config import Config
from environment_variable import PollutionVariable, DroughtVariable
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

    if _environment_variables["drought"].state_name == "none":
        return normal_ddt

    if _environment_variables["drought"].state_name == "mild":
        mild_ddt = (
            _config.mild_growth_effect[_variable_i] * self_value +
            (
                _config.mild_interactions_effect[_variable_i] @
                variables_values *
                self_value
            )
        )

        return normal_ddt + mild_ddt

    if _environment_variables["drought"].state_name == "severe":
        severe_ddt = (
            _config.severe_growth_effect[_variable_i] * self_value +
            (
                _config.severe_interactions_effect[_variable_i] @
                variables_values *
                self_value
            )
        )

        return normal_ddt + severe_ddt


def make_plant_environment_variables(config: Config):
    pollution_variable = PollutionVariable(
        config.pollution_drought_effect,
        config.pollution_state,
        config.pollution_bounds,
        config.pollution_step_size,
        config.seed
    )
    drought_variable = DroughtVariable(
        pollution_variable,
        config.drought_state,
        config.drought_names,
        config.drought_transitions,
        config.seed,
    )

    # since pollution affects drought, order pollution first
    return OrderedDict({
        "pollution": pollution_variable,
        "drought": drought_variable,
    })


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
