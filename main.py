from typing import Dict, Any

import numpy

from config import Config
from simulation import Simulation
from visualize import plot_population_time, plot_population, show_plot, plot_statistics
from mulithreading import run_experiments
from metrics import get_simulation_statistics
from metrics import compile_simulation_metrics


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
    run_single_simulation({"num_plants": 20})
    exit(0)

    x_values = list(range(1, 26, 1))
    y_values = []
    for num_plants in x_values:
        simulations = run_experiments(20, {"num_plants": num_plants}, seed=42)
        results = compile_simulation_metrics(simulations)
        y_values.append(results["mean_recovery_rate"])

    plot_statistics(
        x_values,
        [
            [
                y_value["mild"]["mean"]
                for y_value in y_values
            ],
            [
                y_value["severe"]["mean"]
                for y_value in y_values
            ],
        ],
        [
            [
                y_value["mild"]["std"]
                for y_value in y_values
            ],
            [
                y_value["severe"]["std"]
                for y_value in y_values
            ],
        ],
        "Number of Plant Species",
        "Recovery Rate",
        ["mild", "severe"],
    )
    show_plot()
