from dmai.utils.loader import Loader
from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class Armor:

    # class variables
    armor_data = dict()

    def __init__(self, armor: str, proficiencies=None) -> None:
        """Armor class"""
        self.armor = armor
        self.body = None
        self.shield = None
        self.proficiencies = proficiencies
        self._load_armor_data()

        # assign armor to slots on body
        for armor_id in self.armor:
            self.equip_armor(armor_id, self.armor_data[armor_id]["slot"])

    def __repr__(self) -> str:
        return "Armor:\n{a}".format(a=self.armor)

    @classmethod
    def _load_armor_data(cls) -> None:
        """Set the cls.armor_data class variable data"""
        cls.armor_data = Loader.load_domain("armor")

    def get_armor(self, armor_id: str) -> bool:
        """Method to return specified armor"""
        if armor_id in self.armor_data:
            return self.armor_data[armor_id]

    def equip_armor(self, armor_id: str, slot: str) -> None:
        """Method to equip specified armor to specified slot"""
        if armor_id in self.armor_data:
            self.__setattr__(slot, armor_id)

    def unequip_armor(self, armor_id: str) -> None:
        """Method to unequip specified armor"""
        if self.body == armor_id:
            self.body = None
        elif self.shield == armor_id:
            self.shield = None

    def get_equipped(self, slot) -> dict:
        """Method to get equipped armor.
        Returns a dictionary"""
        if slot == "body" and self.body:
            return self.armor_data[self.body]
        if slot == "shield" and self.shield:
            return self.armor_data[self.shield]

    def is_equipped(self, armor_id: str) -> bool:
        """Method to determine if armor is equipped.
        Returns bool"""
        body_armor = self.get_equipped("body")
        shield_armor = self.get_equipped("shield")

        if body_armor and armor_id == body_armor["id"]:
            return True
        if shield_armor and armor_id == shield_armor["id"]:
            return True
        return False

    def calculate_armor_class(self, dex: int) -> int:
        """Method to calculate the armor class given a dexterity modifier"""
        ac = 10
        if not self.body and not self.shield:
            return ac + dex

        if self.body:
            body = self.get_equipped("body")
            ac = body["ac"]["base"]
            if body["ac"]["mod"] == "dex":
                ac += max(dex, body["ac"]["mod_max"])
                ac += body["ac"]["bonus"]

        if self.shield:
            shield = self.get_equipped("shield")
            ac += shield["ac"]["bonus"]

        return ac

    def get_all(self) -> list:
        """Return a list with all the equipment ids"""
        return self.armor.keys()

    def get_proficient(self) -> str:
        """Return the proficient armor in a list"""
        all_profs = []
        for prof in self.proficiencies:
            if prof in self.armor_data:
                all_profs.append(self.armor_data[prof])
            else:
                # proficiency could be type
                for armor in self.armor_data.values():
                    if armor["type"] == prof:
                        all_profs.append(armor)
        return all_profs
    
    def get_formatted(self, armor_id) -> str:
        """Return the formatted armor"""
        if armor_id in self.armor_data:
            armor = self.armor_data[armor_id]
            if self.is_equipped(armor_id):
               return "{a} (equipped)".format(a=armor["name"])
            else:
                return "{q}".format(a=armor["name"])