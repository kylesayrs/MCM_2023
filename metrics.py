from typing import Dict, List

import json
import numpy

from utils import get_spans
from simulation import Simulation


def generate_mean_std(values_dict: Dict[str, List[float]]):
    return {
        key: {
            "mean": numpy.mean(values),
            "std": numpy.std(values)
        }
        for key, values in values_dict.items()
    }


def get_resistance_values(
    time_history: List[float],
    drought_history: List[float],
    plant_history: List[float],
):
    drought_spans = get_spans(drought_history)
    return {
        drought_state_name: [
            (
                (plant_history[span[0]] - plant_history[span[1]]) /
                (plant_history[span[0]] * (time_history[span[0]] - time_history[span[1]]))
            )
            for span in drought_spans
        ]
        for drought_state_name, drought_spans in drought_spans.items()
    }


def get_variability(values: List[float]):
    return numpy.var(values)


def get_simulation_statistics(simulation: Simulation, stringify: bool = False):
    total_population_history = numpy.sum(list(simulation.population_history.values()), axis=0)
    population_histories_with_total = simulation.population_history.copy()
    population_histories_with_total["total"] = total_population_history

    plant_resistance_values = {
        plant_name: get_resistance_values(
            simulation.time_history,
            simulation.environment_history["drought"],
            plant_history,
        )
        for plant_name, plant_history in population_histories_with_total.items()
    }

    plant_variability_values = {
        plant_name: get_variability(
            population_histories_with_total[plant_name]
        )
        for plant_name, plant_history in population_histories_with_total.items()
    }

    statistics = {
        "resistance": {
            plant_name: generate_mean_std(values_dict)
            for plant_name, values_dict in plant_resistance_values.items()
        },
        "variability": {
            plant_name: variability
            for plant_name, variability in plant_variability_values.items()
        }
    }

    if stringify:
        return json.dumps(statistics, indent=4)
    else:
        return statistics


def compile_simulation_metrics(simulations: List[Simulation], stringify: bool = False):
    simulation_statistics = [get_simulation_statistics(simulation) for simulation in simulations]

    mean_resistances_dict = {
        drought_state_name: [
            statistics["resistance"]["total"][drought_state_name]["mean"]
            for statistics in simulation_statistics
        ]
        for drought_state_name in simulation_statistics[0]["resistance"]["total"].keys()
    }

    mean_variability = [
        statistics["variability"]["total"]
        for statistics in simulation_statistics
    ]

    compiled_statistics = {
        "mean_resistance": generate_mean_std(mean_resistances_dict)
    }
    compiled_statistics.update(
        generate_mean_std({"mean_variability": mean_variability})
    )

    if stringify:
        return json.dumps(compiled_statistics, indent=4)
    else:
        return compiled_statistics
