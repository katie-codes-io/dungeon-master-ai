import unittest
import sys
import os
import shutil

p = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, p + "/../")

from dmai.game.game import Game
from dmai.planning.fast_downward_adapter import FastDownwardAdapter
from dmai.utils.config import Config
from dmai.game.state import State
from dmai.nlg.nlg import NLG


class TestFastDownwardAdapter(unittest.TestCase):
    """Test the FastDownwardAdapter class"""
    def _prepare_adapter(self, domain: str,
                         problem: str) -> FastDownwardAdapter:
        shutil.copy(
            os.path.join(Config.directory.planning_test,
                         "{d}.pddl".format(d=domain)),
            os.path.join(Config.directory.planning,
                         "{u}.{d}.domain.pddl".format(d=domain,
                                                      u=Config.uuid)))
        shutil.copy(
            os.path.join(Config.directory.planning_test,
                         "{p}.pddl".format(p=problem)),
            os.path.join(
                Config.directory.planning,
                "{u}.{p}.problem.pddl".format(p=problem, u=Config.uuid)))
        return FastDownwardAdapter(domain, problem)

    def _cleanup(self, domain, problem) -> None:
            os.remove(
                os.path.join(
                    Config.directory.planning,
                    "{u}.{d}.domain.pddl".format(d=domain, u=Config.uuid)))
            os.remove(
                os.path.join(
                    Config.directory.planning,
                    "{u}.{p}.problem.pddl".format(p=problem, u=Config.uuid)))
            os.remove(
                os.path.join(
                    Config.directory.planning,
                    "{u}.{d}-{p}.plan".format(d=domain,
                                              p=problem,
                                              u=Config.uuid)))

    def test_build_plan_player(self) -> None:
        domain = "player_domain"
        problem = "player_problem_fighter"
        try:
            Config.set_uuid()
            adapter = self._prepare_adapter(domain, problem)
            p = adapter.build_plan()
        except Exception:
            self._cleanup(domain, problem)
        self.assertEqual(p, True)
        self._cleanup(domain, problem)

    def test_build_plan_monster(self) -> None:
        domain = "monster_domain"
        problem = "monster_problem_inns_cellar"
        try:
            Config.set_uuid()
            adapter = self._prepare_adapter(domain, problem)
            m = adapter.build_plan()
        except Exception:
            self._cleanup(domain, problem)
        self.assertEqual(m, True)
        self._cleanup(domain, problem)


class TestPlanningMonster(unittest.TestCase):
    """Test the PlanningMonster class"""
    def setUp(self) -> None:
        self.game = Game(
            char_class="fighter",
            char_name="Xena",
            adventure="the_tomb_of_baradin_stormfury",
        )
        self.game.load()
        NLG.set_game(self.game)
        Config.set_uuid()
        Config.agent.set_player("planning")
        Config.planner.set_player("fd")
        monster_id = "giant_rat_1"
        State.set_current_room("player", "inns_cellar")
        State.light_torch()
        State.set_target(monster_id)
        self.monster = State.get_entity(monster_id)
        self.monster.agent.prepare_next_move()
    
    def tearDown(self) -> None:
        shutil.rmtree(Config.directory.planning)
    
    def test_giant_rat_plan(self) -> None:
        self.assertEqual("(declare_attack_against_player giant_rat_1 player inns_cellar)\n", self.monster.agent.get_next_move())
    
    def test_build_domain(self) -> None:
        file_path = os.path.join(
            Config.directory.planning,
            "{u}.{d}.domain.pddl".format(u=Config.uuid, d=self.monster.agent.domain)
        )
        self.assertTrue(os.path.exists(file_path))
        
    def test_build_problem(self) -> None:
        file_path = os.path.join(
            Config.directory.planning,
            "{u}.{p}.problem.pddl".format(u=Config.uuid, p=self.monster.agent.problem)
        )
        self.assertTrue(os.path.exists(file_path))


class TestPlanningPlayer(unittest.TestCase):
    """Test the PlanningPlayer class"""
    def setUp(self) -> None:
        self.game = Game(
            char_class="fighter",
            char_name="Xena",
            adventure="the_tomb_of_baradin_stormfury",
        )
        self.game.load()
        NLG.set_game(self.game)
        Config.set_uuid()
        Config.agent.set_player("planning")
        Config.planner.set_player("fd")
        monster_id = "giant_rat_1"
        State.set_current_room("player", "inns_cellar")
        State.quest()
        State.light_torch()
        State.set_target(monster_id)
        self.player = State.get_player()
        self.player.agent.prepare_next_move()
    
    def tearDown(self) -> None:
        pass
        # shutil.rmtree(Config.directory.planning)
    
    def test_player_plan(self) -> None:
        self.assertEqual("(declare_attack_against_entity player giant_rat_1 inns_cellar)\n", self.player.agent.get_next_move())
    
    def test_build_domain(self) -> None:
        file_path = os.path.join(
            Config.directory.planning,
            "{u}.{d}.domain.pddl".format(u=Config.uuid, d=self.player.agent.domain)
        )
        self.assertTrue(os.path.exists(file_path))
        
    def test_build_problem(self) -> None:
        file_path = os.path.join(
            Config.directory.planning,
            "{u}.{p}.problem.pddl".format(u=Config.uuid, p=self.player.agent.problem)
        )
        self.assertTrue(os.path.exists(file_path))
        
        
if __name__ == "__main__":
    unittest.main()
