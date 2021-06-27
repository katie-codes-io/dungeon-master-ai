from dmai.game.world.puzzles.puzzle_collection import PuzzleCollection
from dmai.game.world.puzzles.puzzle_collection import PuzzleCollection
from dmai.utils.output_builder import OutputBuilder
from dmai.nlg.nlg import NLG
from dmai.utils.text import Text
from dmai.game.state import State
from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class Room:
    def __init__(self, room_data: dict) -> None:
        """Main class for a room"""
        try:
            for key in room_data:
                self.__setattr__(key, room_data[key])

            # replace the attributes values with objects where appropriate
            self.puzzles = PuzzleCollection(self.puzzles)

        except AttributeError as e:
            logger.error(
                "Cannot create room, incorrect attribute: {e}".format(e=e))
            raise

        trigger_map = {
            "enter": self.enter,
            "exit": self.exit,
            "visibility": self.trigger_visibility,
            "fight_ends": self.trigger_fight_ends
        }

        # populate the self.text object
        for text_type in self.text:
            text = self.text[text_type]
            trigger = trigger_map[
                text_type] if text_type in trigger_map else None
            self.text[text_type] = {
                "text": text,
                "can_trigger": text_type in trigger_map,
                "trigger": trigger
            }

    def __repr__(self) -> str:
        return "Room: {a}".format(a=self.name)

    def enter(self) -> None:
        """Method when entering a room"""
        logger.debug("Triggering enter in room: {r}".format(r=self.id))
        if not State.stationary:
            if not self.visited:
                self.visited = True
                OutputBuilder.append(self.text["enter"]["text"])
            else:
                OutputBuilder.append(NLG.enter_room(self.name))
            State.halt()
    
    def exit(self) -> None:
        """Method when exiting a room"""
        logger.debug("Triggering exit in room: {r}".format(r=self.id))
        # TODO implement inns cellar to storage room exit text

    def trigger_visibility(self) -> str:
        """Method when triggering visibility text"""
        logger.debug("Triggering visibility in room: {r}".format(r=self.id))
        if not self.visibility:
            if State.torch_lit or State.get_player().character.has_darkvision(
            ):
                OutputBuilder.append(self.text["visibility"]["text"])
                self.text["visibility"]["can_trigger"] = False
    
    def trigger_fight_ends(self) -> str:
        """Method when triggering fight ends text"""
        logger.debug("Triggering fight ending in room: {r}".format(r=self.id))
        if not State.get_possible_monster_targets():
            OutputBuilder.append(self.text["fight_ends"]["text"])
            self.text["fight_ends"]["can_trigger"] = False
            
    def trigger(self) -> None:
        """Method to print any new text if conditions met"""
        for text_type in self.text:
            if self.text[text_type]["can_trigger"]:
                # execute function
                if text_type in self.text:
                    self.text[text_type]["trigger"]()

    def get_connected_rooms(self) -> list:
        """Method to return the connected rooms"""
        return list(self.connections.keys())
    
    def has_item(self, item: str) -> bool:
        """Method to determine if query item is in the room's treasure"""
        return bool(item in self.treasure)
    
    def get_item(self, item: str) -> None:
        """Method to return an item from the room's treasure"""
        # TODO return Item
        if self.has_item(item):
            # TODO factory method to make and return an Item object
            return self.treasure[item]

    def get_description(self) -> str:
        """Method to get the room description, including any treasure and puzzles"""
        
        # if there's no visibility, return only the most basic description
        if not self.visibility and not State.torch_lit and not State.get_player().character.has_darkvision():
            return self.text["no_visibility_description"]["text"]
        
        else:
            desc_str = self.text["description"]["text"]
            
            # add description of connect rooms
            desc_str += " There are exits to the {d} from here.".format(d=Text.properly_format_list([State.get_room_name(room) for room in self.get_connected_rooms()], delimiter=", the ", last_delimiter=" or "))
            
            # add descriptions of monsters
            desc_str += " " + State.get_formatted_monster_status_summary(self.id)
            
            # add description of treasure if there are no living monsters
            if not State.get_possible_monster_targets():
                # TODO replace with properly formatted names
                if self.treasure:
                    desc_str += " After searching the barrels and boxes thoroughly you find a {t}.".format(t=Text.properly_format_list(self.treasure))
            
            # TODO add description of puzzles
            
            return desc_str