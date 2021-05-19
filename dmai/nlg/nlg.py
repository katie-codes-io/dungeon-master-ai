from dmai.domain.characters.character_collection import CharacterCollection
import random


class NLGMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs) -> None:
        """NLG static singleton metaclass"""
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class NLG(metaclass=NLGMeta):

    # class variable
    game = None

    def __init__(self) -> None:
        """NLG static class"""
        pass

    @classmethod
    def set_game(cls, game) -> None:
        cls.game = game

    @classmethod
    def get_char_class(cls) -> str:
        """Return utterance for character selection"""
        c = "\n".join(CharacterCollection.get_all_names())
        utters = [
            "Which character class would you like to play?\n{c}".format(c=c),
            "Select a character class you like the sound of:\n{c}".format(c=c),
            "Select a character class from the following choices:\n{c}".format(c=c),
        ]
        return random.choice(utters)

    @classmethod
    def get_player_name(cls) -> str:
        """Return the utterance for getting player's name"""
        c = cls.game.player.character_class
        utters = [
            "What is your character's name, this great {c}?".format(c=c),
            "Ahh, a {c}. Excellent choice! And what is your character's name?".format(
                c=c
            ),
            "A {c}, marvelous! And what do they call your character?".format(c=c),
        ]
        return random.choice(utters)

    @classmethod
    def get_action(cls) -> str:
        """Return the utterance for getting a player action"""
        n = cls.game.player.name
        utters = ["{n}, what do you do?".format(n=n)]
        return random.choice(utters)

    @classmethod
    def get_title(cls) -> str:
        """Return the utterance for introducing the adventure title"""
        t = cls.game.dm.adventure.title
        utters = [
            "Welcome adventurer, today we're going to play {t}! Let me set the scene...".format(
                t=t
            ),
            "Today we'll play {t}, an exciting tale of adventure! Let me set the scene...".format(
                t=t
            ),
            "The title of the adventure we're about to play is: {t}. Let me set the scene...".format(
                t=t
            ),
        ]
        return random.choice(utters)

    @classmethod
    def acknowledge_name(cls) -> str:
        """Return the utterance for acknowledging player's name"""
        n = cls.game.player.name
        utters = [
            "{n}, simply majestic!".format(n=n),
            "{n}, the finest name in all the lands!".format(n=n),
            "{n}, that's a good one!".format(n=n),
        ]
        return random.choice(utters)
    
    @classmethod
    def enter_room(cls, room: str, adventure = None) -> str:
        """Return the utterance for entering a room previously visited"""
        if not adventure:
            return "You entered {r}".format(r=room)
        else:
            return adventure.get_room(room).enter()

    @classmethod
    def cannot_move(cls, room: str, reason: str = None) -> str:
        """Return the utterance for not allowing movement"""
        if not reason:
            return "You cannot move to {room}".format(room=room)
        elif reason == "same":
            return "You cannot move to {room} because you're already there!".format(
                room=room
            )
        elif reason == "locked":
            return "You cannot move to {room} because the way is locked!".format(
                room=room
            )

    @classmethod
    def no_target(cls) -> str:
        """Return the utterance for no target"""
        utters = [
            "Can you confirm your target",
            "Who, or what, do you want to attack?",
            "I'm not sure what you want to attack, can you repeat your target",
        ]
        return random.choice(utters)
        
    @classmethod
    def transition_to_combat(cls) -> str:
        """Return the utterance for transitioning to combat"""
        utters = [
            "Okay, let's fight!",
            "You're now starting combat",
            "Let's begin the combat round",
            "Moving into combat"
        ]
        return random.choice(utters)
    
    @classmethod
    def attack_npc_end_game(cls, npc_id: str) -> str:
        """Return the utterance for ending the game by attacking npc"""
        n = cls.game.dm.npcs.get_npc(npc_id).short_name
        utters = [
            "You attacked and fatally wounded {n}. He was a much loved member of the community and retribution was swift. You were captured within the day and currently languish in a miserable cell in the Greyforge city jail, awaiting trial.".format(n=n),
            "Your unprovoked attack took your good friend {n} completely unawares. As the light left his eyes, he managed to utter a quiet \"why?\" with his dying breath. Why indeed? You were captured within the day and currently languish in a miserable cell in the Greyforge city jail, awaiting trial.".format(n=n),
            "Not known for reasonable, measured behaviour you irrationally lashed out at {n}. The elderly dwarf had no time to defend himself, but let out a shout as he succumbed to his injury. Overheard by the city guard, you were promptly captured and currently languish in a miserable cell in the Greyforge city jail, awaiting trial.".format(n=n),
        ]
        return random.choice(utters)
        
    @classmethod
    def explain_armor_class(cls) -> str:
        """Return the utterance for explaining a armos class"""
        return "The minimum roll for successful damage. It is calculated as [x] because of [x, y, z]."

    @classmethod
    def explain_critical(cls) -> str:
        """Return the utterance for explaining a critical hit"""
        return "Critical means the damage dice are doubled. Roll for damage, double that, and add your modifier after that."