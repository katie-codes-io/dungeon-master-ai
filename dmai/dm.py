import dmai
from dmai.game.state import State
from dmai.game.adventure import Adventure
from dmai.domain.actions import Actions
from dmai.nlg.nlg import NLG
from dmai.game.npcs.npc_collection import NPCCollection
from dmai.utils.output_builder import OutputBuilder
from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class DM:

    # class variables
    ENTITY_CONFIDENCE = 0.75

    def __init__(self, adventure: str) -> None:
        """Main DM class"""
        self._dm_utter = None
        self._player_utter = None
        self.triggers = []
        self.adventure = Adventure(adventure)

    def load(self) -> None:
        # Initialise the NPC Collection with the adventure data
        self.npcs = NPCCollection(self.adventure)
        self.npcs.load()

        # Initialise the actions with the adventure and npc data
        self.actions = Actions(self.adventure, self.npcs)

        # Initialise the player intent map
        self.player_intent_map = {
            "hint": self.hint,
            "move": self.move,
            "attack": self.attack,
            "use": self.use,
            "stop_using": self.stop_using
        }

    def input(
        self,
        player_utter: str,
        utter_type: str = None,
        intent: str = None,
        kwargs: dict = {},
    ) -> bool:
        """Receive a player input.
        Returns whether the utterance was successful."""
        succeed = False
        self._player_utter = player_utter
        if utter_type:
            if utter_type == "start":
                State.start()
            elif utter_type == "name":
                OutputBuilder.append(NLG.acknowledge_name())
            else:
                OutputBuilder.append(NLG.get_action())
            succeed = True

        elif intent:
            # look up intent in map
            try:
                succeed = self.player_intent_map[intent](**kwargs)
            except KeyError:
                logger.error("Intent not in map: {i}".format(i=intent))
                raise

        # execute any triggers
        if succeed:
            self.execute_triggers()

        # prepare next AI moves
        State.get_player().prepare_next_move()
        # TODO monster next moves

        # last thing to do: maintain state
        State.maintenance()

        return succeed

    @property
    def output(self) -> str:
        """Return an output for the player"""
        if OutputBuilder.has_response():
            return OutputBuilder.format()
        else:
            return NLG.get_action()

    def register_trigger(self, trigger: object) -> None:
        """Register a trigger object"""
        if trigger not in self.triggers:
            logger.debug("Registering trigger: {n}".format(n=str(trigger)))
            self.triggers.append(trigger)

    def deregister_trigger(self, trigger: object) -> None:
        """Deregister a trigger object"""
        if trigger in self.triggers:
            logger.debug("Deregistering trigger: {n}".format(n=str(trigger)))
            self.triggers.remove(trigger)

    def execute_triggers(self) -> None:
        """Method to execute triggers"""
        for obj in self.triggers:
            obj.trigger()

    def get_intro_text(self) -> str:
        return self.adventure.intro_text

    def hint(self) -> None:
        """Use the player AI to get the next possible move.
        Appends the hint to output with the OutputBuilder.
        """
        State.get_player().print_next_move()

    def _get_destination(self, nlu_entities: dict) -> str:
        """Extract a destination from NLU entities dictionary.
        Returns a string with destination"""
        for entity in nlu_entities:
            if entity["entity"] == "location" and entity[
                    "confidence"] >= self.ENTITY_CONFIDENCE:
                return entity["value"]

    def _get_target(self, nlu_entities: dict) -> str:
        """Extract a target from NLU entities dictionary.
        Returns a string with destination"""
        monster = None
        i = None
        npc = None
        for entity in nlu_entities:
            if entity["entity"] == "monster" and entity[
                    "confidence"] >= self.ENTITY_CONFIDENCE:
                monster = entity["value"]
            if entity["entity"] == "id" and entity[
                    "confidence"] >= self.ENTITY_CONFIDENCE:
                i = entity["value"]
            if entity["entity"] == "npc" and entity[
                    "confidence"] >= self.ENTITY_CONFIDENCE:
                npc = entity["value"]

        # monsters are indexed by a unique id, determine it if possible
        if monster:
            if i:
                # player appeared to specify particular individual, get it's id
                monster_id = "{m}_{i}".format(m=monster, i=i)
            else:
                # player hasn't appeared to specify particular individual, pick first alive one
                # TODO get player confirmation about which monster to target
                monster_id = self.npcs.get_monster_id(
                    monster,
                    status="alive",
                    location=State.get_current_room_id())
            return monster_id

        # NPCs have unique ids
        if npc:
            return npc

    def _get_equipment(self, nlu_entities: dict) -> str:
        """Extract a equipment from NLU entities dictionary.
        Returns a string with equipment"""
        for entity in nlu_entities:
            if entity["entity"] == "equipment" and entity[
                    "confidence"] >= self.ENTITY_CONFIDENCE:
                return entity["value"]

    def move(self,
             destination: str = None,
             entity: str = None,
             nlu_entities: dict = None) -> bool:
        """Attempt to move an entity to a destination determined by NLU or specified.
        Returns whether the move was successful."""
        if not entity:
            entity = "player"
        if not destination and nlu_entities:
            destination = self._get_destination(nlu_entities)

        if not destination:
            moved = False
            OutputBuilder.append(NLG.no_destination())
        else:
            logger.info("Moving {e} to {d}!".format(e=entity, d=destination))
            moved = self.actions.move(entity, destination)
        return moved

    def attack(self,
               target: str = None,
               attacker: str = None,
               nlu_entities: dict = None) -> bool:
        """Attempt an attack by attacker against target determined by NLU or specified.
        Returns whether the attack was successful."""
        if not attacker:
            attacker = "player"
        if not target and nlu_entities:
            target = self._get_target(nlu_entities)

        if not target:
            attacked = False
            OutputBuilder.append(NLG.no_target())
        else:
            logger.info("{a} is attacking {t}!".format(a=attacker, t=target))
            attacked = self.actions.attack(attacker, target)
        return attacked

    def use(self,
            equipment: str = None,
            entity: str = None,
            nlu_entities: dict = None,
            stop: bool = False) -> bool:
        """Attempt to use an equipment.
        Returns whether the use was successful."""
        if not entity:
            entity = "player"
        if not equipment and nlu_entities:
            equipment = self._get_equipment(nlu_entities)

        if not equipment:
            used = False
            OutputBuilder.append(NLG.no_equipment(stop=stop))
        else:
            logger.info("{e} is using {q}!".format(e=entity, q=equipment))
            used = self.actions.use(equipment, entity, stop)
        return used

    def stop_using(self,
                   equipment: str = None,
                   entity: str = None,
                   nlu_entities: dict = None) -> bool:
        """Attempt to stop using an equipment.
        Returns whether the stoppage was successful."""
        return self.use(equipment=equipment,
                        entity=entity,
                        nlu_entities=nlu_entities,
                        stop=True)
