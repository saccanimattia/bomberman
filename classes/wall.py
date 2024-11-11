from classes.actor import Actor, Point, Arena

TILE, STEP = 16, 4

Wall_types = {
    "destroyable": (64, 48),
    "indestructible": (48, 48),
}

class Wall(Actor):
    def __init__(self, pos, wall_type: str):
        self._x, self._y = pos
        self._w, self._h = TILE, TILE
        self._sprite = Wall_types[wall_type]

    def move(self, arena: Arena):
        return

    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h

    def sprite(self) -> Point:
        return self._sprite