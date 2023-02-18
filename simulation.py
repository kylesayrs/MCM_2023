from typing import List, Dict, Any, Optional

from config import BaseConfig
from population_variable import PopulationVariable
from smc import StochasticMarkovChain
from plants import make_plant_environment_variables, make_plant_population_variables


class Simulation:
    def __init__(
        self,
        environment_variables: Dict[str, StochasticMarkovChain],
        population_variables: Dict[str, PopulationVariable],
        simulation_h: Optional[float] = None,
        environment_update_period: float = 1.0,
    ):
        self.environment_variables = environment_variables
        self.population_variables = population_variables
        self.simulation_h = simulation_h
        self.environment_update_period = environment_update_period

        self.t_buffer = 0.0
        self.time_history = [0.0]
        self.environment_history = {
            key: [environment_variable.value]
            for key, environment_variable in self.environment_variables.items()
        }
        self.population_history = {
            key: [population_variable.value]
            for key, population_variable in self.population_variables.items()
        }


    @classmethod
    def from_config(cls, config: BaseConfig):
        # environment variables
        environment_variables = make_plant_environment_variables(
            config.drought_state,
            config.drought_names,
            config.drought_transitions,
            config.seed,
        )

        # create population variables
        population_variables = make_plant_population_variables(
            config.num_species,
            config.initial,
            config.growth,
            config.interactions,
            environment_variables,
        )

        # create simulation
        return cls(
            environment_variables=environment_variables,
            population_variables=population_variables,
            simulation_h=config.simulation_h,
            environment_update_period=config.environment_update_period,
        )


    @staticmethod
    def step_variables(variables: Dict[str, Any], *step_args, **step_kwargs):
        return {
            var_name: variable.step(*step_args, **step_kwargs)
            for var_name, variable in variables.items()
        }


    @staticmethod
    def update_variables(variables: Dict[str, Any]):
        for variable in variables.values():
            variable.update()


    @staticmethod
    def update_history(history: Dict[str, List[Any]], variables: Dict[str, Any]):
        for var_name, variable in variables.items():
            history[var_name].append(variable.value)


    def step_and_update(self):
        self.t_buffer += self.simulation_h

        if self.t_buffer >= self.environment_update_period:
            self.step_variables(self.environment_variables)
            self.update_variables(self.environment_variables)
            self.t_buffer -= self.environment_update_period

        self.step_variables(self.population_variables, self.simulation_h)
        self.update_variables(self.population_variables)

        self.update_history(self.environment_history, self.environment_variables)
        self.update_history(self.population_history, self.population_variables)
        self.time_history.append(self.time_history[-1] + self.simulation_h)


    def run(self, max_time: float = 1000.0):
        max_simulation_steps = int(max_time / self.simulation_h)
        for simulation_step_i in range(max_simulation_steps):
            self.step_and_update()
