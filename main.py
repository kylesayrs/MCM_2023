import numpy

from config import BaseConfig
from simulation import Simulation
from population_variable import make_plant_population_variables
from visualize import plot_population_time, plot_population, show_plot


if __name__ == "__main__":
    # set up configuration
    config = BaseConfig()
    config.seed = 42
    numpy.random.seed(config.seed)

    # create population variables
    populations = make_plant_population_variables(
        config.num_species,
        config.initial,
        config.growth,
        config.interactions,
    )

    # create simulation
    simulation = Simulation(
        environment_variables={},
        population_variables=populations,
        simulation_h=config.simulation_h,
    )

    # run simulation
    simulation.run(max_time=1)

    # visualize
    plot_population_time(
        simulation.time_history,
        simulation.population_history
    )
    show_plot()
    plot_population(
        simulation.population_history,
        "plant_0", "plant_1",
        reduce_factor=10
    )
    show_plot()
