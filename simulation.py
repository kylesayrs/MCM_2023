from typing import List, Dict, Any

from population_variable import PopulationVariable
from smc import StochasticMarkovChain


class Simulation:
    def __init__(
        self,
        environment_variables: Dict[str, StochasticMarkovChain],
        population_variables: Dict[str, PopulationVariable],
    ):
        self.environment_variables = environment_variables
        self.population_variables = population_variables

        self.environment_history = {
            key: []
            for key in self.environment_variables.keys()
        }
        self.population_history = {
            key: []
            for key in self.population_variables.keys()
        }


    @classmethod
    def from_config(cls, config):
        raise NotImplementedError()


    @staticmethod
    def step_variables(variables: Dict[str, Any]):
        return {
            var_name: variable.step()
            for var_name, variable in variables.items()
        }


    @staticmethod
    def update_variables(variables: Dict[str, Any]):
        [
            variable.update()
            for variable in variables.values()
        ]


    @staticmethod
    def update_history(history: Dict[str, List[Any]], new_values: Dict[str, Any]):
        for var_name, new_value in new_values.items():
            history[var_name].append(new_value)


    def step_and_update(self):
        new_env_values = self.step_variables(self.environment_variables)
        self.update_history(self.environment_history, new_env_values)
        self.update_variables(self.environment_variables)

        new_pop_values = self.step_variables(self.population_variables)
        self.update_history(self.population_history, new_pop_values)
        self.update_variables(self.population_variables)


    def run(self, max_steps: int = 1000):
        [self.step_and_update() for _ in range(max_steps)]
