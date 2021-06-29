from dmai.game.world.puzzles.puzzle import Puzzle


class PuzzleCollection:
    def __init__(self, puzzles_dict: dict) -> None:
        """PuzzleCollection class"""
        self.puzzles = {}

        # prepare the puzzles
        for puzzle_id in puzzles_dict:
            puzzle = Puzzle(puzzles_dict[puzzle_id])
            self.puzzles[puzzle_id] = puzzle

    def __repr__(self) -> str:
        return "Puzzle collection:\n{a}".format(a=self.puzzles)

    def get_all_puzzles(self) -> list:
        """Method to return a list of all puzzles"""
        return list(self.puzzles.values())
    
    def can_attack_door(self, room: str, door: str) -> bool:
        """Method to return whether a door of room can be attacked"""
        door_id = "{i}---{d}".format(i=room, d=door)
        return bool(door_id in self.puzzles)
    
    def get_door_armor_class(self, room: str, door: str) -> int:
        """Method to return the armor class of specified door"""
        if self.can_attack_door(room, door):
            door_id = "{i}---{d}".format(i=room, d=door)
            return self.puzzles[door_id].get_armor_class()

    def get_door_hp(self, room: str, door: str) -> int:
        """Method to return the armor class of specified door"""
        if self.can_attack_door(room, door):
            door_id = "{i}---{d}".format(i=room, d=door)
            return self.puzzles[door_id].get_hp()