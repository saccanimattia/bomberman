font = "BombermanFonts.ttf"

import lib.g2d as g2d

type = {
    "start": {
        "title": "Welcome to Bomberman",
        "subtitle": "Press Enter to start",
    }
}

class InfoDiv:
    def __init__(self, type: str, w, h ):
        self._type = type
        self._w = w
        self._h = h
        
    def show(self):
        g2d.set_color((0, 120, 0))
        g2d.draw_rect((0, 0), (self._w, self._h))
        g2d.set_color((255, 255, 255))
        g2d.draw_text(type[self._type]["title"], (self._w//2, self._h//2), 16, font, "center")
        g2d.draw_text(type[self._type]["subtitle"], (self._w//2, self._h//2 + 16), 16, font, "center")
        