from abc import ABC, abstractmethod

from dmai.utils.output_builder import OutputBuilder
from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class Agent(ABC):
    def __init__(self, **kwargs) -> None:
        """Agent abstract class"""
        self.agent = self.get_agent(**kwargs)

    def __repr__(self) -> str:
        return "{c}".format(c=self.__class__.__name__)

    @abstractmethod
    def get_agent(self, **kwargs):
        pass

    def get_next_move(self) -> None:
        OutputBuilder.append(self.agent.get_next_move())