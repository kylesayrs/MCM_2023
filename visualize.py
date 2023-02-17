from typing import Union, List

import numpy
import matplotlib.pyplot as plt


def sanitize_2d_numpy(array_input):
    array = numpy.array(array_input)
    if len(array.shape) == 1:
        array = numpy.array([array])

    return array


def plot_values(time, counts: Union[numpy.ndarray, List[float], List[List[float]]]):
    counts = sanitize_2d_numpy(counts)
    fig, ax = plt.subplots(1, 1)

    for count in counts:
        ax.plot(time, count)


def plot_population_variables(time, counts: Union[numpy.ndarray, List[float], List[List[float]]]):
    counts = sanitize_2d_numpy(counts)
    fig, ax = plt.subplots(1, 1)

    for count in counts:
        ax.plot(time, count)


def show_plot():
    plt.show()
