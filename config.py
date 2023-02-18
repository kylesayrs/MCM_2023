import numpy


class BaseConfig:
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

        assert (
            self.num_species ==
            self.initial.shape[0] ==
            self.growth.shape[0] ==
            self.interactions.shape[0] ==
            self.interactions.shape[1]
        )


    def __str__(self):
        return self.__dict__
