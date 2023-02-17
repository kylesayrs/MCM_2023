import numpy

from config import BaseConfig
from simulation import Simulation
from smc import StochasticMarkovChain
from population_variable import PopulationVariable
from visualize import plot_values, plot_population_variables, show_plot


if __name__ == "__main__":
    # set up configuration
    config = BaseConfig()
    config.seed = 42
    numpy.random.seed(config.seed)

    # create environment variables
    environment_variables = {}
    weather = StochasticMarkovChain(
        "sunny",
        ["rainy", "sunny"],
        [[0.9, 0.1],
         [0.5, 0.5]]
    )
    environment_variables["weather"] = weather

    # create population variables
    population_variables = {}
    for plant_i in range(0, 1):
        population = PopulationVariable(
            f"plant_{plant_i}",
            0.0,
            lambda: (
                1.0 +
                0.001 * population.value +
                numpy.array([-1.0, 2.0]) @ weather.one_hot
            )
        )
        population_variables[population.name] = population

    # create simulation
    simulation = Simulation(
        environment_variables=environment_variables,
        population_variables=population_variables,
    )

    # run simulation
    simulation.run(1000)

    # visualize
    first_plant_history = list(simulation.population_history.values())[0]
    plot_population_variables(first_plant_history)
    show_plot()
