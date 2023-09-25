import math

import numpy as np

from bossman.algorithm.base_success_probability_algorithm import BaseSuccessProbabilityAlgorithm


class UCB1(BaseSuccessProbabilityAlgorithm):
    """
    Based on https://www.chessprogramming.org/UCT
    Upper confidence bound:
    UCB1 = win percentage + C * sqrt(ln(total_games) / visits)
    """

    def __init__(self, explore_constant=1.4):
        self.explore_constant = explore_constant

    def calc(self, success_perc: np.ndarray, chosen_count: np.ndarray) -> dict:
        total_games = np.sum(chosen_count)
        if total_games > 0:
            return success_perc + self.explore_constant * np.sqrt(
                math.log(total_games + 1) / chosen_count,
                out=np.ones_like(chosen_count, dtype=float) * 1e100,
                where=(chosen_count != 0),
            )
        return np.ones_like(chosen_count, dtype=float)

