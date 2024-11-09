from classes.actor import Actor, Point, Arena
from random import choice

TILE, STEP = 16, 4

class Ballom(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._x = self._x // TILE * TILE
        self._y = self._y // TILE * TILE
        self._w, self._h = TILE, TILE
        self._speed = STEP
        self._dx, self._dy = choice([(0, -STEP), (STEP, 0), (0, STEP), (-STEP, 0)])

    def move(self, arena: Arena):
        if self._x % TILE == 0 and self._y % TILE == 0:
            self._dx, self._dy = choice([(0, -STEP), (STEP, 0), (0, STEP), (-STEP, 0)])
        self._x += self._dx
        self._y += self._dy

    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h

    def sprite(self) -> Point:
        return 0, 240