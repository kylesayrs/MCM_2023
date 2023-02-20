from typing import Optional

import json
import numpy


class Config:
    def __init__(self, seed: Optional[int] = 42, num_plants: int = 2, **kwargs):
        # config and simulation seed
        self.seed = seed
        local_rand = numpy.random.RandomState(self.seed)

        # simulation arguments
        self.simulation_h = 0.01
        self.max_time = 500.0

        # environment arguments
        self.environment_update_period = 0.1  # period over time
        self.drought_state = 0
        self.drought_names = ["none", "mild", "severe"]
        # based on massachusetts 2022 drought data
        self.drought_transitions = numpy.array([[0.944, 0.056, 0.0],
                                                [0.0952, 0.857, 0.0478],
                                                [0.0, 0.4, 0.6]])
        self.pollution_state = 0.0
        self.pollution_bounds = (0.0, 1.0)
        self.pollution_step_size = (
            min(self.drought_transitions[0:2][:, 0]) /
            self.max_time *
            self.environment_update_period
        )
        self.pollution_drought_effect = numpy.array([[-1, 0.75, 0.25],
                                                     [-1, 0.75, 0.25],
                                                     [0.0, 0.0, 0.0]])

        # base population arguments
        self.num_plants = num_plants
        self.initial = numpy.array([100 / self.num_plants] * self.num_plants)
        self.growth = local_rand.normal(0.3, 0.05, (self.num_plants,))
        self.growth[self.growth < 0.0] = 0.0  # enforce positivity
        self.damping = -0.01  # should be greater magnitude than interactions
        
        # competitive
        self.interactions = self.interactions = local_rand.normal(
            -0.0007, 0.00012, (self.num_plants, self.num_plants)
        )

        # extreme competition
        '''
        self.interactions = self.interactions = local_rand.normal(
                    -0.01, 0.00012, (self.num_plants, self.num_plants)
                )
        '''

       # parasitic
        '''
       self.interactions = self.interactions = local_rand.normal(
                   -0.000001, 0.0002, (self.num_plants, self.num_plants)
               )
        '''

       # symbiotic
        '''
       i_val = random.randint(1,num_plants-1)
       j_val = random.randint(1, num_plants-1)

       while i_val == j_val:
            j_val = random.randint(1, num_plants-1)

       self.interactions = self.interactions = local_rand.normal(
                   -0.0007, 0.00012, (self.num_plants, self.num_plants)
               )

       self.interactions[i][j] = local_rand.normal(0.0007, 0.00012)
       self.interactions[j][i] = local_rand.normal(0.0007, 0.00012)

        '''
        
        
        numpy.fill_diagonal(self.interactions, self.damping)
        self.population_limit = 200.0
        self.population_limit_change = -1 * self.population_limit * 0.3 / self.max_time * self.environment_update_period

        # mild drought effects
        self.mild_growth_effect = -0.9 * self.growth
        self.mild_interactions_effect = -0.7 * self.interactions

        # severe drought effects
        self.severe_growth_effect = -1.5 * self.growth
        self.severe_interactions_effect = 3.0 * self.interactions

        # custom arguments
        self.__dict__.update(kwargs)

        # check arguments
        self.check_arguments()


    def check_arguments(self):
        assert (
            self.num_plants ==
            self.initial.shape[0] ==
            self.growth.shape[0] ==
            self.interactions.shape[0] ==
            self.interactions.shape[1]
        )

        assert numpy.all(numpy.sum(self.drought_transitions, axis=1).astype(numpy.float32) == 1.0)
        assert numpy.all(numpy.sum(self.pollution_drought_effect, axis=1).astype(numpy.float32) == 0.0)


    def __str__(self):
        return json.dumps(self.json(), indent=4)


    def json(self):
        tmp = self.__dict__.copy()
        for key in tmp:
            if type(tmp[key]) == numpy.ndarray:
                tmp[key] = tmp[key].tolist()

        return tmp

    def copy(self):
        return Config(**self.__dict__)
