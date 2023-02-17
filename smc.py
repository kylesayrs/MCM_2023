from typing import Union, List

import numpy


class StochasticMarkovChain:
    def __init__(
        self,
        initial_state: Union[str, int],
        state_names: List[str],
        transitions: Union[List[List[float]], numpy.matrix],
    ):
        if type(initial_state) == str:
            self.initial_state_index = state_names.index(initial_state)
        if type(initial_state) == int:
            self.initial_state_index = initial_state
        self.state_names = state_names
        self.transitions = numpy.matrix(transitions)
        assert numpy.all(numpy.sum(transitions, axis=1) == 1.0)

        self.state_index = self.initial_state_index
        self.new_value = None


    def step(self):
        choice_probabilities = self.transitions[self.state_index].tolist()[0]
        self.new_value = numpy.random.choice(
            range(0, len(self.state_names)),
            p=choice_probabilities
        )
        return self.new_value


    def update(self):
        self.state_index = self.new_value
        self.new_value = None


    @property
    def one_hot(self):
        array = numpy.zeros(len(self.state_names))
        array[self.state_index] = 1
        return array


    def __str__(self):
        state_name = self.state_names[self.state_index]
        return f"StochasticMarkovChain(state={state_name}, states={self.state_names})"
