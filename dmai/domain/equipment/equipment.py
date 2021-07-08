from abc import ABC, abstractmethod

from dmai.utils.config import Config
from dmai.utils.logger import get_logger

logger = get_logger(__name__, Config.session.session_id)


class Equipment(ABC):
    def __init__(self, equipment_data: dict) -> None:
        """Equipment abstract class"""
        try:
            for key in equipment_data:
                self.__setattr__(key, equipment_data[key])

        except AttributeError as e:
            logger.error(
                "Cannot create equipment, incorrect attribute: {e}".format(
                    e=e))
            raise

    def __repr__(self) -> str:
        return "{c}: {n}".format(c=self.__class__.__name__, n=self.name)

    def use(self) -> None:
        print("Using this doesn't do anything special")
        return True

    def stop(self) -> None:
        return True