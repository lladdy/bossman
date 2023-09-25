from abc import ABC, abstractmethod

import numpy as np


class BaseSuccessProbabilityAlgorithm(ABC):
    """A class that calculates the probability of success for a list of choices."""

    @abstractmethod
    def calc(self, success_perc: np.ndarray, chosen_count: np.ndarray) -> dict:
        """
        Calculates the probability of success for each choice.
        :param success_perc: the success percentage of each choice
        :param chosen_count: the number of times each choice was chosen
        :return:
        """
        pass
