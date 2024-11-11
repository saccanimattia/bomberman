from classes.actor import Actor, Point, Arena, check_collision


Bomb_steps = [(0, 64), (16, 64), (32, 64), (0, 64), (80, 64), (0, 144), (80, 144)]

TILE = 16

class Bomb(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._x = self._x // TILE * TILE
        self._y = self._y // TILE * TILE
        self._w, self._h = TILE, TILE
        self._step = 0
        self._sprite = Bomb_steps[0]

    def move(self, arena: Arena):
        self._step += 1
        if self._step == len(Bomb_steps):
            arena.remove(self)
            return
        self._sprite = Bomb_steps[self._step]

    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h

    def sprite(self) -> Point:
        return 0, 240