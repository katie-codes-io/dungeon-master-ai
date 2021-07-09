from dmai.utils.logger import get_logger
from dmai.utils.config import Config
from dmai.agents.agent import Agent
from dmai.planning.planning_monster import PlanningMonster
from dmai.game.state import State

logger = get_logger(__name__)


class MonsterAgent(Agent):
    def __init__(self, state: State, **kwargs) -> None:
        """MonsterAgent class"""
        Agent.__init__(self, **kwargs)
        self.state = state

    def __repr__(self) -> str:
        return "{c}".format(c=self.__class__.__name__)

    def get_agent(self, **kwargs):
        """Returns an instance of a specified agent"""
        try:
            return self._agent_factory(Config.agent.monster, **kwargs)
        except ValueError as e:
            logger.error(e)

    def _agent_factory(self, agent: str, **kwargs):
        """Construct an instance of a specified agent"""
        try:
            agent_map = {"planning": PlanningMonster}
            agent = agent_map[agent]
            return agent(self.state, **kwargs)
        except (ValueError, KeyError) as e:
            msg = "Cannot create agent {a} - it does not exist!".format(
                a=agent)
            raise ValueError(msg)
