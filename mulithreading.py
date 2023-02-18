import tqdm
import numpy
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt

from config import Config
from simulation import Simulation
from visualize import plot_population, show_plot


def run_simulations(seed=42):
    # seed config generator
    local_rand = numpy.random.RandomState(seed)

    # create and run simulations
    with ThreadPoolExecutor(max_workers=None) as executor:
        futures = []
        simulations = []
        progress = tqdm.tqdm(total=50)

        # species
        for initial in local_rand.uniform(0.0, 50.0, (50, 2)):
            config = Config(initial=initial)
            simulation = Simulation.from_config(config)
            future = executor.submit(simulation.run, config.max_time, progress)

            simulations.append(simulation)
            futures.append(future)

    # visualize diffeq
    _, axes = plt.subplots(1, 1)
    for simulation in simulations:
        plot_population(
            simulation.population_history,
            "plant_0", "plant_1",
            reduce_factor=20,
            axes=axes
        )
    show_plot()
