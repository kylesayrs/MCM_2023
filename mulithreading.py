from typing import Dict, Any, Optional

import json
import tqdm
import numpy
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt

from config import Config
from simulation import Simulation
from visualize import plot_population, show_plot
from metrics import compile_simulation_metrics


def run_experiments(
    num_runs: int,
    config_args: Dict[str, Any],
    seed: int = 42,
    save_file_path: Optional[str] = None,
):
    # create and run simulations
    with ThreadPoolExecutor(max_workers=None) as executor:
        futures = []
        simulations = []
        progress = tqdm.tqdm(total=num_runs)

        # species
        local_rand = numpy.random.RandomState(seed)
        for run_i in range(num_runs):
            config = Config(**config_args, seed=local_rand.randint(0, 1 << 32))
            simulation = Simulation.from_config(config)
            future = executor.submit(simulation.run, config.max_time, progress)
            simulations.append(simulation)
            futures.append(future)

    # visualize diffeq
    """
    _, axes = plt.subplots(1, 1)
    for simulation in simulations:
        plot_population(
            simulation.population_history,
            "plant_0", "plant_1",
            reduce_factor=20,
            axes=axes
        )
    show_plot()
    """

    if save_file_path is not None:
        with open(save_file_path, "w") as file:
            json.dump(
                {
                    "config": Config(**config_args).json(),
                    "statistics": compile_simulation_metrics(simulations),
                },
                file,
                indent=4,
            )

    return simulations
