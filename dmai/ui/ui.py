from dmai.game.game import Game


class UserInterface:
    def __init__(self, game: Game) -> None:
        """UserInterface class for the game and interacting with the DM"""
        self.game = game

    def execute(self) -> None:
        """Execute function which allows CLI communication between
        player and DM"""
        while True:
            output = self.game.output()
            if output:
                prompt = "\n" + output + "\n> "
            else:
                prompt = "\n> "
            user_input = input(prompt)
            self.game.input(user_input)
