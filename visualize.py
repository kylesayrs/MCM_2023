from typing import Union, List

import numpy
import matplotlib.pyplot as plt


def sanitize_2d_numpy(array_input):
    array = numpy.array(array_input)
    if len(array.shape) == 1:
        array = numpy.array([array])

    return array


def plot_values(counts: Union[numpy.ndarray, List[float], List[List[float]]]):
    counts = sanitize_2d_numpy(counts)
    fig, ax = plt.subplots(1, 1)

    time_data = range(0, counts.shape[1])
    for count in counts:
        ax.plot(time_data, count)


def plot_population_variables(counts: Union[numpy.ndarray, List[float], List[List[float]]]):
    counts = sanitize_2d_numpy(counts)
    fig, ax = plt.subplots(1, 1)

    time_data = range(0, counts.shape[1])
    for count in counts:
        ax.plot(time_data, count)
