from abc import ABC, abstractmethod
from dmai.utils.output_builder import OutputBuilder

from dmai.game.state import State
from dmai.utils.output_builder import OutputBuilder
from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class Agent(ABC):
    def __init__(self, state: State, output_builder: OutputBuilder, **kwargs) -> None:
        """Agent abstract class"""
        self.state = state
        self.output_builder = output_builder
        self.agent = self.get_agent(**kwargs)

    def __repr__(self) -> str:
        return "{c}".format(c=self.__class__.__name__)

    @abstractmethod
    def get_agent(self, **kwargs):
        pass

    def prepare_next_move(self) -> bool:
        logger.debug("(SESSION {s}) Preparing next move: {i}".format(s=self.state.session.session_id, i=self.unique_id))
        return self.agent.prepare_next_move()

    def print_next_move(self) -> bool:
        """Method to print the next move"""
        logger.debug("(SESSION {s}) Printing next move: {i}".format(s=self.state.session.session_id, i=self.unique_id))
        move = self.agent.get_next_move()
        self.output_builder.append(move)
        return bool(move)

    def perform_next_move(self) -> bool:
        """Method to perform the next move"""
        logger.debug("(SESSION {s}) Performing next move: {i}".format(s=self.state.session.session_id, i=self.unique_id))
        self.agent.perform_next_move()
        
        # TODO parse the PDDL and act accordinging 
        # e.g. Steps of combat:
        # 1. declare target
        # 1. attack roll - damage_roll() if exceeds target AC else return
        # 2. damage roll - apply_damage()"""