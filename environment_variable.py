from typing import Union, List, Optional, Tuple

import numpy


class RandomWalk:
    def __init__(
        self,
        initial_state: float,
        bounds: Tuple[float, float],
        step_size: float,
        seed: Optional[int] = None
    ):
        self.state = initial_state
        self.bounds = bounds
        self.step_size = step_size
        self.local_random = numpy.random.RandomState(seed)

        self.new_value = None


    def step(self):
        self.new_value = self.state + self.step_size * numpy.random.choice([-1, 1])
        self.new_value = min(max(self.new_value, self.bounds[0]), self.bounds[1])
        return self.new_value


    def update(self):
        self.state = self.new_value
        self.new_value = None


    @property
    def value(self):
        return self.state


class StochasticMarkovChain:
    def __init__(
        self,
        initial_state: Union[str, int],
        state_names: List[str],
        transitions: Union[List[List[float]], numpy.ndarray],
        seed: Optional[int] = None
    ):
        if type(initial_state) == str:
            self.initial_state_index = state_names.index(initial_state)
        if type(initial_state) == int:
            self.initial_state_index = initial_state
        self.state_names = state_names
        self.transitions = numpy.array(transitions)
        self.local_random = numpy.random.RandomState(seed)
        assert numpy.all(numpy.sum(transitions, axis=1).astype(numpy.float32) == 1.0)

        self.state_index = self.initial_state_index
        self.new_value = None


    def step(self):
        choice_probabilities = self.transitions[self.state_index]
        self.new_value = self.local_random.choice(
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


    @property
    def state_name(self):
        return self.state_names[self.state_index]


    @property
    def value(self):
        return self.state_name


    def __str__(self):
        return f"StochasticMarkovChain(state={self.state_name}, states={self.state_names})"


class PollutionVariable(RandomWalk):
    def __init__(self, drought_effect: numpy.ndarray, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.drought_effect = drought_effect


class DroughtVariable(StochasticMarkovChain):
    def __init__(self, pollution_variable: PollutionVariable, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.base_transitions = self.transitions.copy()
        self.pollution_variable = pollution_variable


    def step(self):
        self.transitions = (
            self.base_transitions +
            (self.pollution_variable.value * self.pollution_variable.drought_effect)
        )
        super().step()
