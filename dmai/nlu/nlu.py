import traceback

from dmai.utils.exceptions import UnrecognisedCommandError
from dmai.utils.output_builder import OutputBuilder
from dmai.utils.text import Text
from dmai.nlu.rasa_adapter import RasaAdapter
from dmai.game.state import State
from dmai.game.state import Combat
from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class NLU():

    # class variables
    INTENT_CONFIDENCE = 0.5

    def __init__(self, state: State, output_builder: OutputBuilder) -> None:
        self.state = state
        self.output_builder = output_builder
        self.param = ""
        self.commands = {
            "help": {
                "text": "/help",
                "help": "Show these commands",
                "cmd": "self.output_builder.append(self.show_commands(), wrap=False)"
            },
            "exit": {
                "text": "/exit",
                "help": "Exit the game",
                "cmd": "self.state.gameover()"
            },
            "stats": {
                "text":
                "/stats",
                "help":
                "Show your character stats in a character sheet",
                "cmd":
                "self.output_builder.append(self.game.player.get_character_sheet(), wrap=False)"
            }
        }

    def show_commands(self) -> str:
        """Return the command list"""
        cmd_str = "Commands:\n"
        for cmd in self.commands:
            cmd_str += "{c:<20}".format(c=self.commands[cmd]["text"])
            cmd_str += "{h}\n".format(h=self.commands[cmd]["help"])
        return cmd_str

    def process_player_command(self, player_cmd: str) -> tuple:
        """Method to process the player command.
        Returns a tuple with (bool, string) where bool indicates if DM output
        should be paused and string is the updated player utterance."""

        # first check if the user is issuing a command
        if player_cmd[0] == "/" or player_cmd[0] == "\\":
            try:
                return self._regex_and_exec(player_cmd)
            except UnrecognisedCommandError as e:
                logger.error("(SESSION {s}) {e}".format(s=self.state.session.session_id, e=e))
        return (False, player_cmd)

    def _regex_and_exec(self, player_cmd: str) -> None:
        """Process the player command as a regular expression"""
        cmd_tokens = player_cmd.split()
        cmd = cmd_tokens[0][1:]

        try:
            # setting param here in the local namespace for exec
            if len(cmd_tokens) == 2:
                self.param = cmd_tokens[1]
            elif len(cmd_tokens) > 2:
                self.param = " ".join(cmd_tokens[2:])
            elif "default_param" in self.commands[cmd]:
                self.param = self.commands[cmd]["default_param"]

            command = self.commands[cmd]["cmd"]
        except KeyError:
            msg = "Command not recognised: {c}\nUse /help to get list of available commands".format(
                c=player_cmd)
            raise UnrecognisedCommandError(msg)

        try:
            exec(command)
        except Exception as e:
            traceback.print_exc()
            return (False, "")

        if "return" in self.commands[cmd]:
            return_vals = []
            for val in self.commands[cmd]["return"]:
                # check if string refers to class variable
                if type(val) == str and val in self.__dict__:
                    return_vals.append(self.__dict__[val])
                else:
                    return_vals.append(val)
            return tuple(return_vals)
        else:
            return (True, "")

    def process_player_utterance(self, player_utter: str) -> tuple:
        """Method to process the player utterance"""
        return self._determine_intent(player_utter)

    def _determine_intent(self, player_utter: str) -> tuple:
        """Method to determine the player intent"""
        player_utter = player_utter.lower()
        (intent, confidence, entities) = RasaAdapter.get_intent(player_utter)
        logger.debug("(SESSION {s}) Detected player intent: {i} ({c})".format(s=self.state.session.session_id, i=intent, c=confidence))
        if confidence < self.INTENT_CONFIDENCE:
            intent = "no_intent"
        self.state.set_intent(intent)
        if intent:
            print("intent: " + intent)
        if entities:
            print(entities)

        logger.debug("(SESSION {s}) Expected entities: {i}".format(s=self.state.session.session_id, i=str(self.state.expected_entities)))
        logger.debug("(SESSION {s}) Expected intent: {i}".format(s=self.state.session.session_id, i=str(self.state.expected_intent)))
        logger.debug("(SESSION {s}) Stored intent: {i}".format(s=self.state.session.session_id, i=str(self.state.stored_intent)))
        logger.debug("(SESSION {s}) Suggested next move: {i}".format(s=self.state.session.session_id, i=str(self.state.suggested_next_move["utter"])))

        # check if there's expected entities
        if self.state.expected_entities:
            hits = [entity for entity in entities if entity["entity"] in self.state.expected_entities]
            if hits:
                # if we have a hit for expected entities, use the primary expected intent
                if self.state.expected_intent:
                    intent = self.state.expected_intent[0]
                elif self.state.stored_intent:
                    intent = self.state.stored_intent["intent"]
            self.state.clear_expected_entities()
                
        # check if there's an expected intent
        elif self.state.expected_intent:
            if intent != "affirm" and "roll" not in self.state.expected_intent:
                if intent not in self.state.expected_intent:
                    # TODO make exception for hints or questions
                    # TODO this also seems a little broken when input is not recognised and player corrects themselves to roll initiative
                    intents = [self.state.get_dm().player_intent_map[intent]["desc"] for intent in self.state.expected_intent]
                    intent_str = Text.properly_format_list(intents, last_delimiter=" or ")
                    self.output_builder.append("I was expecting you to {i}.".format(i=intent_str))
                    logger.debug("(SESSION {s}) Intent being processed: None".format(s=self.state.session.session_id))
                    return (None, {"nlu_entities": entities})
        
        # check if there's a suggested next move
        elif self.state.suggested_next_move["state"]:
            if intent != "affirm":
                self.state.clear_suggested_next_move()

        # check if in combat before allowing any player utterance
        if self.state.in_combat:
            if self.state.get_combat_status() == Combat.ATTACK_ROLL:
                logger.debug("(SESSION {s}) Intent being processed: attack".format(s=self.state.session.session_id))
                return ("attack", {"nlu_entities": entities})
            else:
                logger.debug("(SESSION {s}) Intent being processed: roll".format(s=self.state.session.session_id))
                return ("roll", {"nlu_entities": entities})
        
        logger.debug("(SESSION {s}) Intent being processed: {i}".format(s=self.state.session.session_id, i=str(intent)))

        if intent == "no_intent":
            return ("no_intent", {})
        if intent == "move":
            return ("move", {"nlu_entities": entities})
        if intent == "attack" or intent == "ranged_attack":
            return ("attack", {"nlu_entities": entities})
        if intent == "use":
            return ("use", {"nlu_entities": entities})
        if intent == "stop_using":
            return ("stop_using", {"nlu_entities": entities})
        if intent == "hint":
            return ("hint", {"nlu_entities": entities})
        if intent == "equip":
            return ("equip", {"nlu_entities": entities})
        if intent == "unequip":
            return ("unequip", {"nlu_entities": entities})
        if intent == "converse":
            return ("converse", {"nlu_entities": entities})
        if intent == "greet":
            return ("converse", {"nlu_entities": entities})
        if intent == "question_npc":
            return ("converse", {"nlu_entities": entities})
        if intent == "affirm":
            return ("affirm", {})
        if intent == "deny":
            return ("deny", {})
        if intent == "explore":
            return ("explore", {"nlu_entities": entities})
        if intent == "roll":
            return ("roll", {"nlu_entities": entities})
        if intent == "pick_up":
            return ("pick_up", {"nlu_entities": entities})
        if intent == "health":
            return ("health", {})
        if intent == "inventory":
            return ("inventory", {"nlu_entities": entities})
        if intent == "force":
            return ("force", {"nlu_entities": entities})
        if intent == "ability_check":
            return ("ability_check", {"nlu_entities": entities})
        if intent == "skill_check":
            return ("skill_check", {"nlu_entities": entities})
        if intent == "ale":
            return ("ale", {"nlu_entities": entities})
        if intent == "roleplay":
            return ("roleplay", {"nlu_entities": entities})
        if intent == "negotiate":
            return ("negotiate", {"nlu_entities": entities})
        if intent == "rescue":
            return ("rescue", {"nlu_entities": entities})
        if intent == "bot_challenge":
            return ("bot_challenge", {})
        if intent == "stealth":
            return ("stealth", {"nlu_entities": entities})
        if intent == "pick_lock":
            return ("pick_lock", {"nlu_entities": entities})
        else:
            # check for stored intent in self.state
            if self.state.stored_intent:
                # combine the stored entities with new entities
                if "nlu_entities" in self.state.stored_intent["params"]:
                    entities.extend(
                        self.state.stored_intent["params"]["nlu_entities"])
                return (self.state.stored_intent["intent"], {
                    "nlu_entities": entities
                })

        return (None, {})
