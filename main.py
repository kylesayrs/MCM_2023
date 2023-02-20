from typing import Dict, Any

import numpy

from config import Config
from simulation import Simulation
from visualize import plot_population_time, plot_population, show_plot
from mulithreading import run_experiments
from metrics import get_simulation_statistics


def run_single_simulation(config_args: Dict[str, Any]):
    # create and run simulations
    config = Config(**config_args)
    simulation = Simulation.from_config(config)
    simulation.run(config.max_time)

    # print config
    # print(config)

    # print simulation statistics
    simulation_statistics = get_simulation_statistics(simulation, stringify=True)
    print(simulation_statistics)

    # visualize population
    plot_population_time(
        simulation.time_history,
        simulation.population_history,
        simulation.environment_history,
    )
    show_plot()

    # visualize diffeq
    """
    plot_population(
        simulation.population_history,
        "plant_0", "plant_1",
        reduce_factor=1,
    )
    show_plot()
    """


if __name__ == "__main__":
    run_single_simulation({"num_plants": 10})
    #simulations = run_experiments(20, {"num_plants": 2}, seed=42, save_file_path="./results.json")

