import numpy

from config import BaseConfig
from simulation import Simulation
from smc import StochasticMarkovChain
from population_variable import PopulationVariable
from visualize import plot_values, plot_population_time, plot_population, show_plot


if __name__ == "__main__":
    # set up configuration
    config = BaseConfig()
    config.seed = 42
    numpy.random.seed(config.seed)

    # create population variables
    population_variables = {}
    population_variables["plant_x"] = PopulationVariable(f"plant_x", 30.0)
    population_variables["plant_y"] = PopulationVariable(f"plant_y", 30.0)

    population_variables["plant_x"].ddt = (
        lambda:
        0.3 * population_variables["plant_x"].value +
        (numpy.array([0, -0.01]) @ numpy.array([var.value for var in population_variables.values()])) * population_variables["plant_x"].value
    )
    population_variables["plant_y"].ddt = (
        lambda:
        0.05 * population_variables["plant_y"].value +
        (numpy.array([0.01, 0]) @ numpy.array([var.value for var in population_variables.values()])) * population_variables["plant_y"].value
    )

    # create simulation
    simulation = Simulation(
        environment_variables={},
        population_variables=population_variables,
        simulation_h=0.1,
    )

    # run simulation
    simulation.run(max_time=10)

    # visualize
    plot_population_time(
        simulation.time_history,
        simulation.population_history
    )
    show_plot()
    plot_population(
        simulation.time_history,
        simulation.population_history,
        "plant_x", "plant_y"
    )
    show_plot()
