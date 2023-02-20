from typing import Union, List, Dict, Optional

import numpy
import matplotlib.pyplot as plt

from utils import sanitize_2d_numpy, get_time_spans, get_velocity


def plot_values(
    time_history: List[float],
    counts: Union[numpy.ndarray, List[float], List[List[float]]],
    axes: Optional[plt.Axes] = None
):
    if axes is None:
        _, axes = plt.subplots(1, 1)

    counts = sanitize_2d_numpy(counts)

    for count in counts:
        axes.plot(time_history, count)


def plot_population_time(
    time_history: List[float],
    population_history: Dict[str, List[float]],
    environment_history: Dict[str, List[float]],
    axes: Optional[plt.Axes] = None
):
    if axes is None:
        _, axes = plt.subplots(2, 1, height_ratios=[1, 3])

    # total plant history
    total_population_history = numpy.sum(list(population_history.values()), axis=0)
    axes[0].plot(time_history, total_population_history, label="total population")

    # individual plant history
    for name, history in population_history.items():
        axes[1].plot(time_history, history, label=name)

    # drought
    drought_state_to_color = {
        "none": "grey",
        "mild": "yellow",
        "severe": "red",
    }
    drought_time_spans = get_time_spans(time_history, environment_history["drought"])
    for drought_state, spans in drought_time_spans.items():
        color = drought_state_to_color[drought_state]
        for span in spans:
            axes[0].axvspan(*span, color=color, alpha=0.1)
            axes[1].axvspan(*span, color=color, alpha=0.1)

    # plot settings
    axes[0].set_xbound(0, time_history[-1])
    axes[0].set_ybound(0)
    axes[1].set_xbound(0, time_history[-1])
    axes[1].set_ybound(0)

    axes[1].set_xlabel(f"time")
    axes[0].set_ylabel(f"total population")
    axes[1].set_ylabel(f"plant populations")


def plot_population(
    population_history: Dict[str, List[float]],
    x_axis_name: str,
    y_axis_name: str,
    reduce_factor: int = 1,
    axes: Optional[plt.Axes] = None
):
    if axes is None:
        _, axes = plt.subplots(1, 1)

    x_positions = population_history[x_axis_name]
    y_positions = population_history[y_axis_name]

    x_positions = [position for index, position in enumerate(x_positions) if index % reduce_factor == 0]
    y_positions = [position for index, position in enumerate(y_positions) if index % reduce_factor == 0]

    x_velocity = get_velocity(x_positions)
    y_velocity = get_velocity(y_positions)

    axes.quiver(
        x_positions, y_positions, x_velocity, y_velocity,
        angles="xy"
    )
    axes.set_xlabel(f"{x_axis_name} population")
    axes.set_ylabel(f"{y_axis_name} population")
    axes.set_aspect("equal", "box")
    axes.set_xbound(lower=0)
    axes.set_ybound(lower=0)

    return axes


def plot_statistics(
    x_values: List[float],
    y_values: List[List[float]],
    x_axis_label: str,
    y_axis_label: str,
    labels: List[str],
    axes: Optional[plt.Axes] = None
):
    if axes is None:
        _, axes = plt.subplots(1, 1)

    assert len(y_values) == len(labels)

    for y_value, label in zip(y_values, labels):
        axes.plot(x_values, y_value, label=label)

    axes.set_xlabel(x_axis_label)
    axes.set_ylabel(y_axis_label)
    axes.legend()


def show_plot():
    plt.show()
