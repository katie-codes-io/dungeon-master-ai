import unittest
import sys
import os

p = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, p + "/../")

from dmai.domain.actions.attack import Attack
from dmai.game.game import Game
from dmai.nlg.nlg import NLG


class TestActions(unittest.TestCase):
    """Test the Actions class"""
    def setUp(self) -> None:
        self.game = Game(char_class="fighter", char_name="Xena", adventure="the_tomb_of_baradin_stormfury")
        self.game.load()
        self.actions = self.game.dm.actions

    def tearDown(self) -> None:
        self.game.state.extinguish_torch()
        
    def test_move_good_destination(self) -> None:
        entity = "player"
        destination = "inns_cellar"
        self.game.state.quest()
        moved = self.actions.move(entity, destination)
        self.assertEqual(moved, True)

    def test_move_bad_destination(self) -> None:
        entity = "player"
        destination = "the_moon"
        moved = self.actions.move(entity, destination)
        self.assertEqual(moved, False)

    def test_move_locked(self) -> None:
        self.game.output_builder.clear()
        entity = "player"
        self.game.state.set_current_room(entity, "western_corridor")
        moved  = self.actions.move(entity, "dungeon_entrance")
        self.assertEqual(moved, False)
        self.assertEqual("You cannot move to the Dungeon Entrance because the way is locked! You should figure out a way to get through or you could go to the Antechamber.\n", self.game.output_builder.format())
        
    def test__can_move_must_kill_monsters(self) -> None:
        entity = "player"
        destination = "stout_meal_inn"
        self.game.state.set_current_room(entity, "inns_cellar")
        self.game.state.light_torch()
        (moved, reason) = self.actions._can_move(entity, destination)
        self.assertEqual(moved, False)
        self.assertEqual(reason, "must kill")
    
    def test__can_move_same_destination(self) -> None:
        entity = "player"
        destination = "stout_meal_inn"
        self.game.state.set_current_room(entity, destination)
        (moved, reason) = self.actions._can_move(entity, destination)
        self.assertEqual(moved, False)
        self.assertEqual(reason, "same")

    def test__can_move_no_quest(self) -> None:
        entity = "player"
        destination = "inns_cellar"
        self.game.state.set_current_room(entity, "stout_meal_inn")
        self.game.state.questing = False
        (moved, reason) = self.actions._can_move(entity, destination)
        self.assertEqual(moved, False)
        self.assertEqual(reason, "no quest")
        
    def test__can_move_no_visibility(self) -> None:
        entity = "player"
        destination = "stout_meal_inn"
        self.game.state.set_current_room(entity, "inns_cellar")
        self.game.state.extinguish_torch()
        (moved, reason) = self.actions._can_move(entity, destination)
        self.assertEqual(moved, False)
        self.assertEqual(reason, "no visibility")
        
    def test__can_move_locked(self) -> None:
        entity = "player"
        destination = "dungeon_entrance"
        self.game.state.set_current_room(entity, "western_corridor")
        self.game.state.light_torch()
        self.game.state.quest()
        (moved, reason) = self.actions._can_move(entity, destination)
        self.assertEqual(moved, False)
        self.assertEqual(reason, "locked")
        
    def test__can_move_unrecognised_room(self) -> None:
        entity = "player"
        destination = "the moon"
        self.game.state.set_current_room(entity, "stout_meal_inn")
        self.game.state.quest()
        (moved, reason) = self.actions._can_move(entity, destination)
        self.assertEqual(moved, False)
        self.assertEqual(reason, "unknown destination")
    
    def test__can_move_unrecognised_entity(self) -> None:
        entity = "yoda"
        destination = "inns_cellar"
        (moved, reason) = self.actions._can_move(entity, destination)
        self.assertEqual(moved, False)
        self.assertEqual(reason, "unknown entity")

    def test__can_move_not_connected(self) -> None:
        entity = "player"
        destination = "antechamber"
        self.game.state.set_current_room(entity, "stout_meal_inn")
        self.game.state.quest()
        (moved, reason) = self.actions._can_move(entity, destination)
        self.assertEqual(moved, False)
        self.assertEqual(reason, "not connected")
        
    def test_attack_good_target(self) -> None:
        entity = "player"
        target = "giant_rat_1"
        self.game.state.quest()
        self.game.state.light_torch()
        self.actions.move(entity, "inns_cellar")
        attacked = self.actions.attack(entity, target)
        self.assertEqual(attacked, True)
    
    def test_attack_bad_target(self) -> None:
        entity = "player"
        target = "goblin_1"
        self.game.state.quest()
        self.actions.move(entity, "inns_cellar")
        attacked = self.actions.attack(entity, target)
        self.assertEqual(attacked, False)

    def test_use_good_equipment(self) -> None:
        entity = "player"
        equipment = "torch"
        used = self.actions.use(equipment=equipment, entity=entity)
        self.assertEqual(used, True)
    
    def test_use_bad_equipment(self) -> None:
        entity = "player"
        equipment = "computer"
        used = self.actions.use(equipment=equipment, entity=entity)
        self.assertEqual(used, False)
    
    def test_equip_good_weapon(self) -> None:
        entity = "player"
        weapon = "greataxe"
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


class TestAttack(unittest.TestCase):
    """Test the Attack class"""
    def setUp(self) -> None:
        self.game = Game(char_class="fighter", char_name="Xena", adventure="the_tomb_of_baradin_stormfury")
        self.game.load()
    
    def test__can_attack_unknown_target(self) -> None:
        entity = "player"
        target = "yoda"
        self.game.state.set_current_room(entity, "inns_cellar")
        attack = Attack(entity, target, "monster", self.game.state, self.game.output_builder)
        (attacked, reason) = attack._can_attack()
        self.assertEqual(attacked, False)
        self.assertEqual(reason, "unknown target")
    
    def test__can_attack_different_location(self) -> None:
        entity = "player"
        target = "zombie_1"
        self.game.state.set_current_room(entity, "inns_cellar")
        self.game.state.extinguish_torch()
        attack = Attack(entity, target, "monster", self.game.state, self.game.output_builder)
        (attacked, reason) = attack._can_attack()
        self.assertEqual(attacked, False)
        self.assertEqual(reason, "different location")
        
    def test__can_attack_no_visibility(self) -> None:
        entity = "player"
        target = "giant_rat_1"
        self.game.state.set_current_room(entity, "inns_cellar")
        self.game.state.extinguish_torch()
        attack = Attack(entity, target, "monster", self.game.state, self.game.output_builder)
        (attacked, reason) = attack._can_attack()
        self.assertEqual(attacked, False)
        self.assertEqual(reason, "no visibility")


if __name__ == "__main__":
    unittest.main()
