from dmai.utils.output_builder import OutputBuilder
from dmai.utils.exceptions import UnrecognisedEntityError
from dmai.game.state import State
from dmai.nlg.nlg import NLG
from dmai.domain.actions.action import Action
from dmai.utils.logger import get_logger

logger = get_logger(__name__)



class PickUp(Action):
    def __init__(self, item: str, entity: str, state: State, output_builder: OutputBuilder) -> None:
        """PickUp class"""
        Action.__init__(self)
        self.item = item
        self.entity = entity
        self.state = state
        self.output_builder = output_builder

    def __repr__(self) -> str:
        return "{c}".format(c=self.__class__.__name__)

    def execute(self, **kwargs) -> bool:
        return self._pick_up()

    def _can_pick_up(self) -> tuple:
        """Check if an item can be picked up by an entity.
        Returns tuple (bool, str) to indicate whether pick up is possible
        and reason why not if not."""

        # check if entity and item are within pick up range
        try:
            current = self.state.get_current_room(self.entity)
            if not current.has_item(self.item):
                return (False, "not in room")

            # can't pick up if can't see
            if not current.visibility:
                if self.entity == "player":
                    if (
                        not self.state.torch_lit
                        and not self.state.get_player().character.has_darkvision()
                    ):
                        return (False, "no visibility")

            # none of the above situations were triggered so allow pick up
            return (True, "")
        except UnrecognisedEntityError:
            return (False, "unknown entity")

    def _pick_up(self) -> bool:
        """Attempt to pick up a specified item.
        Returns a bool to indicate whether the action was successful"""

        # check if pick up can happen
        (picked_up, reason) = self._can_pick_up()
        if picked_up:
            picked_up = self.state.get_player().character.items.add_item(self.item)
            if picked_up:
                self.state.get_current_room(self.entity).took_item(self.item)
                self.output_builder.append(
                    NLG.pick_up(self.state.get_player().character.items.get_name(self.item))
                )
            return picked_up
        else:
            self.output_builder.append(
                NLG.cannot_pick_up(
                    self.state.get_player().character.items.get_name(self.item), reason
                )
            )
            return picked_up
