from dmai.game.npcs.npc import NPC
from dmai.domain.abilities import Abilities
from dmai.domain.alignment import Alignment
from dmai.domain.armor import Armor
from dmai.domain.attacks import Attacks
from dmai.domain.conditions import Conditions
from dmai.domain.equipment import Equipment
from dmai.domain.features import Features
from dmai.domain.languages import Languages
from dmai.domain.skills import Skills
from dmai.domain.spells import Spells

class Monster(NPC):
    def __init__(self, monster_data: dict, npc_data: dict = None) -> None:
        """Monster abstract class"""
        if npc_data:
            NPC.__init__(self, npc_data)
            
        try:
            for key in monster_data:
                self.__setattr__(key, monster_data[key])

            # replace the attributes values with objects where appropriate
            self.abilities = Abilities(self.abilities)
            self.alignment = Alignment(self.alignment)
            self.armor = Armor(self.armor)
            self.attacks = Attacks(self.attacks)
            self.conditions = Conditions()
            self.equipment = Equipment(self.equipment)
            self.features = Features(features=self.features)
            self.languages = Languages(self.languages)
            self.skills = Skills(abilities=self.abilities, skills=self.skills)
            self.spells = Spells(self.spells)

        except AttributeError as e:
            print("Cannot create monster, incorrect attribute: {e}".format(e=e))
            raise
        
        # Initialise additional variables
        self.treasure = None

    def __repr__(self) -> str:
        return "Monster: {n}\nMax HP: {hp}".format(n=self.name, hp=self.hp_max)

    def set_treasure(self, treasure: str) -> None:
        """Method to set treasure."""
        self.treasure = treasure