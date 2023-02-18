import numpy


class BaseConfig:
    # environment arguments
    drought_state = 0
    drought_names = ["no drought", "drought"]
    drought_transitions = numpy.array([[0.95, 0.05],
                                       [0.1, 0.9]])

    # population arguments
    num_species = 2
    initial = numpy.array([7.0, 6.0])
    growth = numpy.array([4.0, 3.0])
    damping = -0.001
    interactions = numpy.array([[damping, -2.0],
                                [-1.0, damping]])

    # simulation arguments
    seed = 42
    simulation_h = 0.00001

    def __init__(self):
        numpy.fill_diagonal(self.interactions, self.damping)

        self.check_arguments()


    def check_arguments(self):
        assert (
            self.num_species ==
            self.initial.shape[0] ==
            self.growth.shape[0] ==
            self.interactions.shape[0] ==
            self.interactions.shape[1]
        )


    def __str__(self):
        return self.__dict__
