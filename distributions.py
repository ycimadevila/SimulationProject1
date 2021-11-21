import numpy as np
import math 


class Distributions:
    def uniform(a, b, u):
        return a + (b - a) * u

    def exponential(lambda_, u):
        return (-1 / lambda_) * math.log(np.e, u)
        