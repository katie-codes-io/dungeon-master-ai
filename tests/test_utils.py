import unittest
import sys
import os

p = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, p + "/../")

from dmai.utils.dice_roller import DiceRoller
from dmai.utils.text import Text
from dmai.utils.output_builder import OutputBuilder



class TestOutputBuilder(unittest.TestCase):
    """Test the self.output_builder class"""

    def setUp(self) -> None:
        self.output_builder = OutputBuilder()

    def test_format(self) -> None:
        self.output_builder.clear()
        statement1 = "This is a statement"
        statement2 = "Also this is a statement"
        statement3 = "And this one"
        self.output_builder.append(statement1)
        self.output_builder.append(statement2)
        self.output_builder.append(statement3)
        self.assertEqual(self.output_builder.format(), "This is a statement\n\nAlso this is a statement\n\nAnd this one\n")
        
    
class TestText(unittest.TestCase):
    """Test the Text class"""

    def setUp(self) -> None:
        pass

    def test_get_signed_value(self) -> None:
        self.assertEqual(Text.get_signed_value(0), "")
        self.assertEqual(Text.get_signed_value(-1), "-1")
        self.assertEqual(Text.get_signed_value(1), "+1")

    def test_properly_format_list_single(self) -> None:
        values = ["single"]
        self.assertEqual(Text.properly_format_list(values), "single")
        self.assertEqual(Text.properly_format_list(values, delimiter="\t"), "single")
        self.assertEqual(
            Text.properly_format_list(values, last_delimiter=" or "), "single"
        )
        self.assertEqual(
            Text.properly_format_list(values, delimiter="\t", last_delimiter=" or "),
            "single",
        )
    
    def test_properly_format_list_double(self) -> None:
        values = ["single", "double"]
        self.assertEqual(Text.properly_format_list(values), "single and double")
        self.assertEqual(Text.properly_format_list(values, delimiter="\t"), "single and double")
        self.assertEqual(
            Text.properly_format_list(values, last_delimiter=" or "), "single or double"
        )
        self.assertEqual(
            Text.properly_format_list(values, delimiter="\t", last_delimiter=" or "),
            "single or double",
        )
    
    def test_properly_format_list_multi(self) -> None:
        values = ["single", "double", "multi"]
        self.assertEqual(Text.properly_format_list(values), "single, double and multi")
        self.assertEqual(Text.properly_format_list(values, delimiter="\t"), "single\tdouble and multi")
        self.assertEqual(
            Text.properly_format_list(values, last_delimiter=" or "), "single, double or multi"
        )
        self.assertEqual(
            Text.properly_format_list(values, delimiter="\t", last_delimiter=" or "),
            "single\tdouble or multi",
        )


