
import numpy as np
from scipy.special import expit

from bossman.algorithm.base_success_probability_algorithm import BaseSuccessProbabilityAlgorithm


class WeightedSuccessRate(BaseSuccessProbabilityAlgorithm):
    """
    Returns the choice success rate, modified to preference choices with low sample size.
    """

    def __init__(self, mod: int = 1.0):
        """

        :param mod: The higher this value, the quicker the weight fall off as chosen_count climbs
        """
        self.mod = mod

    def calc(self, success_perc: np.ndarray, chosen_count: np.ndarray) -> dict:
        """
        mod: The higher this value, the quicker the weight fall off as chosen_count climbs
        """
        # calculate a weight that will make low sample size choices more likely
        probability_weight = 1 - (expit(chosen_count * self.mod) - 0.5) * 2

        # Apply that weight to each choice's win percentage
        return success_perc + probability_weight
