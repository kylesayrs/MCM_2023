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
    initial = numpy.array([7.0, 6.0])
    growth = numpy.array([4.0, 3.0])
    interactions = numpy.array([[0.0, -2.0],
                                [-1.0, 0.0]])
    populations = make_plant_population_variables(2, initial, growth, interactions)

    # create simulation
    simulation = Simulation(
        environment_variables={},
        population_variables=populations,
        simulation_h=0.00001,
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
