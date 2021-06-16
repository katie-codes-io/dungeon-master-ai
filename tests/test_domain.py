import unittest
import sys
import os

p = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, p + "/../")

from dmai.domain.actions import Actions
from dmai.game.game import Game
from dmai.game.state import State
from dmai.utils.exceptions import UnrecognisedRoomError


class TestActions(unittest.TestCase):
    """Test the Actions class"""
    def setUp(self) -> None:
        self.game = Game(char_class="fighter", char_name="Xena", adventure="the_tomb_of_baradin_stormfury")
        self.game.load()
        self.actions = self.game.dm.actions

    def test_move_good_destination(self) -> None:
        entity = "player"
        destination = "inns_cellar"
        State.quest()
        moved = self.actions.move(entity, destination)
        self.assertEqual(moved, True)

    def test_move_bad_destination(self) -> None:
        entity = "player"
        destination = "the_moon"
        moved = self.actions.move(entity, destination)
        self.assertEqual(moved, False)

    def test_attack_good_target(self) -> None:
        entity = "player"
        target = "giant_rat_1"
        State.quest()
        self.actions.move(entity, "inns_cellar")
        attacked = self.actions.attack(entity, target)
        self.assertEqual(attacked, True)
    
    def test_attack_bad_target(self) -> None:
        entity = "player"
        target = "goblin_1"
        State.quest()
        self.actions.move(entity, "inns_cellar")
        attacked = self.actions.attack(entity, target)
        self.assertEqual(attacked, False)
    
    def test_use_good_equipment(self) -> None:
        entity = "player"
        equipment = "torch"
        used = self.actions.use(equipment, entity)
        self.assertEqual(used, True)
    
    def test_use_bad_equipment(self) -> None:
        entity = "player"
        equipment = "computer"
        used = self.actions.use(equipment, entity)
        self.assertEqual(used, False)
    
    def test_equip_good_weapon(self) -> None:
        entity = "player"
        weapon = "javelin"
        self.actions.unequip()
        equipped = self.actions.equip(weapon, entity)
        self.assertEqual(equipped, True)
    
    def test_equip_bad_weapon(self) -> None:
        entity = "player"
        weapon = "rubber_duck"
        self.actions.unequip()
        equipped = self.actions.equip(weapon, entity)
        self.assertEqual(equipped, False)

    def test_unequip_all(self) -> None:
        unequipped = self.actions.unequip()
        self.assertEqual(unequipped, True)

    def test_unequip_good_weapon(self) -> None:
        entity = "player"
        weapon = "greataxe"
        unequipped = self.actions.unequip(weapon, entity)
        self.assertEqual(unequipped, True)

    def test_unequip_good_weapon(self) -> None:
        entity = "player"
        weapon1 = "rubber_duck"
        weapon2 = "quarterstaff"
        unequipped = self.actions.unequip(weapon1, entity)
        self.assertEqual(unequipped, False)
        unequipped = self.actions.unequip(weapon2, entity)
        self.assertEqual(unequipped, False)
    
    def test_converse_good_target(self) -> None:
        target = "corvus"
        can_converse = self.actions.converse(target)
        self.assertEqual(can_converse, True)

    def test_converse_bad_target(self) -> None:
        target1 = "yoda"
        target2 = "anvil"
        can_converse = self.actions.converse(target1)
        self.assertEqual(can_converse, False)
        can_converse = self.actions.converse(target2)
        self.assertEqual(can_converse, False)

    def test_investigate_good_target(self) -> None:
        target = "corvus"
        can_converse = self.actions.investigate(target)
        self.assertEqual(can_converse, True)

    def test_investigate_bad_target(self) -> None:
        target1 = "yoda"
        target2 = "anvil"
        can_converse = self.actions.investigate(target1)
        self.assertEqual(can_converse, False)
        can_converse = self.actions.investigate(target2)
        self.assertEqual(can_converse, False)


if __name__ == "__main__":
    unittest.main()
