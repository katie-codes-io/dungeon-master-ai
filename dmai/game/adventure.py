from typing import Generator

from dmai.game.state import State
from dmai.utils.loader import Loader
from dmai.utils.text import Text
from dmai.game.world.room import Room
from dmai.utils.output_builder import OutputBuilder
from dmai.utils.exceptions import UnrecognisedRoomError
from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class Adventure:

    # class variables
    adventure_data = dict()

    def __init__(self, adventure: str, state: State, output_builder: OutputBuilder) -> None:
        """Main class for the adventure"""
        self.adventure = adventure
        self.state = state
        self.output_builder = output_builder
        self._load_adventure_data(self.adventure)

        try:
            for key in self.adventure_data:
                self.__setattr__(key, self.adventure_data[key])
        except AttributeError as e:
            logger.error("(SESSION {s}) Cannot create adventure, incorrect attribute: {e}".format(s=self.state.session.session_id, e=e))
            raise

        self._build_world()

    def __repr__(self) -> str:
        return "Adventure: {a}".format(a=self.title)

    @classmethod
    def _load_adventure_data(cls, adventure) -> None:
        """Set the cls.adventure_data class variable data"""
        cls.adventure_data = Loader.load_adventure(adventure)

    def _build_world(self) -> None:
        """Method to build the world"""
        self.rooms = dict()

        for room_name in self.adventure_data["rooms"]:
            room_data = self.adventure_data["rooms"][room_name]
            room = Room(room_data, self.state, self.output_builder)
            self.rooms[room_name] = room

    @property
    def intro_text(self) -> str:
        return self.text["intro"]

    def intro_text_generator(self) -> Generator:
        return Text.yield_text(self.text["intro"], "\n")

    def get_init_room(self) -> str:
        """Method to get the starting room"""
        for room_id in self.rooms:
            if self.rooms[room_id].init:
                return room_id

    def get_room(self, room_id: str) -> Room:
        try:
            return self.rooms[room_id]
        except KeyError as e:
            msg = "Room not recognised: {e}".format(e=e)
            raise UnrecognisedRoomError(msg)

    def get_all_rooms(self) -> list:
        """Method to return all room objects in a list.
        Returns a list of rooms"""
        return list(self.rooms.values())
