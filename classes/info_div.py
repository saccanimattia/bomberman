font = "BombermanFont.ttf"

import lib.g2d as g2d

types = {
    "start": {
        "title": "Welcome to Bomberman",
        "subtitle": "Press 1 or 2 for the number of players.",
        "color": (0, 0, 255),
        "Points": False
    },
    "game_over": {
        "title": "Game Over",
        "subtitle": "Press Enter to restart",
        "color": (255, 0, 0),
        "Points": True
    },
    "game_won": {
        "title": "You won!",
        "subtitle": "Press Enter to restart",
        "color": (0, 255, 0),
        "Points": True
    },
    "level_finished":{
        "title": "Level Finished",
        "subtitle": "Press Enter to continue",
        "color": (255, 255, 0),
        "Points": True
    }
}

class InfoDiv:
    def __init__(self, type: str, w, h ):
        self._type = type
        self._w = w
        self._h = h
        
    def show(self, points: int | None):
        g2d.set_color((176, 176, 176))
        g2d.draw_rect((0, 0), (self._w, self._h))
        g2d.set_color(types[self._type]["color"])
        g2d.draw_text(types[self._type]["title"], (self._w//2, self._h//2 - 24), 20, font, "center")
        g2d.draw_text(types[self._type]["subtitle"], (self._w//2, self._h//2 + 12), 10, font, "center")
        if types[self._type]["Points"]:
            g2d.draw_text("Points: " + str(points), (self._w//2, self._h//2 + 28), 10, font, "center")

    def get_type(self):
        return self._type
    
    def set_type(self, type):
        if type in types:
            self._type = type