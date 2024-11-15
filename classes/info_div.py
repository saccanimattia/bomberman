font = "BombermanFonts.ttf"

import lib.g2d as g2d

type = {
    "start": (0, 0),
    "game_over": (0, 16),
    "new_level": (0, 32),
    "pause": (0, 48),
    "win": (0, 64),
    "scorer": (0, 80),
}

class InfoDiv:
    def __init__(self, type: str, ):
        self._type = type
        self._sprite = type[type]
        self._w, self._h = 16, 16