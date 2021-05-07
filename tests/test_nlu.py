import unittest
import sys
import os

p = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, p + "/../")

from dmai.nlu.nlu import NLU
from dmai.utils.exceptions import UnrecognisedCommandError


class TestNLU(unittest.TestCase):
    """Test the NLU class"""

    def setUp(self) -> None:
        self.roll_cmd1 = "/roll d20"
        self.help_cmd = "/help"
        self.exit_cmd = "/exit"
        self.bad_cmd1 = "roll d20"
        self.bad_cmd2 = "/unknown"

    def test_show_commands(self) -> None:
        actual = "\nCommands:\n"
        actual += "/help           Show these commands\n"
        actual += "/exit           Exit the game\n"
        actual += "/roll [die]     Roll a specified die, options: d4, d6, d8, d10, d12, d20, d100 (d20 by default)\n"

        self.assertEqual(NLU.show_commands(), actual)

    def test_process_player_command_help(self) -> None:
        self.assertEqual(NLU.process_player_command(self.help_cmd), True)

    def test_process_player_command_roll(self) -> None:
        self.assertEqual(NLU.process_player_command(self.roll_cmd1), True)

    def test_process_player_command_exit(self) -> None:
        with self.assertRaises(SystemExit):
            NLU.process_player_command(self.exit_cmd)

    def test_process_player_command_malformed(self) -> None:
        self.assertEqual(NLU.process_player_command(self.bad_cmd1), False)
        self.assertEqual(NLU.process_player_command(self.bad_cmd2), True)

    def test_regex_help(self) -> None:
        self.assertEqual(NLU._regex(self.help_cmd), True)

    def test_regex_roll(self) -> None:
        self.assertEqual(NLU._regex(self.roll_cmd1), True)

    def test_regex_exit(self) -> None:
        with self.assertRaises(SystemExit):
            NLU._regex(self.exit_cmd)

    def test_regex_malformed(self) -> None:
        with self.assertRaises(UnrecognisedCommandError):
            NLU._regex(self.bad_cmd1)
        with self.assertRaises(UnrecognisedCommandError):
            NLU._regex(self.bad_cmd2)


if __name__ == "__main__":
    unittest.main()
