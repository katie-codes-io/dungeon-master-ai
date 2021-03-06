from dmai.utils.loader import Loader
from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class Abilities:

    # class variables
    ability_data = dict()

    def __init__(self, abilities: dict) -> None:
        """Abilities class"""
        self.abilities = abilities
        self._load_ability_data()
        self.modifiers = self._calculate_ability_modifiers()

    def __repr__(self) -> str:
        return "Abilities:\n{a}\nModifiers:\n{m}".format(a=self.abilities,
                                                         m=self.modifiers)

    @classmethod
    def _load_ability_data(cls) -> None:
        """Set the cls.ability_data class variable data"""
        cls.ability_data = Loader.load_domain("abilities")

    @classmethod
    def get_all_abilities(cls) -> list:
        """Method to return a list of all abilities in tuple (id, name)"""
        abilities = cls.ability_data["abilities"]
        return [(ability, abilities[ability]["name"]) for ability in abilities]

    def _calculate_ability_modifiers(self) -> dict:
        """Calculate the ability modifiers"""
        modifiers = dict()
        for ability in self.abilities:
            for mod in self.ability_data["modifiers"]:
                mod_min = self.ability_data["modifiers"][mod]["min"]
                mod_max = self.ability_data["modifiers"][mod]["max"]
                if mod_min <= self.abilities[ability] <= mod_max:
                    modifiers[ability] = int(mod)
                    break
        return modifiers

    def get_score(self, ability: str) -> int:
        """Return the specified ability score"""
        return self.abilities[ability]

    def get_modifier(self, mod: str) -> int:
        """Return the specified ability modifier"""
        return self.modifiers[mod]

    @classmethod
    def get_name(cls, ability: str) -> str:
        """Return the full ability name"""
        return cls.ability_data["abilities"][ability]["name"]