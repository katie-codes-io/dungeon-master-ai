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
    def get_char_class(cls, characters: str) -> str:
        """Return utterance for character selection"""
        utters = [
            "Which character class would you like to play?\n{c}".format(
                c=characters),
            "Select a character class you like the sound of:\n{c}".format(
                c=characters),
            "Select a character class from the following choices:\n{c}".format(
                c=characters),
        ]
        return random.choice(utters)

    @classmethod
    def get_player_name(cls) -> str:
        """Return the utterance for getting player's name"""
        c = cls.game.player.character_class
        utters = [
            "What is your character's name, this great {c}?".format(c=c),
            "Ahh, a {c}. Excellent choice! And what is your character's name?".
            format(c=c),
            "A {c}, marvelous! And what do they call your character?".format(
                c=c),
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
            "Welcome adventurer, today we're going to play {t}! Let me set the scene..."
            .format(t=t),
            "Today we'll play {t}, an exciting tale of adventure! Let me set the scene..."
            .format(t=t),
            "The title of the adventure we're about to play is: {t}. Let me set the scene..."
            .format(t=t),
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
    def enter_room(cls, room: str, adventure=None) -> str:
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
                room=room)
        elif reason == "locked":
            return "You cannot move to {room} because the way is locked!".format(
                room=room)
        elif reason == "no visibility":
            return "You cannot move to {room} because it's too dark for you to find the way!".format(
                room=room)
        elif reason == "no quest":
            return "You cannot move to {room} because you haven't accepted the quest!".format(
                room=room)
        elif reason == "unknown":
            return "You cannot move to unknown location: {room}!".format(
                room=room)

    @classmethod
    def cannot_use(cls, equipment: str, reason: str = None) -> str:
        """Return the utterance for not allowing use of equipment"""
        if not reason:
            return "You cannot use {e}".format(e=equipment)
        elif reason == "unknown":
            return "You cannot use unknown equipment: {e}!".format(e=equipment)
        elif reason == "not equipped":
            return "You cannot use {e} because it's not equipped!".format(
                e=equipment)
        elif reason == "quantity":
            return "You cannot use {e} because you've run out!".format(
                e=equipment)

    @classmethod
    def no_destination(cls) -> str:
        """Return the utterance for no destination"""
        utters = [
            "Can you confirm your destination",
            "Sorry, where do you want to go?",
            "I'm not sure where you want to go, can you repeat your destination",
        ]
        return random.choice(utters)

    @classmethod
    def no_target(cls, verb: str) -> str:
        """Return the utterance for no target"""
        utters = [
            "Can you confirm your target",
            "Who, or what, do you want to {v}?".format(v=verb),
            "I'm not sure who or what you want to {v}, can you repeat your target".format(v=verb),
        ]
        return random.choice(utters)

    @classmethod
    def no_equipment(cls, stop: bool = False) -> str:
        """Return the utterance for no equipment"""
        if stop:
            utters = [
                "Can you confirm the equipment you want to stop using",
                "Sorry, what do you want to stop using?",
                "I'm not sure where you want to stop using, can you repeat the equipment",
            ]
        else:
            utters = [
                "Can you confirm the equipment you want to use",
                "Sorry, what do you want to use?",
                "I'm not sure where you want to use, can you repeat the equipment",
            ]
        return random.choice(utters)

    @classmethod
    def no_weapon(cls, unequip: bool = False) -> str:
        """Return the utterance for no weapon"""
        if unequip:
            utters = [
                "Can you confirm the weapon you want to unequip",
                "Sorry, what do you want to unequip?",
                "I'm not sure where you want to unequip, can you repeat the weapon",
            ]
        else:
            utters = [
                "Can you confirm the weapon you want to equip",
                "Sorry, what do you want to equip?",
                "I'm not sure where you want to equip, can you repeat the weapon",
            ]
        return random.choice(utters)

    @classmethod
    def cannot_equip(cls, weapon: str, reason: str = None) -> str:
        """Return the utterance for not allowing equipping of weapon"""
        if not reason:
            return "You cannot equip {w}".format(w=weapon)
        elif reason == "unknown":
            return "You cannot equip unknown equipment: {w}!".format(w=weapon)
        elif reason == "not owned":
            return "You cannot equip {w} because it's not in your inventory!".format(
                w=weapon)
        elif reason == "no free slots":
            return "You cannot equip {w} because you don't have any free slots! Unequip something first.".format(
                w=weapon)
        elif reason == "already equipped":
            return "You cannot equip {w} because it's already equipped!".format(
                w=weapon)

    @classmethod
    def cannot_unequip(cls, weapon: str, reason: str = None) -> str:
        """Return the utterance for not allowing unequipping of weapon"""
        if not reason:
            return "You cannot unequip {w}".format(w=weapon)
        elif reason == "unknown":
            return "You cannot unequip unknown equipment: {w}!".format(w=weapon)
        elif reason == "not owned":
            return "You cannot unequip {w} because it's not in your inventory!".format(
                w=weapon)
        elif reason == "not equipped":
            return "You cannot unequip {w} because it's not equipped!".format(
                w=weapon)
        elif reason == "nothing equipped":
            return "You cannot unequip because nothing is equipped!"

    @classmethod
    def equip_weapon(cls, weapon: str) -> str:
        """Return the utterance for equipping a weapon"""
        utters = [
            "You equipped {w}".format(w=weapon)
        ]
        return random.choice(utters)

    @classmethod
    def unequip_weapon(cls, weapon: str) -> str:
        """Return the utterance for unequipping a weapon"""
        if not weapon:
            return "You unequipped all weapons"
        utters = [
            "You unequipped {w}".format(w=weapon)
        ]
        return random.choice(utters)

    @classmethod
    def light_torch(cls) -> str:
        """Return the utterance for lighting a torch"""
        utters = [
            "You light a torch and the space around you is now lighter",
            "The space around you illuminates in the glow of your lit torch",
            "Light now cascades from the point of your torch around you"
        ]
        return random.choice(utters)

    @classmethod
    def extinguish_torch(cls) -> str:
        """Return the utterance for extinguishing a torch"""
        utters = [
            "You extinguish your torch and the space around you is now darker",
            "The space around you returns to its normal light level",
            "Light ceases to cascade from your torch"
        ]
        return random.choice(utters)

    @classmethod
    def transition_to_combat(cls) -> str:
        """Return the utterance for transitioning to combat"""
        utters = [
            "Okay, let's fight!", "You're now starting combat",
            "Let's begin the combat round", "Moving into combat"
        ]
        return random.choice(utters)

    @classmethod
    def roleplay(cls, target: str) -> str:
        """Return the utterance for getting roleplay prompt"""
        n = cls.game.player.name
        utters = [
            "{n}, what do you say to {t}?".format(n=n, t=target)
        ]
        return random.choice(utters)

    @classmethod
    def attack_of_opportunity(cls,
                              attacker: str = None,
                              target: str = None) -> str:
        """Return the utterance for an attack of opportunity"""
        if target and attacker:
            utters = [
                "{a} took an attack of opportunity against {t}!".format(
                    a=attacker, t=target),
                "{t} opened themselves up to an an attack of opportunity from {a}!"
                .format(a=attacker, t=target)
            ]
            return random.choice(utters)
        elif attacker:
            utters = [
                "{a} took an attack of opportunity against you!".format(
                    a=attacker),
                "You opened yourself up to an an attack of opportunity from {a}!"
                .format(a=attacker)
            ]
            return random.choice(utters)
        elif target:
            utters = [
                "You took an attack of opportunity against {t}!".format(
                    t=target),
                "{t} opened themselves up to an an attack of opportunity from you!"
                .format(t=target)
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

    ############################################################
    # Exploration and investigation utterances
    @classmethod
    def cannot_investigate(cls, target: str, reason: str = None) -> str:
        """Return the utterance for not allowing investigate of target"""
        if not reason:
            return "You cannot investigate {t}".format(t=target)
        elif reason == "unknown entity":
            return "You cannot investigate unknown target: {t}!".format(t=target)
        elif reason == "different location":
            return "You cannot investigate target {t}, you're not in the same location!".format(t=target)

    ############################################################
    # Gameover utterances
    @classmethod
    def attack_npc_end_game(cls, npc_id: str) -> str:
        """Return the utterance for ending the game by attacking npc"""
        n = cls.game.dm.npcs.get_npc(npc_id).short_name
        utters = [
            "You attacked and fatally wounded {n}. He was a much loved member of the community and retribution was swift. You were captured within the day and currently languish in a miserable cell in the Greyforge city jail, awaiting trial."
            .format(n=n),
            "Your unprovoked attack took your good friend {n} completely unawares. As the light left his eyes, he managed to utter a quiet \"why?\" with his dying breath. Why indeed? You were captured within the day and currently languish in a miserable cell in the Greyforge city jail, awaiting trial."
            .format(n=n),
            "Not known for reasonable, measured behaviour you irrationally lashed out at {n}. The elderly dwarf had no time to defend himself, but let out a shout as he succumbed to his injury. Overheard by the city guard, you were promptly captured and currently languish in a miserable cell in the Greyforge city jail, awaiting trial."
            .format(n=n),
        ]
        return random.choice(utters)
    