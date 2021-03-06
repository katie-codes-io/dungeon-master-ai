from dmai.utils.output_builder import OutputBuilder
from dmai.utils.logger import get_logger
from dmai.utils.config import Config
from dmai.agents.agent import Agent
from dmai.planning.planning_player import PlanningPlayer
from dmai.game.state import State

logger = get_logger(__name__)


class PlayerAgent(Agent):
    def __init__(self, state: State, output_builder: OutputBuilder, **kwargs) -> None:
        """PlayerAgent class"""
        Agent.__init__(self, state, output_builder, **kwargs)

    def __repr__(self) -> str:
        return "{c}".format(c=self.__class__.__name__)

    def get_agent(self, **kwargs):
        """Returns an instance of a specified agent"""
        try:
            return self._agent_factory(Config.agent.player, **kwargs)
        except ValueError as e:
            logger.error("(SESSION {s}) {e}".format(s=self.state.session.session_id, e=e))

    def _agent_factory(self, agent: str, **kwargs):
        """Construct an instance of a specified agent"""
        try:
            agent_map = {"planning": PlanningPlayer}
            agent = agent_map[agent]
            return agent(self.state, self.output_builder, **kwargs)
        except (ValueError, KeyError) as e:
            msg = "Cannot create agent {a} - it does not exist!".format(
                a=agent)
            raise ValueError(msg)
