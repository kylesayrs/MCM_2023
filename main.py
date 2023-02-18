import numpy
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt

from config import Config
from simulation import Simulation
from visualize import plot_population_time, plot_population, show_plot


if __name__ == "__main__":
    # set up configuration
    config = Config()

    # create and run simulations
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = []
        simulations = []
        for initial in numpy.random.uniform(0.0, 7.0, (30, 2)):
            config = Config(initial=initial)
            simulation = Simulation.from_config(config)
            future = executor.submit(simulation.run, config.max_time)

            simulations.append(simulation)
            futures.append(future)

    # visualize time
    """
    _, plt_axes = plt.subplots(1, 1)
    for simulation in simulations:
        plot_population_time(
            simulation.time_history,
            simulation.population_history,
            plt_axes=plt_axes,
        )
    show_plot()
    """

    # visualize diffeq
    _, plt_axes = plt.subplots(1, 1)
    for simulation in simulations:
        plot_population(
            simulation.population_history,
            "plant_0", "plant_1",
            reduce_factor=20,
            plt_axes=plt_axes
        )
    show_plot()
