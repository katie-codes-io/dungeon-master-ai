import random

from dmai.utils.text import Text


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

    ############################################################
    # Player interaction utterances
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
    def roll_reaction(cls, result: int) -> str:
        """Return utterance for reacting to a dice roll"""
        if result < 1:
            utters = [
                "Ouch!",
                "That is painful",
                "How unfortunate",
                "Oof"
            ]
        elif result > 19:
            utters = [
                "Nice!",
                "Truly magnificent",
                "Natural 20, way to go!",
                "That's how you do it!",
            ]
        else:
            utters = ["Well, it's a number!"]
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

    ############################################################
    # Action utterances
    @classmethod
    def health_update(cls, current_hp, hp_max: int = None):
        """Return the utterance updating player about their current hp"""
        if not hp_max:
            m = ""
        else:
            m = " out of a maximum of {h}".format(h=hp_max)
        utters = [
            "You've got {h} hp left{m}.".format(h=current_hp, m=m)
        ]
        return random.choice(utters)
        
    ############################################################
    # Action utterances
    @classmethod
    def enter_room(cls, room: str, adventure=None) -> str:
        """Return the utterance for entering a room previously visited"""
        if not adventure:
            return "You entered {r}".format(r=room)
        else:
            return adventure.get_room(room).enter()

    
    @classmethod
    def cannot_move(cls, room: str, reason: str = None, possible_destinations: str = []) -> str:
        """Return the utterance for not allowing movement"""
        if possible_destinations:
            p = "You could go to the {p}.".format(p=Text.properly_format_list(possible_destinations, delimiter=", the ", last_delimiter=" or the "))
        else:
            p = ""
        if not reason:
            return "You cannot move to {room}. {p}".format(room=room, p=p)
        elif reason == "same":
            return "You cannot move to {room} because you're already there! {p}".format(
                room=room, p=p)
        elif reason == "locked":
            return "You cannot move to {room} because the way is locked! {p}".format(
                room=room, p=p)
        elif reason == "not connected":
            return "You cannot move to {room} because it's not connected to this room. {p}".format(
                room=room, p=p)
        elif reason == "no visibility":
            return "You cannot move to {room} because it's too dark for you to find the way!".format(
                room=room, p=p)
        elif reason == "no quest":
            return "You cannot move to {room} because you haven't accepted the quest!".format(
                room=room, p=p)
        elif reason == "must kill":
            return "You cannot move to {room} because there are monsters in here you must deal with!".format(
                room=room)
        elif reason == "unknown destination":
            return "You cannot move to unknown room: {room}! {p}".format(
                room=room, p=p)
        else:
            return "You cannot move to {room}, although, I'm not sure why not... {p}".format(
                room=room, p=p)

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
    def no_destination(cls, possible_destinations: list = []) -> str:
        """Return the utterance for no destination"""
        utters = [
            "Can you confirm your destination.",
            "Sorry, where do you want to go?",
            "I'm not sure where you want to go, can you repeat your destination.",
        ]
        
        if possible_destinations:
            p = "You could go to the {p}.".format(p=Text.properly_format_list(possible_destinations, delimiter=", the ", last_delimiter=" or the "))
        else:
            p = ""
        
        return "{u} {p}".format(u=random.choice(utters), p=p)

    @classmethod
    def no_target(cls, verb: str, possible_targets: str = "") -> str:
        """Return the utterance for no target"""
        utters = [
            "Can you confirm your target. {p}".format(p=possible_targets),
            "Who, or what, do you want to {v}? {p}".format(v=verb, p=possible_targets),
            "I'm not sure who or what you want to {v}. {p}".format(v=verb, p=possible_targets),
        ]
        return random.choice(utters)

    @classmethod
    def no_monster_targets(cls) -> str:
        """Return the utterance for no mosnter targets"""
        utters = [
            "There are no monsters in here for you to attack!",
            "You don't have any targets in here",
            "Nope, there are no monsters here"
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

    ############################################################
    # Combat utterances
    @classmethod
    def transition_to_combat(cls) -> str:
        """Return the utterance for transitioning to combat"""
        utters = [
            "Okay let's fight, roll for initiative!", "You're now starting combat, roll for initiative!",
            "Let's begin the combat round, roll for initiative!", "Moving into combat, roll for initiative!"
        ]
        return random.choice(utters)

    @classmethod
    def entity_turn(cls, entity: str) -> str:
        """Return the utterance for telling the player whose turn it is"""
        entity = "your" if entity == "player" else "{e}'s".format(e=entity)
        utters = [
            "Okay, it's {e} turn...".format(e=entity)
        ]
        return random.choice(utters)
    
    @classmethod
    def declare_attack(cls) -> str:
        """Return the utterance for getting player to declare an attack"""
        utters = [
            "Your turn, who do you want to attack?"
        ]
        return random.choice(utters)
    
    @classmethod
    def perform_attack_roll(cls) -> str:
        """Return the utterance for getting player to perform attack roll"""
        utters = [
            "Make your attack roll"
        ]
        return random.choice(utters)

    @classmethod
    def perform_damage_roll(cls) -> str:
        """Return the utterance for getting player to perform damage roll"""
        utters = [
            "Make your damage roll"
        ]
        return random.choice(utters)
    
    @classmethod
    def attack(cls, attacker: str, target: str, *args) -> str:
        """Return the utterance for attacking"""
        # TODO different utterances for different weapons?
        attacker = "You" if attacker == "player" else attacker
        utters = [
            "{a} attacked {t}!".format(a=attacker, t=target),
            "{a} launched an assault on {t}".format(a=attacker, t=target),
            "{a} struck at {t}".format(a=attacker, t=target),
        ]
        return random.choice(utters)

    @classmethod
    def cannot_attack(cls, attacker: str, target: str, reason: str = None, possible_targets: list = []) -> str:
        """Return the utterance for not allowing attack"""
        if attacker == "player" or attacker == cls.game.player.name:
            attacker = "You"
        
        if possible_targets:
            p = "You could target {p}".format(p=possible_targets[0])
            for poss in possible_targets[1:]:
                if possible_targets[-1] == poss:
                    p += " or the {p}".format(p=poss)
                else:
                    p += ", the {p}".format(p=poss)
                    
        if not reason:
            return "{a} cannot attack {t}".format(a=attacker, t=target)
        elif reason == "unknown target":
            return "{a} cannot attack unknown target: {t}!".format(a=attacker, t=target)
        elif reason == "different loction":
            return "{a} cannot attack {t} as it's not in the same location as you!".format(a=attacker, t=target)
        elif reason == "no visibility":
            return "{a} cannot attack {t} because it's too dark to see them!".format(
                a=attacker, t=target) 
        elif reason == "dead target":
            return "{a} cannot attack {t} because they're already dead!".format(
                a=attacker, t=target) 
    
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
    def won_fight(cls) -> str:
        """Method to return the utterance for winning a fight"""
        utters = [
            "You won the battle, congratulations!",
            "You put up a good fight and it paid off",
            "Awesome, they won't be bothering you again!"
        ]
        return random.choice(utters)

    ############################################################
    # Roleplay utterances
    @classmethod
    def roleplay(cls, target: str) -> str:
        """Return the utterance for getting roleplay prompt"""
        n = cls.game.player.name
        utters = [
            "{n}, what do you say to {t}?".format(n=n, t=target)
        ]
        return random.choice(utters)

    ############################################################
    # Query utterances
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
    
    @classmethod
    def hp_end_game(cls, entity: str, death_text: str = "") -> str:
        """Return the utterance for ending the game by running out of hp"""
        utters = [
            "You were attacked and fatally wounded by {e}. {d}".format(e=entity, d=death_text),
            "{e} killed you! {d}".format(e=entity, d=death_text),
            "Nooo, you tried your hardest but it wasn't to be. {d}".format(e=entity, d=death_text),
        ]
        return random.choice(utters)