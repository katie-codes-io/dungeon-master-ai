from dmai.domain.abilities import Abilities
from dmai.utils.loader import Loader
from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class Skills:

    # class variables
    skill_data = dict()

    def __init__(
        self,
        abilities: Abilities,
        pro_bonus=None,
        proficiencies=None,
        skills: dict = None,
    ) -> None:
        """Skills class"""
        self._load_skill_data()
        self.skills = dict()

        # Initialise the skill values with the ability modifiers
        for skill in self.skill_data:
            ability = self.skill_data[skill]["ability"]
            self.skills[skill] = abilities.get_modifier(ability)

        # If a skill object has been passed, it means it's a monster.
        # This given skill value already takes the modifier into account
        # so replace the self.skills values, instead of adding
        if skills:
            for skill in skills:
                self.skills[skill] = skills[skill]

        # Add any specified proficiency bonuses to the skill modifiers
        if proficiencies and pro_bonus:
            for pro_type in proficiencies:
                for pro in proficiencies[pro_type]:
                    self.skills[pro] = self.skills[pro] + pro_bonus

    def __repr__(self) -> str:
        repr_str = "Skills:\n"
        for skill in self.skills:
            repr_str += "{skill}: {score}\n".format(
                skill=self.skill_data[skill]["name"], score=self.skills[skill])
        return repr_str

    @classmethod
    def _load_skill_data(cls) -> None:
        """Set the cls.skill_data class variable data"""
        cls.skill_data = Loader.load_domain("skills")

    @classmethod
    def get_all_skills(cls) -> list:
        """Method to return a list of all skills in tuple (id, name)"""
        skills = cls.skill_data
        return [(skill, skills[skill]["name"]) for skill in skills]

    def get_modifier(self, skill: str) -> int:
        """Return the specified skill modifier"""
        return self.skills[skill]

    @classmethod
    def get_name(cls, skill: str) -> str:
        """Return the full skill name"""
        return cls.skill_data[skill]["name"]