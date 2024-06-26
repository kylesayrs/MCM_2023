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
                if plant_history[span[0]] > 0.0 else 0.0
            )
            for span in spans
        ]
        for drought_state_name, spans in drought_spans.items()
    }


def get_variability_values(plant_history: List[float]):
    return numpy.var(plant_history)


def get_recovery_rate_values(
    time_history: List[float],
    drought_history: List[float],
    plant_history: List[float],
):
    drought_spans = get_spans(drought_history)
    mean_population = numpy.mean(plant_history)
    values = {}

    if "mild" in drought_spans:
        values["mild"] = _get_recovery_rate_values_for_state(
            time_history,
            drought_spans,
            plant_history,
            mean_population,
            "mild"
        )

    if "severe" in drought_spans:
        values["severe"] = _get_recovery_rate_values_for_state(
            time_history,
            drought_spans,
            plant_history,
            mean_population,
            "severe"
        )

    return values


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

    plant_mean_values = {
        plant_name: numpy.mean(population_histories_with_total[plant_name])
        for plant_name, plant_history in population_histories_with_total.items()
    }

    plant_variability_values = {
        plant_name: get_variability_values(
            population_histories_with_total[plant_name]
        )
        for plant_name, plant_history in population_histories_with_total.items()
    }

    plant_recovery_rate_values = {
        plant_name: get_recovery_rate_values(
            simulation.time_history,
            simulation.environment_history["drought"],
            plant_history
        )
        for plant_name, plant_history in population_histories_with_total.items()
    }

    statistics = {
        "population_resistance": {
            plant_name: generate_mean_std(values_dict)
            for plant_name, values_dict in plant_resistance_values.items()
        },
        "population_recovery_rate": {
            plant_name: generate_mean_std(values_dict)
            for plant_name, values_dict in plant_recovery_rate_values.items()
        },
        "population_variability": {
            plant_name: variability
            for plant_name, variability in plant_variability_values.items()
        },
        "population_mean": plant_mean_values
    }

    if stringify:
        return json.dumps(statistics, indent=4)
    else:
        return statistics


def compile_simulation_metrics(simulations: List[Simulation], stringify: bool = False):
    simulation_statistics = [get_simulation_statistics(simulation) for simulation in simulations]

    mean_resistances_dict = {
        drought_state_name: [
            statistics["population_resistance"]["total"][drought_state_name]["mean"]
            for statistics in simulation_statistics
        ]
        for drought_state_name in simulation_statistics[0]["population_resistance"]["total"].keys()
    }

    mean_recovery_rate_dict = {
        drought_state_name: [
            statistics["population_recovery_rate"]["total"][drought_state_name]["mean"]
            for statistics in simulation_statistics
        ]
        for drought_state_name in simulation_statistics[0]["population_recovery_rate"]["total"].keys()
    }

    means = [
        statistics["population_mean"]["total"]
        for statistics in simulation_statistics
    ]

    variabilities = [
        statistics["population_variability"]["total"]
        for statistics in simulation_statistics
    ]

    compiled_statistics = {
        "mean_resistance": generate_mean_std(mean_resistances_dict),
        "mean_recovery_rate": generate_mean_std(mean_recovery_rate_dict),
    }
    compiled_statistics.update(
        generate_mean_std({"population_variability": variabilities})
    )
    compiled_statistics.update(
        generate_mean_std({"population_means": means})
    )

    if stringify:
        return json.dumps(compiled_statistics, indent=4)
    else:
        return compiled_statistics


def _get_recovery_rate_values_for_state(
    time_history: List[float],
    drought_spans: Dict[str, List[List[int]]],
    plant_history: List[float],
    mean_population: float,
    drought_state: str,
):
    values = []

    for span_i, span in enumerate(drought_spans[drought_state]):
        if span_i >= len(drought_spans[drought_state]) - 1:
            break

        if plant_history[span[1]] >= mean_population:
            continue

        next_span = drought_spans[drought_state][span_i + 1]
        for span_offset, plant_population_value in enumerate(plant_history[span[1]: next_span[0]]):
            if plant_population_value >= mean_population:
                values.append((
                    (plant_history[span[1] + span_offset] - plant_history[span[1]])) /
                    (time_history[span[1] + span_offset] - time_history[span[1]])
                )
                break

    return values
