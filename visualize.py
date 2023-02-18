from typing import Union, List, Dict

import numpy
import matplotlib.pyplot as plt


def plot_values(
    time_history: List[float],
    counts: Union[numpy.ndarray, List[float], List[List[float]]]
):
    counts = _sanitize_2d_numpy(counts)
    fig, ax = plt.subplots(1, 1)

    for count in counts:
        ax.plot(time_history, count)


def plot_population_time(
    time_history: List[float],
    population_history: Dict[str, List[float]]
):
    fig, ax = plt.subplots(1, 1)

    for name, history in population_history.items():
        ax.plot(time_history, history, label=name)

    ax.legend()


def plot_population(
    population_history: Dict[str, List[float]],
    x_axis_name: str,
    y_axis_name: str,
    reduce_factor: int = 1,
):
    fig, ax = plt.subplots(1, 1)

    x_positions = population_history[x_axis_name]
    y_positions = population_history[y_axis_name]

    x_positions = [position for index, position in enumerate(x_positions) if index % reduce_factor == 0]
    y_positions = [position for index, position in enumerate(y_positions) if index % reduce_factor == 0]

    x_velocity = _get_velocity(x_positions)
    y_velocity = _get_velocity(y_positions)

    ax.quiver(
        x_positions, y_positions, x_velocity, y_velocity,
        angles="xy"
    )
    ax.set_xlabel(f"{x_axis_name} population")
    ax.set_ylabel(f"{y_axis_name} population")
    ax.set_aspect("equal", "box")


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
