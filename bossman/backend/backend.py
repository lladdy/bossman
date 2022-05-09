from abc import ABC, abstractmethod
from enum import Enum


class BackendType(Enum):
    JSON = 1


class Backend(ABC):
    """An abstract bossman backend"""

    @abstractmethod
    def load_decision_stats(self) -> dict:
        pass

    @abstractmethod
    def save(self, decision_stats, match_decision_history):
        pass
