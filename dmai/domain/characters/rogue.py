from dmai.domain.characters.character import Character


class Rogue(Character):
    def __init__(self, character_data: dict) -> None:
        Character.__init__(self, character_data)
