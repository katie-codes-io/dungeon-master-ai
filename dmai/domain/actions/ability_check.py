from dmai.domain.abilities import Abilities
from dmai.utils.output_builder import OutputBuilder
from dmai.utils.exceptions import UnrecognisedEntityError
from dmai.game.state import State
from dmai.nlg.nlg import NLG
from dmai.domain.actions.action import Action
import dmai


class AbilityCheck(Action):
    def __init__(self, ability: str, entity: str, target: str) -> None:
        """AbilityCheck class"""
        Action.__init__(self)
        self.ability = ability
        self.entity = entity
        self.target = target

    def __repr__(self) -> str:
        return "{c}".format(c=self.__class__.__name__)

    def execute(self, **kwargs) -> bool:
        return self._ability_check()

    def _can_ability_check(self) -> tuple:
        """Check entity can perform ability check.
        Returns tuple (bool, str) to indicate whether ability check is possible
        and reason why not if not."""

        # check if entity and target are within pick up range
        try:
            current = State.get_current_room(self.entity)
            if State.get_entity(self.target):
                # TODO support non-room ability checks
                # if not current == State.get_current_room(self.target):
                #     return (False, "different location")
                return (False, "not required")
            elif not self.target in current.get_connected_rooms():
                return (False, "different location")

            # can't ability check if can't see
            if not current.visibility:
                if self.entity == "player":
                    if (
                        not State.torch_lit
                        or State.get_player().character.has_darkvision()
                    ):
                        return (False, "no visibility")

            # now check if an ability check is required for this situation
            for puzzle in current.puzzles.get_all_puzzles():
                # TODO support non-door puzzles
                if puzzle.id == "{c}---{t}".format(c=current.id, t=self.target):
                    if puzzle.check_solution_ability(self.ability):
                        return (True, "")
            
            # none of the above situations were triggered so by default don't allow ability check
            return (False, "not required")
        except UnrecognisedEntityError:
            return (False, "unknown entity")

    def _ability_check(self) -> bool:
        """Attempt to perform ability check.
        Returns a bool to indicate whether the action was successful"""

        # check if ability check can happen
        (can_check, reason) = self._can_ability_check()
        if can_check:
            if can_check:
                OutputBuilder.append(
                    NLG.ability_check(Abilities.get_name(self.ability))
                )
                State.set_expected_intents(["roll"])
            return can_check
        else:
            target_name = State.get_entity_name(self.target)
            if not bool(target_name):
                target_name = State.get_room_name(self.target)
            OutputBuilder.append(NLG.cannot_ability_check(Abilities.get_name(self.ability), target_name, reason))
            return can_check
