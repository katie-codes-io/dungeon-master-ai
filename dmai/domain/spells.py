from dmai.utils.loader import Loader


class Spells:

    # class variables
    spell_data = dict()

    def __init__(self, spells: dict) -> None:
        """Spells class"""
        self.spells = spells
        self._load_spell_data()

    def __repr__(self) -> str:
        return "Spells:\n{a}".format(a=self.spells)

    @classmethod
    def _load_spell_data(cls) -> None:
        """Set the cls.spell_data class variable data"""
        cls.spell_data = Loader.load_json("data/domain/spells.json")
