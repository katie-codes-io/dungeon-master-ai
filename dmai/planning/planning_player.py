from abc import ABC, abstractmethod
from dmai.utils.output_builder import OutputBuilder
import os

from dmai.planning.planning_agent import PlanningAgent
from dmai.domain.abilities import Abilities
from dmai.domain.monsters.monster_collection import MonsterCollection
from dmai.domain.skills import Skills
from dmai.utils.config import Config
from dmai.game.state import State
from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class PlanningPlayer(PlanningAgent):
    def __init__(self, state: State, output_builder: OutputBuilder, **kwargs) -> None:
        """PlanningPlayer class"""
        PlanningAgent.__init__(self, Config.planner.player, "player", state, output_builder, **kwargs)

    def __repr__(self) -> str:
        return "{c}".format(c=self.__class__.__name__)

    def build_domain(self) -> None:
        logger.debug("(SESSION {s}) Building domain: player".format(s=self.state.session.session_id))
        domain_file = os.path.join(
            Config.directory.planning,
            "{u}.{d}.domain.pddl".format(u=self.state.session.session_id, d=self.domain),
        )

        # TODO implement intent solution
        # TODO implement item solution
        # TODO implement solve intent

        with open(domain_file, "w") as writer:
            ################################################
            # Construct the domain file header and requirements
            writer.write(self._construct_domain_header(self.domain))
            writer.write(self._construct_requirements())

            ################################################
            # Construct the domain file types
            types = []

            # Append types
            types.append(
                {
                    "type": "object",
                    "subtypes": [
                        "entity",
                        "intent",
                        "puzzle",
                        "attitude",
                        "ability",
                        "room",
                        "door",
                        "weapon",
                        "equipment",
                        "item",
                    ],
                }
            )
            types.append({"type": "entity", "subtypes": ["player", "npc", "monster"]})
            types.append(
                {"type": "monster", "subtypes": MonsterCollection.get_all_monsters()}
            )
            types.append(
                {"type": "attitude", "subtypes": ["indifferent", "friendly", "hostile"]}
            )
            types.append({"type": "ability", "subtypes": ["skill"]})
            types.append({"type": "weapon", "subtypes": ["ranged_weapon"]})
            writer.write(self._construct_types(types))

            ################################################
            # Construct the domain file predicates
            predicates = []

            # Adventure
            predicates.append({"predicate": "quest", "params": []})
            predicates.append({"predicate": "complete", "params": []})
            predicates.append({"predicate": "gives_quest", "params": [("npc", "npc")]})
            predicates.append({"predicate": "treasure", "params": [("object", "object")]})
            predicates.append(
                {"predicate": "advantage", "params": [("object", "object")]}
            )
            predicates.append(
                {"predicate": "disadvantage", "params": [("object", "object")]}
            )
            for ability in Abilities.get_all_abilities():
                predicates.append(
                    {
                        "predicate": ability[1].lower(),
                        "params": [("ability", "ability")],
                    }
                )
            for skill in Skills.get_all_skills():
                predicates.append(
                    {"predicate": skill[0], "params": [("skill", "skill")]}
                )
            predicates.append(
                {
                    "predicate": "has",
                    "params": [("entity", "entity"), ("object", "object")],
                }
            )
            predicates.append(
                {"predicate": "at", "params": [("object", "object"), ("room", "room")]}
            )
            predicates.append({"predicate": "alive", "params": [("object", "object")]})
            predicates.append({"predicate": "injured", "params": [("player", "player")]})
            predicates.append(
                {"predicate": "damaged", "params": [("object", "object")]}
            )
            predicates.append(
                {
                    "predicate": "equipped",
                    "params": [("player", "player"), ("object", "object")],
                }
            )
            predicates.append(
                {
                    "predicate": "connected",
                    "params": [
                        ("door", "door"),
                        ("location", "room"),
                        ("destination", "room"),
                    ],
                }
            )
            predicates.append({"predicate": "locked", "params": [("door", "door")]})
            predicates.append(
                {"predicate": "higher_than_ac", "params": [("target", "object")]}
            )
            predicates.append(
                {
                    "predicate": "can_attack_roll",
                    "params": [("player", "player"), ("target", "object")],
                }
            )
            predicates.append(
                {
                    "predicate": "can_damage_roll",
                    "params": [("player", "player"), ("target", "object")],
                }
            )
            predicates.append(
                {
                    "predicate": "can_ability_check",
                    "params": [
                        ("player", "player"),
                        ("ability", "ability"),
                        ("target", "object"),
                    ],
                }
            )
            predicates.append(
                {
                    "predicate": "can_equipment_check",
                    "params": [
                        ("player", "player"),
                        ("equipment", "equipment"),
                        ("target", "object"),
                    ],
                }
            )
            predicates.append(
                {
                    "predicate": "ability_check_success",
                    "params": [
                        ("player", "player"),
                        ("ability", "ability"),
                        ("target", "object"),
                    ],
                }
            )
            predicates.append(
                {
                    "predicate": "equipment_check_success",
                    "params": [
                        ("player", "player"),
                        ("equipment", "equipment"),
                        ("target", "object"),
                    ],
                }
            )
            predicates.append(
                {
                    "predicate": "attack_roll_success",
                    "params": [("player", "player"), ("target", "object")],
                }
            )
            for equipment in self.state.get_player().get_all_equipment_ids():
                predicates.append(
                    {"predicate": equipment, "params": [("equipment", "equipment")]}
                )
            for item in self.state.get_player().character.items.item_data.keys():
                predicates.append(
                    {"predicate": item, "params": [("item", "item")]}
                )
            predicates.append({"predicate": "action", "params": []})
            predicates.append({"predicate": "torch_lit", "params": []})
            predicates.append({"predicate": "darkvision", "params": []})
            predicates.append({"predicate": "dark", "params": [("room", "room")]})
            predicates.append(
                {
                    "predicate": "attitude_towards_player",
                    "params": [("npc", "npc"), ("attitude", "attitude")],
                }
            )
            predicates.append(
                {
                    "predicate": "improve_attitude",
                    "params": [("current", "attitude"), ("next", "attitude")],
                }
            )
            predicates.append(
                {
                    "predicate": "degrade_attitude",
                    "params": [("current", "attitude"), ("next", "attitude")],
                }
            )
            predicates.append({"predicate": "combat", "params": []})
            predicates.append(
                {"predicate": "must_kill", "params": [("monster", "monster")]}
            )
            predicates.append(
                {
                    "predicate": "explore_solution",
                    "params": [("target", "object")],
                }
            )
            predicates.append(
                {
                    "predicate": "ability_solution",
                    "params": [("target", "object"), ("ability", "ability")],
                }
            )
            predicates.append(
                {
                    "predicate": "equipment_solution",
                    "params": [("target", "object"), ("equipment", "equipment")],
                }
            )
            predicates.append(
                {
                    "predicate": "intent_solution",
                    "params": [("target", "object"), ("intent", "intent")],
                }
            )
            predicates.append(
                {
                    "predicate": "item_solution",
                    "params": [("target", "object"), ("item", "item")],
                }
            )
                
            writer.write(self._construct_predicates(predicates))

            ################################################
            # Construct the domain file actions
            actions = [
                "ability_check",
                "ability_check_with_advantage",
                "ability_check_with_disadvantage",
                "equipment_check",
                "equipment_check_with_advantage",
                "equipment_check_with_disadvantage",
                "attack_roll",
                "attack_roll_with_advantage",
                "attack_roll_with_disadvantage",
                "damage_roll",
                "equip",
                "unequip",
                "explore",
                "investigate_puzzle",
                "investigate_monster",
                "use_potion_of_healing",
                "move",
                "open_door_with_item",
                "open_door_with_explore",
                "open_door_with_ability",
                "open_door_with_equipment",
                "open_door_with_attack",
                "force_door",
                "use_door_switch",
                "attack_door",
                "breaks_down_door",
                "receive_quest",
                "roleplay_positively",
                "roleplay_negatively",
                "declare_attack_against_entity",
                "kill_monster",
            ]
            if self.state.get_player().has_equipment("thieves_tools")[0]:
                actions.append("use_thieves_tools")
            if self.state.get_player().has_equipment("torch")[0]:
                actions.append("light_torch")
                actions.append("extinguish_torch")
            
            writer.write(self._construct_actions(actions))
            writer.write(self._construct_domain_footer())

    def build_problem(self) -> None:
        logger.debug("(SESSION {s}) Building problem: {p}".format(s=self.state.session.session_id, p=self.problem))
        problem_file = os.path.join(
            Config.directory.planning,
            "{u}.{p}.problem.pddl".format(u=self.state.session.session_id, p=self.problem),
        )

        with open(problem_file, "w") as writer:
            ################################################
            # Construct the problem file header
            writer.write(self._construct_problem_header(self.problem, "player"))

            ################################################
            # Construct the problem file objects
            objects = []

            # Player
            objects.append(["player", "player"])
            for intent in self.state.get_dm().player_intent_map.keys():
                objects.append(["{i}_intent".format(i=intent), "intent"])
            for item in self.state.get_player().character.items.item_data.keys():
                objects.append([item, "item"])

            # NPCs
            for npc in self.state.get_dm().npcs.get_all_npcs():
                objects.append([npc.id, "npc"])
            objects.append(["indifferent", "indifferent"])
            objects.append(["friendly", "friendly"])
            objects.append(["hostile", "hostile"])

            # Rooms
            for room in self.state.get_dm().adventure.get_all_rooms():
                objects.append([room.id, "room"])

            # Doors
            doors = []
            for room in self.state.get_dm().adventure.get_all_rooms():
                for connection in room.get_connected_rooms():
                    door = "{r}---{c}".format(r=room.id, c=connection)
                    reverse_door = "{c}---{r}".format(r=room.id, c=connection)
                    if not reverse_door in doors:
                        doors.append(door)
            for door in doors:
                objects.append([door, "door"])

            # Monsters
            for monster in self.state.get_dm().npcs.get_all_monsters():
                objects.append([monster.unique_id, monster.id])

            # Abilities
            for ability in Abilities.get_all_abilities():
                objects.append([ability[0], "ability"])

            # Skills
            for skill in Skills.get_all_skills():
                objects.append([skill[0], "skill"])

            # Weapons
            for weapon in self.state.get_player().get_all_weapon_ids():
                objects.append([weapon, "weapon"])

            # Equipment
            for equipment in self.state.get_player().get_all_equipment_ids():
                objects.append([equipment, "equipment"])

            # Puzzles
            for room in self.state.get_dm().adventure.get_all_rooms():
                for puzzle in room.puzzles.get_all_puzzles():
                    if not puzzle.type == "door":
                        if not self.state.get_player().character.items.has_item(puzzle.id)[0]:
                            objects.append(["{p}_puzzle".format(p=puzzle.id), "puzzle"])

            # Construct the string
            writer.write(self._construct_objects(objects))

            ################################################
            # Construct the problem file init
            init = []

            # Adventure
            if self.state.questing:
                init.append(["quest"])

            # Player
            init.append(["at", "player", self.state.get_current_room().id])
            if self.state.is_alive():
                init.append(["alive", "player"])
            if self.state.get_current_hp() <= (0.75*self.state.get_player().hp_max):
                init.append(["injured", "player"])
            if self.state.torch_lit:
                init.append(["torch_lit"])
            if self.state.get_player().character.has_darkvision():
                init.append(["darkvision"])
            for ability in Abilities.get_all_abilities():
                init.append([ability[1].lower(), ability[0]])
            for skill in Skills.get_all_skills():
                init.append([skill[0], skill[0]])
            for weapon in self.state.get_player().get_all_weapon_ids():
                init.append(["has", "player", weapon])
                if self.state.get_player().is_equipped(weapon):
                    init.append(["equipped", "player", weapon])
            for equipment in self.state.get_player().get_all_equipment_ids():
                init.append([equipment, equipment])
                init.append(["has", "player", equipment])
            
            # NPCs
            for npc in self.state.get_dm().npcs.get_all_npcs():
                init.append(["at", npc.id, self.state.get_current_room(npc.id).id])
                if self.state.is_alive(npc.id):
                    init.append(["alive", npc.id])
                if npc.gives_quest:
                    init.append(["gives_quest", npc.id])
            init.append(["improve_attitude", "indifferent", "friendly"])
            init.append(["improve_attitude", "hostile", "indifferent"])
            init.append(["degrade_attitude", "friendly", "indifferent"])
            init.append(["degrade_attitude", "indifferent", "hostile"])
            for npc in self.state.get_dm().npcs.get_all_npcs():
                init.append(
                    [
                        "attitude_towards_player",
                        npc.id,
                        self.state.get_current_attitude(npc.id).value,
                    ]
                )

            # Monsters
            for monster in self.state.get_dm().npcs.get_all_monsters():
                init.append(
                    [
                        "at",
                        monster.unique_id,
                        self.state.get_current_room(monster.unique_id).id,
                    ]
                )
                if self.state.is_alive(monster.unique_id):
                    init.append(["alive", monster.unique_id])
                if self.state.monster_treasure_map[monster.unique_id]:
                    if not self.state.is_hidden(monster.unique_id):
                        init.append(["treasure", monster.unique_id])

            # Combat
            for npc in self.state.get_dm().npcs.get_all_npcs():
                if npc.must_kill:
                    init.append(["must_kill", npc.id])
            for monster in self.state.get_dm().npcs.get_all_monsters():
                if monster.must_kill:
                    init.append(["must_kill", monster.unique_id])

            # Rooms
            for room in self.state.get_dm().adventure.get_all_rooms():
                if not room.visibility:
                    init.append(["dark", room.id])
                if bool(self.state.room_treasure_map[room.id]):
                    init.append(["treasure", room.id])
                    
            # Room connections
            for door in doors:
                room1 = door.split("---")[0]
                room2 = door.split("---")[1]
                init.append(["connected", door, room1, room2])
                init.append(["connected", door, room2, room1])
                init.append(["at", door, room1])
                init.append(["at", door, room2])
                if not self.state.travel_allowed(room1, room2):
                    init.append(["locked", door])
                if not self.state.connection_broken(room1, room2):
                    init.append(["alive", door])

            # Items
            for item in self.state.get_player().character.items.item_data.keys():
                init.append([item, item])
                # if item is used for a puzzle solution, also put the location in init
                for room in self.state.get_dm().adventure.get_all_rooms():
                    for puzzle in room.puzzles.get_all_puzzles():
                        if puzzle.id not in self.state.solved_puzzles:
                            if puzzle.type == "item" and puzzle.id == item:
                                init.append(["at", puzzle.id, room.id])
            # check if NPC has item
            for npc in self.state.npc_treasure_map:
                if self.state.npc_treasure_map[npc]:
                    for item in self.state.npc_treasure_map[npc]:
                        init.append(["has", npc, item])

            for item in self.state.get_player().get_all_item_ids():
                init.append(["has", "player", item])

            # Puzzles
            for room in self.state.get_dm().adventure.get_all_rooms():
                for puzzle in room.puzzles.get_all_puzzles():
                    puzzle_id = puzzle.id if puzzle.type == "door" else "{p}_puzzle".format(p=puzzle.id)
                    if puzzle.type != "door":
                        init.append(["at", puzzle_id, room.id])
                    if puzzle.id not in self.state.solved_puzzles:
                        puzzle_solution = False
                        if not puzzle_solution:
                            # Item solution
                            for solution in puzzle.get_all_solutions():
                                if "item" in puzzle.get_solution(solution):
                                    item = puzzle.get_solution(solution)["item"]
                                    if self.state.get_player().has_item(item)[0]:
                                        init.append(["item_solution", puzzle_id, item])
                                        puzzle_solution = True
                                        break
                        if not puzzle_solution:
                            # Skill solution
                            for skill in Skills.get_all_skills():
                                if puzzle.check_solution_skill(skill[0]):
                                    init.append(["skill_solution", puzzle_id, skill[0]])
                                    puzzle_solution = True
                                    break
                        if not puzzle_solution:
                            # Explore solution
                            for explore in self.state.puzzle_trigger_map[puzzle.id]["explore"]:
                                if self.state.puzzle_trigger_map[puzzle.id]["explore"][explore]:
                                    if puzzle.check_solution_explore():
                                        init.append(["explore_solution", puzzle_id])
                                        puzzle_solution = True
                                        break
                        if not puzzle_solution:
                            # Ability solution
                            for ability in Abilities.get_all_abilities():
                                if puzzle.check_solution_ability(ability[0]):
                                    init.append(["ability_solution", puzzle_id, ability[0]])
                                    puzzle_solution = True
                                    break
                        if not puzzle_solution:
                            # Intent solution
                            for intent in self.state.get_dm().player_intent_map.keys():
                                if puzzle.check_solution_intent(intent):
                                    init.append(["intent_solution", puzzle_id, intent])
                                    puzzle_solution = True
                                    break
                        if not puzzle_solution:
                            # Equipment solution
                            for equipment in self.state.get_player().get_all_equipment_ids():
                                if puzzle.check_solution_equipment(equipment):
                                    init.append(["equipment_solution", puzzle_id, equipment])
                                    puzzle_solution = True
                                    break

                    # TODO add spell solution

            # Construct the string
            writer.write(self._construct_init(init))

            ################################################
            # Construct the problem file goal
            goal = self.state.current_goal
            writer.write(self._construct_goal(goal))
            writer.write(self._construct_problem_footer())
