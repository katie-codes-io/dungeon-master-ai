from dmai.utils.output_builder import OutputBuilder
from dmai.game.state import State
from dmai.utils.loader import Loader
from dmai.domain.characters.character import Character
from dmai.domain.characters.fighter import Fighter
from dmai.domain.characters.wizard import Wizard
from dmai.domain.characters.rogue import Rogue
from dmai.domain.characters.cleric import Cleric
from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class CharacterCollectionMeta(type):
    _instances = {}

    def __new__(cls, name, bases, dict):
        instance = super().__new__(cls, name, bases, dict)
        instance.character_data = {}
        return instance

    def __call__(cls, *args, **kwargs) -> None:
        """CharacterCollection static singleton metaclass"""
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class CharacterCollection(metaclass=CharacterCollectionMeta):
    def __init__(self) -> None:
        """CharacterCollection class"""
        pass

    @classmethod
    def __repr__(cls) -> str:
        character_list = cls.character_data.keys()
        character_str = "{c} is storing the following characters: {cl}".format(
            c=cls.__class__.__name__, cl=", ".join(character_list))
        return character_str

    @classmethod
    def load(cls) -> None:
        cls.character_data = Loader.load_domain("characters")

    @classmethod
    def get_all_names(cls) -> list:
        return [cls.character_data[c]["name"] for c in cls.character_data]

    @classmethod
    def get_character(cls, character: str, state: State, output_builder: OutputBuilder) -> Character:
        """Return a character of specified type"""
        character_obj = None
        try:
            character_obj = cls._character_factory(character, state, output_builder)
        except ValueError as e:
            logger.error("(SESSION {s}) {e}".format(s=state.session.session_id, e=e))
        return character_obj

    @classmethod
    def _character_factory(cls, character: str, state: State, output_builder: OutputBuilder) -> Character:
        """Construct a character of specified type"""
        character = character.lower()
        if character in cls.character_data.keys():
            character_map = {
                "cleric": Cleric,
                "fighter": Fighter,
                "rogue": Rogue,
                "wizard": Wizard,
            }
            character_obj = character_map[character]
        else:
            msg = "Cannot create character class {c} - it does not exist!".format(
                c=character)
            raise ValueError(msg)
        return character_obj(cls.character_data[character], state, output_builder)
