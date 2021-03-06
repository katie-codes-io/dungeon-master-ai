import random

from dmai.utils.exceptions import DiceFormatError


class DiceRollerMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs) -> None:
        """DiceRoller static singleton metaclass"""
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class DiceRoller(metaclass=DiceRollerMeta):

    # class variables
    dice_map = {
        "d4": 4,
        "d6": 6,
        "d8": 8,
        "d10": 10,
        "d12": 12,
        "d20": 20,
        "d100": 100
    }

    def __init__(self) -> None:
        """DiceRoller static class"""
        pass

    @classmethod
    def roll(cls, die: str, silent: bool = False, min: bool = False, max: bool = False) -> int:
        """Roll a die supplied by the user"""
        die = die.lower()

        # identify d, plus and minus
        d = die.find("d")
        plus = die.find("+")
        minus = die.find("-")

        if d == -1:
            msg = 'Cannot roll dice: "{d}"\nUse format /roll d4 or /roll 2d12+2 for example'.format(
                d=die)
            raise DiceFormatError(msg)

        try:
            # convert the string into a die spec and pass to roll_dice
            total = 1 if not die[0:d] else int(die[0:d])
            if plus != -1:
                dice_spec = {
                    "die": die[d:plus],
                    "total": total,
                    "mod": int(die[plus:])
                }
            elif minus != -1:
                dice_spec = {
                    "die": die[d:minus],
                    "total": total,
                    "mod": int(die[minus:]),
                }
            else:
                dice_spec = {"die": die[d:], "total": total, "mod": 0}

            (roll_str, dice_val) = cls.roll_dice(dice_spec, silent, min, max)
            return (roll_str, dice_val)

        except (KeyError, TypeError, ValueError) as e:
            msg = 'Cannot roll dice: "{d}"\nUse format /roll d4 or /roll 2d12+2 for example'.format(
                d=die)
            raise DiceFormatError(msg)


    @classmethod
    def roll_die(cls, die: str, silent: bool = False) -> int:
        """Roll singular specified die"""
        die = die.lower()

        try:
            max_val = cls.dice_map[die]
            val = random.randint(1, max_val)
            roll_str = ""
            if not silent:
                roll_str = "Rolling {d}... {v}".format(d=die, v=val)
        except KeyError as e:
            raise

        return (roll_str, val)

    @classmethod
    def roll_dice(cls, dice_spec: dict, silent: bool = False, min: bool = False, max: bool = False) -> int:
        """Roll dice according to spec in dictionary:\n
        {
            "die": "d4",
            "total": 1,
            "mod": 0
        }
        """
        try:
            dice = range(dice_spec["total"])
            max_val = cls.dice_map[dice_spec["die"]]
            modifier = dice_spec["mod"]
            if min:
                rolls = [1 for _ in dice]
            elif max:
                rolls = [max_val for _ in dice]
            else:
                rolls = [random.randint(1, max_val) for _ in dice]
            total_roll = sum(rolls) + modifier
            die = cls.construct_dice_spec_string(dice_spec)
            roll_str = ""
            if not silent:
                roll_str = "Rolling {d}... {t}".format(d=die, t=total_roll)
        except (KeyError, TypeError, ValueError) as e:
            raise

        return (roll_str, total_roll)

    @classmethod
    def check(cls, die: str) -> None:
        """Method to check a die, does not output anything.
        Raises a DiceFormatError if badly formatted."""
        try:
            cls.dice_map[die]
        except:
            msg = 'Cannot roll unrecognised dice: "{d}"\n'.format(d=die)
            raise DiceFormatError(msg)
        
    @classmethod
    def get_max(cls, die: str = None, dice_spec: dict = {}, silent: bool = True) -> int:
        if die:
            return cls.roll(die, silent=silent, max=True)
        if dice_spec:
            return cls.roll_dice(dice_spec, silent=silent, max=True)
    
    @classmethod
    def get_min(cls, die: str = None, dice_spec: dict = {}, silent: bool = True) -> int:
        if die:
            return cls.roll(die, silent=silent, min=True)
        if dice_spec:
            return cls.roll_dice(dice_spec, silent=silent, min=True)

    @classmethod
    def construct_dice_spec_string(cls, dice_spec: dict) -> str:
        # construct the spec string
        d = dice_spec["die"]

        t = dice_spec["total"]
        if t == 1:
            t = ""

        m = dice_spec["mod"]
        if m == 0:
            m = ""
        elif m > 0:
            m = "+{m}".format(m=dice_spec["mod"])

        return "{t}{d}{m}".format(t=t, d=d, m=m)
