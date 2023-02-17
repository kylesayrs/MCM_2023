import numpy
import matplotlib.pyplot as plt

from config import Config
from smc import StochasticMarkovChain
from population_variable import PopulationVariable
from visualize import plot_values, plot_population_variables


def demo_smc():
    smc = StochasticMarkovChain(
        "sunny",
        ["rainy", "sunny"],
        [[0.9, 0.1],
         [0.5, 0.5]]
    )

    smc_state_history = [smc.step() for _ in range(1000)]

    plot_values(smc_state_history)
    plt.show()


def demo_population_variable():
    variable = PopulationVariable(
        "plant_y",
        0.0,
        lambda: 1.0 + 0.001 * variable.value
    )

    variable_value_history = [variable.step() for _ in range(1000)]

    plot_population_variables(variable_value_history)
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
        lambda: 1.0 + 0.001 * variable.value - 2 * smc.state_index
    )

    variable_value_history = []
    for _ in range(1000):
        smc.step()
        variable_value_history.append(variable.step())

    plot_population_variables(variable_value_history)
    plt.show()


if __name__ == "__main__":
    numpy.random.seed(Config.SEED)

    #demo_smc()
    #demo_population_variable()
    demo_variable_and_smc()
