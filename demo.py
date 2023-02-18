import matplotlib.pyplot as plt

from config import BaseConfig
from simulation import Simulation
from smc import StochasticMarkovChain
from population_variable import PopulationVariable, make_plant_population_variables
from visualize import plot_values, plot_population_time, plot_population, show_plot


def demo_smc():
    smc = StochasticMarkovChain(
        "sunny",
        ["rainy", "sunny"],
        [[0.9, 0.1],
         [0.5, 0.5]]
    )

    smc_state_history = [smc.step() for _ in range(1000)]

    plot_values(list(range(1000)), smc_state_history)
    plt.show()


def demo_population_variable():
    variable = PopulationVariable(
        "plant_y",
        0.0,
        lambda: 1.0 + 0.001 * variable.value
    )

    variable_value_history = []
    for _ in range(1000):
        variable_value_history.append(variable.step())
        variable.update()

    plot_values(list(range(1000)), variable_value_history)
    plt.show()


def demo_variable_and_smc():
    smc = StochasticMarkovChain(
        "sunny",
        ["rainy", "sunny"],
        [[0.9, 0.1],
         [0.5, 0.5]]
    )

    variable = PopulationVariable(
        "plant_y",
        0.0,
        lambda: 1.0 + 0.001 * variable.value - 7 * smc.state_index
    )

    variable_value_history = []
    for _ in range(1000):
        smc.step()
        smc.update()
        variable_value_history.append(variable.step())
        variable.update()

    plot_values(list(range(1000)), variable_value_history)
    plt.show()


def demo_simulation():
    # set up configuration
    config = BaseConfig()

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


if __name__ == "__main__":
    #demo_smc()
    #demo_population_variable()
    #demo_variable_and_smc()
    demo_simulation()
