import json
import numpy


class Config:
    def __init__(self, **kwargs):
        # environment arguments
        self.environment_update_period = 0.1  # period over time
        self.drought_state = 0
        self.drought_names = ["none", "mild", "severe"]
        self.drought_transitions = numpy.array([[0.90, 0.05, 0.05],
                                                [0.25, 0.50, 0.25],
                                                [0.25, 0.25, 0.50]])

        # base population arguments
        self.num_plants = 2
        self.initial = numpy.array([50.0, 50.0])
        self.growth = numpy.array([1.01, 1.03])
        self.damping = -0.001
        self.interactions = numpy.array([[0.0, -0.0003],
                                         [-0.0008, 0.0]])  # damping on diagonal

        # mild drought effects
        self.mild_growth_effect = -0.9 * self.growth
        self.mild_interactions_effect = -0.7 * self.interactions

        # severe drought effects
        self.severe_growth_effect = -2 * self.growth
        self.severe_interactions_effect = 2.0 * self.interactions

        # simulation arguments
        self.seed = 42
        self.simulation_h = 0.01
        self.max_time = 10.0

        # custom arguments
        self.__dict__.update(kwargs)

        # augmentations
        numpy.fill_diagonal(self.interactions, self.damping)
        self.check_arguments()


    def check_arguments(self):
        assert (
            self.num_plants ==
            self.initial.shape[0] ==
            self.growth.shape[0] ==
            self.interactions.shape[0] ==
            self.interactions.shape[1]
        )


    def __str__(self):
        tmp = self.__dict__.copy()
        for key in tmp:
            if type(tmp[key]) == numpy.ndarray:
                tmp[key] = tmp[key].tolist()
        return json.dumps(tmp, indent=4)


    def copy(self):
        return Config(**self.__dict__)
