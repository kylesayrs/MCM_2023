from typing import Optional

import json
import numpy


class Config:
    def __init__(self, seed: Optional[int] = 42, num_plants: int = 2, **kwargs):
        # config seed
        self.seed = seed
        local_rand = numpy.random.RandomState(self.seed)

        # environment arguments
        self.environment_update_period = 0.1  # period over time
        self.drought_state = 0
        self.drought_names = ["none", "mild", "severe"]
        # based on massachusetts 2022 drought data
        numpy.array([[0.944, 0.056, 0.0],
                     [0.0952, 0.857, 0.0478],
                     [0.0, 0.4, 0.6]])


        # base population arguments
        self.num_plants = num_plants
        self.initial = numpy.array([100 / self.num_plants] * self.num_plants)
        self.growth = local_rand.normal(
            0.3, 0.05, (self.num_plants,)
        )
        self.growth[self.growth < 0.0] = 0.0  # enforce positivity
        self.damping = -0.01  # should be greater magnitude than interactions
        self.interactions = local_rand.normal(
            -0.0003, 0.0012, (self.num_plants, self.num_plants)
        )  # damping on diagonal

        # mild drought effects
        self.mild_growth_effect = -0.9 * self.growth
        self.mild_interactions_effect = -0.7 * self.interactions

        # severe drought effects
        self.severe_growth_effect = -1.5 * self.growth
        self.severe_interactions_effect = 4.0 * self.interactions

        # simulation arguments
        self.simulation_h = 0.01
        self.max_time = 100.0

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
