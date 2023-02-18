from config import BaseConfig
from simulation import Simulation
from plants import make_plant_environment_variables, make_plant_population_variables
from visualize import plot_population_time, plot_population, show_plot


if __name__ == "__main__":
    # set up configuration
    config = BaseConfig()

    # environment variables
    environment_variables = make_plant_environment_variables(
        config.drought_state,
        config.drought_names,
        config.drought_transitions,
    )

    # create population variables
    population_variables = make_plant_population_variables(
        config.num_species,
        config.initial,
        config.growth,
        config.interactions,
        environment_variables,
    )

    # create simulation
    simulation = Simulation(
        environment_variables=environment_variables,
        population_variables=population_variables,
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
