from config import BaseConfig
from simulation import Simulation
from plants import make_plant_environment_variables, make_plant_population_variables
from visualize import plot_population_time, plot_population, show_plot


if __name__ == "__main__":
    # set up configuration
    config = BaseConfig()

    # create and run simulation
    simulation = Simulation.from_config(config)
    simulation.run(max_time=config.max_time)

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
