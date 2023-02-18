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
    populations = {
        "plant_x": PopulationVariable(f"plant_x", 1.0),
        "plant_y": PopulationVariable(f"plant_y", 1.0)
    }

    populations["plant_x"].ddt = (
        lambda:
        4.0 * populations["plant_x"].value +
        (numpy.array([0, -2.0]) @ numpy.array([var.value for var in populations.values()])) * populations["plant_x"].value
    )
    populations["plant_y"].ddt = (
        lambda:
        -3.0 * populations["plant_y"].value +
        (numpy.array([1.0, 0]) @ numpy.array([var.value for var in populations.values()])) * populations["plant_y"].value
    )

    # create simulation
    simulation = Simulation(
        environment_variables={},
        population_variables=populations,
        simulation_h=0.0001,
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
        simulation.population_history,
        "plant_x", "plant_y",
        reduce_factor=1000
    )
    show_plot()
