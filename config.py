import json
import numpy


class Config:
    def __init__(self, **kwargs):
        # environment arguments
        self.environment_update_period = 2.0
        self.drought_state = 0
        self.drought_names = ["no drought", "drought"]
        self.drought_transitions = numpy.array([[0.5, 0.5],
                                                [0.1, 0.9]])

        # base population arguments
        self.num_plants = 2
        self.initial = numpy.array([1.0, 1.0])
        self.growth = numpy.array([4.0, -3.0])
        self.damping = 0.0
        self.interactions = numpy.array([[0.0, -2.0],
                                         [1.0, 0.0]])  # damping on diagonal

        # drought effects
        self.drought_growth_effect = -1 * self.growth * 0.9
        self.severe_drought_growth_effect = -1 * self.growth * 2
        self.drought_interactions_effect = -1 * self.interactions * 0.5
        self.severe_drought_interactions_effect = self.interactions * 2.0

        # simulation arguments
        self.seed = 42
        self.simulation_h = 0.01
        self.max_time = 1.0

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
