from dmai.utils.output_builder import OutputBuilder
from dmai.domain.items.item import Item
from dmai.game.world.puzzles.puzzle_collection import PuzzleCollection
from dmai.nlg.nlg import NLG
from dmai.utils.text import Text
from dmai.game.state import State
from dmai.utils.config import Config
from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class Room:
    def __init__(self, room_data: dict, state: State, output_builder: OutputBuilder) -> None:
        """Main class for a room"""
        self.state = state
        self.output_builder = output_builder

        try:
            for key in room_data:
                self.__setattr__(key, room_data[key])

            # replace the attributes values with objects where appropriate
            self.puzzles = PuzzleCollection(self.puzzles, self.state, self.output_builder)

        except AttributeError as e:
            logger.error("(SESSION {s}) Cannot create room, incorrect attribute: {e}".format(s=self.state.session.session_id, e=e))
            raise

        # set up connections
        if self.id not in self.state.room_connect_map:
            self.state.room_connect_map[self.id] = self.connections
  
        # set up treasure
        if self.id not in self.state.room_treasure_map:
            self.state.room_treasure_map[self.id] = self.treasure

        # set up triggers
        if self.id not in self.state.room_trigger_map:
            self.state.room_trigger_map[self.id] = {}

        trigger_map = {
            "enter": self.enter,
            "visibility": self.trigger_visibility,
            "fight_ends": self.trigger_fight_ends,
        }

        # populate the self.text object
        for text_type in self.text:
            text = self.text[text_type]
            trigger = trigger_map[text_type] if text_type in trigger_map else None
            if text_type not in self.state.room_trigger_map[self.id]:
                can_trigger = text_type in trigger_map
                self.state.room_trigger_map[self.id][text_type] = can_trigger
            self.text[text_type] = {
                "text": text,
                "trigger": trigger,
            }

    def __repr__(self) -> str:
        return "Room: {a}".format(a=self.name)

    def enter(self) -> None:
        """Method when entering a room"""
        if not self.state.stationary and self.state.started:
            logger.debug("(SESSION {s}) Triggering enter in room: {r}".format(s=self.state.session.session_id, r=self.id))
            if self.id not in self.state.visited_rooms:
                self.state.visited_rooms.append(self.id)
                self.output_builder.append(self.text["enter"]["text"])
            else:
                self.output_builder.append(NLG.enter_room(self.name))
            self.state.halt()

    def trigger_visibility(self) -> str:
        """Method when triggering visibility text"""
        if not self.visibility:
            if self.state.torch_lit or self.state.get_player().character.has_darkvision():
                logger.debug("(SESSION {s}) Triggering visibility in room: {r}".format(s=self.state.session.session_id, r=self.id))
                self.output_builder.append(self.text["visibility"]["text"])
                self.state.room_trigger_map[self.id]["visibility"] = False

    def trigger_fight_ends(self) -> str:
        """Method when triggering fight ends text"""
        if self.state.all_dead():
            logger.debug("(SESSION {s}) Triggering fight ending in room: {r}".format(s=self.state.session.session_id, r=self.id))
            self.output_builder.append(self.text["fight_ends"]["text"])
            self.state.room_trigger_map[self.id]["fight_ends"] = False

    def trigger(self) -> None:
        """Method to print any new text if conditions met"""
        if self.state.get_current_room_id() == self.id:
            for text_type in self.text:
                if self.state.room_trigger_map[self.id][text_type]:
                    # execute function
                    if text_type in self.text:
                        self.text[text_type]["trigger"]()
    
    def explore_trigger(self) -> None:
        """Method to print any new text if conditions met"""
        if self.state.get_current_room_id() == self.id:
            logger.debug("(SESSION {s}) Triggering explore_trigger in room: {r}".format(s=self.state.session.session_id, r=self.id))
            self.puzzles.explore_trigger()

    def get_connected_rooms(self) -> list:
        """Method to return the connected rooms"""
        return list(self.state.room_connect_map[self.id].keys())

    def has_item(self, item: str) -> bool:
        """Method to determine if query item is in the room's treasure"""
        return bool(item in self.state.room_treasure_map[self.id])

    def get_item(self, item: str) -> Item:
        """Method to return an item from the room's treasure"""
        # TODO return Item
        if self.has_item(item):
            # TODO factory method to make and return an Item object
            return self.state.room_treasure_map[self.id][item]

    def took_item(self, item: str) -> None:
        """Method to remove the item from the room"""
        self.state.room_treasure_map[self.id].remove(item)
        
    def can_attack_door(self, door: str) -> bool:
        """Method to return whether a door of room can be attacked"""
        return self.puzzles.can_attack_door(self.id, door)
    
    def get_door_armor_class(self, door: str) -> int:
        """Method to return the armor class of specified door"""
        return self.puzzles.get_door_armor_class(self.id, door)
        
    def get_door_hp(self, door: str) -> int:
        """Method to return the armor class of specified door"""
        return self.puzzles.get_door_hp(self.id, door)
    
    def get_all_text_array(self) -> str:
        """Method to return all text prepared in array"""
        all_text = []
        for text in self.text:
            prepared_text = self.text[text]["text"].lower().replace(".", "").replace(",", "").split(" ")
            all_text.extend(prepared_text)
        return all_text
    
    def get_description(self) -> str:
        """Method to get the room description, including any treasure and puzzles"""

        # if there's no visibility, return only the most basic description
        if (
            not self.visibility
            and not self.state.torch_lit
            and not self.state.get_player().character.has_darkvision()
        ):
            return self.text["no_visibility_description"]["text"]

        else:
            desc_str = self.text["description"]["text"]

            # add description of connect rooms
            if len(self.get_connected_rooms()) == 1:
                desc_str += " There is an exit to the {d} from here.".format(
                    d=Text.properly_format_list(
                        [
                            self.state.get_room_name(room)
                            for room in self.get_connected_rooms()
                        ],
                        delimiter=", the ",
                        last_delimiter=" or ",
                    )
                )
            else:
                desc_str += " There are exits to the {d} from here.".format(
                    d=Text.properly_format_list(
                        [
                            self.state.get_room_name(room)
                            for room in self.get_connected_rooms()
                        ],
                        delimiter=", the ",
                        last_delimiter=" or ",
                    )
                )

            # add descriptions of monsters
            desc_str += " " + self.state.get_formatted_monster_status_summary(self.id)

            # add description of treasure if there are no living monsters
            if not self.state.get_possible_monster_targets():
                if self.state.room_treasure_map[self.id]:
                    treasure = [
                        self.state.get_player().character.items.get_name(item)
                        for item in self.state.room_treasure_map[self.id]
                    ]
                    desc_str += " After searching the room thoroughly you find a {t}. You should pick {i} up.".format(
                        t=Text.properly_format_list(treasure),
                        i="it" if len(treasure) == 1 else "them"
                    )

            # TODO add description of puzzles

            return desc_str
