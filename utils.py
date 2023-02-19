from typing import List, Any

import numpy


def sanitize_2d_numpy(array_input):
    array = numpy.array(array_input)
    if len(array.shape) == 1:
        array = numpy.array([array])

    return array


def get_velocity(positions: List[float]):
    return [0.0] + [
        s1 - s0
        for s0, s1 in zip(
            positions,
            positions[1:]
        )
    ]


def get_spans(values: List[Any]):
    completed_spans = {
        key: []
        for key in numpy.unique(values)
    }
    current_span_value = values[0]
    left_index = 0

    for value_i, value in enumerate(values[1:]):
        if value != current_span_value:
            completed_spans[current_span_value].append([
                left_index, value_i
            ])

            current_span_value = value
            left_index = value_i

    completed_spans[value].append([
        left_index, value_i
    ])

    return completed_spans


def get_time_spans(time_history: List[float], values: List[Any]):
    spans = get_spans(values)
    return {
        key: [
            [time_history[span[0]], time_history[span[1]]]
            for span in spans
        ]
        for key, spans in spans.items()
    }
