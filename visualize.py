from typing import Union, List, Dict, Optional, Any

import numpy
import matplotlib.pyplot as plt


def plot_values(
    time_history: List[float],
    counts: Union[numpy.ndarray, List[float], List[List[float]]],
    axes: Optional[plt.Axes] = None
):
    if axes is None:
        _, axes = plt.subplots(1, 1)

    counts = _sanitize_2d_numpy(counts)

    for count in counts:
        axes.plot(time_history, count)


def plot_population_time(
    time_history: List[float],
    population_history: Dict[str, List[float]],
    environment_history: Dict[str, List[float]],
    axes: Optional[plt.Axes] = None
):
    if axes is None:
        _, axes = plt.subplots(1, 1)

    for name, history in population_history.items():
        axes.plot(time_history, history, label=name)

    drought_state_to_color = {
        "none": "grey",
        "mild": "yellow",
        "severe": "red",
    }
    drought_spans = _get_time_spans(time_history, environment_history["drought"])
    for drought_state, spans in drought_spans.items():
        color = drought_state_to_color[drought_state]
        for span in spans:
            axes.axvspan(*span, color=color, alpha=0.3)

    axes.set_xbound(lower=0)
    axes.set_ybound(lower=0)
    axes.legend()


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

    x_velocity = _get_velocity(x_positions)
    y_velocity = _get_velocity(y_positions)

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


def show_plot():
    plt.show()


def _sanitize_2d_numpy(array_input):
    array = numpy.array(array_input)
    if len(array.shape) == 1:
        array = numpy.array([array])

    return array


def _get_velocity(positions: List[float]):
    return [0.0] + [
        s1 - s0
        for s0, s1 in zip(
            positions,
            positions[1:]
        )
    ]


def _get_time_spans(time_history: List[float], values: List[Any]):
    completed_spans = {
        key: []
        for key in numpy.unique(values)
    }
    current_span_value = values[0]
    left_index = 0

    for value_i, value in enumerate(values[1:]):
        if value != current_span_value:
            completed_spans[current_span_value].append([
                time_history[left_index], time_history[value_i]
            ])

            current_span_value = value
            left_index = value_i

    completed_spans[value].append([
        time_history[left_index], time_history[value_i]
    ])

    return completed_spans
