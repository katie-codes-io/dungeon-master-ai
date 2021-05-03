import random

class NLG():
    
    game = None
    
    @classmethod
    def set_game(cls, game) -> None:
        cls.game = game
    
    @classmethod
    def get_char_class(cls) -> str:
        '''Return utterance for character selection'''
        c = "\n".join(cls.game.domain.characters.get_all_names())
        utters = [
            "Which character class would you like to play?\n{c}".format(c=c),
            "Select a character class you like the sound of:\n{c}".format(c=c),
            "Select a character class from the following choices:\n{c}".format(c=c)
        ]
        return random.choice(utters)
    
    @classmethod
    def get_player_name(cls) -> str:
        '''Return the utterance for getting player's name'''
        c = cls.game.player.character_class
        utters = [
            "What is your character's name, this great {c}?".format(c=c),
            "Ahh, a {c}. Excellent choice! And what is your character's name?".format(c=c),
            "A {c}, marvelous! And what do they call your character?".format(c=c)
        ]
        return random.choice(utters)
    
    @classmethod
    def get_action(cls) -> str:
        '''Return the utterance for getting a player action'''
        n = cls.game.player.name
        utters = [
            "{n}, what do you do?".format(n=n)
        ]
        return random.choice(utters)