class TestDiceRoller(unittest.TestCase):
    """Test the DiceRoller class"""

    def setUp(self) -> None:
        self.dice = {
            "d4": {"specs": {"die": "d4", "total": 2, "mod": 1}, "min": 3, "max": 9},
            "d6": {"specs": {"die": "d6", "total": 3, "mod": 2}, "min": 5, "max": 20},
            "d8": {"specs": {"die": "d8", "total": 3, "mod": 2}, "min": 5, "max": 26},
            "d10": {"specs": {"die": "d10", "total": 2, "mod": 0}, "min": 2, "max": 20},
            "d12": {"specs": {"die": "d12", "total": 3, "mod": 3}, "min": 6, "max": 39},
            "d20": {"specs": {"die": "d20", "total": 2, "mod": 2}, "min": 4, "max": 42},
            "d100": {
                "specs": {"die": "d100", "total": 1, "mod": 0},
                "min": 1,
                "max": 100,
            },
        }

    def test_roll_die(self) -> None:
        bad_die1 = "d3"
        bad_die2 = "22"
        with self.assertRaises(KeyError):
            DiceRoller.roll_die(bad_die1)
        with self.assertRaises(KeyError):
            DiceRoller.roll_die(bad_die2)

    def test_roll_dice_d4(self) -> None:
        # roll d4 600 times
        total_rolls = 600
        rolls = [
            DiceRoller.roll_dice(self.dice["d4"]["specs"])[1] for _ in range(total_rolls)
        ]

        self.assertGreaterEqual(min(rolls), self.dice["d4"]["min"])
        self.assertLessEqual(max(rolls), self.dice["d4"]["max"])
        self.assertAlmostEqual(
            rolls.count(self.dice["d4"]["min"]) / total_rolls,
            rolls.count(self.dice["d4"]["max"]) / total_rolls,
            places=1,
        )

    def test_roll_dice_d6(self) -> None:
        # roll d6 600 times
        total_rolls = 600
        rolls = [
            DiceRoller.roll_dice(self.dice["d6"]["specs"])[1] for _ in range(total_rolls)
        ]

        self.assertGreaterEqual(min(rolls), self.dice["d6"]["min"])
        self.assertLessEqual(max(rolls), self.dice["d6"]["max"])
        self.assertAlmostEqual(
            rolls.count(self.dice["d6"]["min"]) / total_rolls,
            rolls.count(self.dice["d6"]["max"]) / total_rolls,
            places=1,
        )

    def test_roll_dice_d8(self) -> None:
        # roll d8 600 times
        total_rolls = 600
        rolls = [
            DiceRoller.roll_dice(self.dice["d8"]["specs"])[1] for _ in range(total_rolls)
        ]

        self.assertGreaterEqual(min(rolls), self.dice["d8"]["min"])
        self.assertLessEqual(max(rolls), self.dice["d8"]["max"])
        self.assertAlmostEqual(
            rolls.count(self.dice["d8"]["min"]) / total_rolls,
            rolls.count(self.dice["d8"]["max"]) / total_rolls,
            places=1,
        )

    def test_roll_dice_d10(self) -> None:
        # roll d10 600 times
        total_rolls = 600
        rolls = [
            DiceRoller.roll_dice(self.dice["d10"]["specs"])[1] for _ in range(total_rolls)
        ]

        self.assertGreaterEqual(min(rolls), self.dice["d10"]["min"])
        self.assertLessEqual(max(rolls), self.dice["d10"]["max"])
        self.assertAlmostEqual(
            rolls.count(self.dice["d10"]["min"]) / total_rolls,
            rolls.count(self.dice["d10"]["max"]) / total_rolls,
            places=1,
        )

    def test_roll_dice_d12(self) -> None:
        # roll d12 600 times
        total_rolls = 600
        rolls = [
            DiceRoller.roll_dice(self.dice["d12"]["specs"])[1] for _ in range(total_rolls)
        ]

        self.assertGreaterEqual(min(rolls), self.dice["d12"]["min"])
        self.assertLessEqual(max(rolls), self.dice["d12"]["max"])
        self.assertAlmostEqual(
            rolls.count(self.dice["d12"]["min"]) / total_rolls,
            rolls.count(self.dice["d12"]["max"]) / total_rolls,
            places=1,
        )

    def test_roll_dice_d20(self) -> None:
        # roll d20 600 times
        total_rolls = 600
        rolls = [
            DiceRoller.roll_dice(self.dice["d20"]["specs"])[1] for _ in range(total_rolls)
        ]

        self.assertGreaterEqual(min(rolls), self.dice["d20"]["min"])
        self.assertLessEqual(max(rolls), self.dice["d20"]["max"])
        self.assertAlmostEqual(
            rolls.count(self.dice["d20"]["min"]) / total_rolls,
            rolls.count(self.dice["d20"]["max"]) / total_rolls,
            places=1,
        )

    def test_roll_dice_d100(self) -> None:
        # roll d100 600 times
        total_rolls = 600
        rolls = [
            DiceRoller.roll_dice(self.dice["d100"]["specs"])[1] for _ in range(total_rolls)
        ]

        self.assertGreaterEqual(min(rolls), self.dice["d100"]["min"])
        self.assertLessEqual(max(rolls), self.dice["d100"]["max"])
        self.assertAlmostEqual(
            rolls.count(self.dice["d100"]["min"]) / total_rolls,
            rolls.count(self.dice["d100"]["max"]) / total_rolls,
            places=1,
        )

    def test_roll_dice_malformed(self) -> None:
        bad_spec1 = {"die": "d3", "total": 1, "mod": 2}
        bad_spec2 = {"die": "d4", "total": 1}
        bad_spec3 = {"type": "d4", "total": 1, "mod": 0}
        bad_spec4 = {"die": "d4", "total": "1", "mod": 0}

        with self.assertRaises(KeyError):
            DiceRoller.roll_dice(bad_spec1)
        with self.assertRaises(KeyError):
            DiceRoller.roll_dice(bad_spec2)
        with self.assertRaises(KeyError):
            DiceRoller.roll_dice(bad_spec3)
        with self.assertRaises(TypeError):
            DiceRoller.roll_dice(bad_spec4)
    
    def test_get_min_die(self) -> None:
        self.assertEqual(1, DiceRoller.get_min(die="d4")[1])
        self.assertEqual(1, DiceRoller.get_min(die="d20")[1])
        self.assertEqual(2, DiceRoller.get_min(die="2d4")[1])
        self.assertEqual(3, DiceRoller.get_min(die="3d20")[1])
        self.assertEqual(-1, DiceRoller.get_min(die="2d4-3")[1])
        self.assertEqual(7, DiceRoller.get_min(die="2d12+5")[1])

    def test_get_min_dice_spec(self) -> None:
        spec1 = {"die": "d4", "total": 1, "mod": 0}
        spec2 = {"die": "d20", "total": 1, "mod": 0}
        spec3 = {"die": "d4", "total": 2, "mod": 0}
        spec4 = {"die": "d20", "total": 3, "mod": 0}
        spec5 = {"die": "d4", "total": 2, "mod": -3}
        spec6 = {"die": "d12", "total": 2, "mod": 5}

        self.assertEqual(1, DiceRoller.get_min(dice_spec=spec1)[1])
        self.assertEqual(1, DiceRoller.get_min(dice_spec=spec2)[1])
        self.assertEqual(2, DiceRoller.get_min(dice_spec=spec3)[1])
        self.assertEqual(3, DiceRoller.get_min(dice_spec=spec4)[1])
        self.assertEqual(-1, DiceRoller.get_min(dice_spec=spec5)[1])
        self.assertEqual(7, DiceRoller.get_min(dice_spec=spec6)[1])

    def test_get_max_die(self) -> None:
        self.assertEqual(4, DiceRoller.get_max(die="d4")[1])
        self.assertEqual(20, DiceRoller.get_max(die="d20")[1])
        self.assertEqual(8, DiceRoller.get_max(die="2d4")[1])
        self.assertEqual(60, DiceRoller.get_max(die="3d20")[1])
        self.assertEqual(5, DiceRoller.get_max(die="2d4-3")[1])
        self.assertEqual(29, DiceRoller.get_max(die="2d12+5")[1])

    def test_get_max_dice_spec(self) -> None:
        spec1 = {"die": "d4", "total": 1, "mod": 0}
        spec2 = {"die": "d20", "total": 1, "mod": 0}
        spec3 = {"die": "d4", "total": 2, "mod": 0}
        spec4 = {"die": "d20", "total": 3, "mod": 0}
        spec5 = {"die": "d4", "total": 2, "mod": -3}
        spec6 = {"die": "d12", "total": 2, "mod": 5}

        self.assertEqual(4, DiceRoller.get_max(dice_spec=spec1)[1])
        self.assertEqual(20, DiceRoller.get_max(dice_spec=spec2)[1])
        self.assertEqual(8, DiceRoller.get_max(dice_spec=spec3)[1])
        self.assertEqual(60, DiceRoller.get_max(dice_spec=spec4)[1])
        self.assertEqual(5, DiceRoller.get_max(dice_spec=spec5)[1])
        self.assertEqual(29, DiceRoller.get_max(dice_spec=spec6)[1])

if __name__ == "__main__":
    unittest.main()
