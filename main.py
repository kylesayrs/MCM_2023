import matplotlib.pyplot as plt

from config import Config
from simulation import Simulation
from visualize import plot_population, show_plot
from mulithreading import run_simulations


def run_simulation():
    # create and run simulations
    config = Config()
    simulation = Simulation.from_config(config)
    simulation.run(config.max_time)

    # visualize diffeq
    _, plt_axes = plt.subplots(1, 1)
    plot_population(
        simulation.population_history,
        "plant_0", "plant_1",
        reduce_factor=20,
        plt_axes=plt_axes
    )
    show_plot()


if __name__ == "__main__":
    #run_simulation()
    run_simulations()
