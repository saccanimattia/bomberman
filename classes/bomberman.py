from classes.actor import Actor, Point, Arena, check_collision
from classes.wall import Wall

TILE, STEP = 16, 4

class Bomberman(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._dx, self._dy = 0, 0
        self._w, self._h = TILE, TILE
        self._speed = STEP

    def move(self, arena: Arena):
        if self._x % TILE == 0 and self._y % TILE == 0:
            self._dx, self._dy = 0, 0
            keys = arena.current_keys()
            if "ArrowUp" in keys:
                self._dy = -self._speed
            elif "ArrowDown" in keys:
                self._dy = self._speed
            elif "ArrowLeft" in keys:
                self._dx = -self._speed
            elif "ArrowRight" in keys:
                self._dx = self._speed

        self._x += self._dx
        self._y += self._dy
        
        for actor in arena.actors():
            if isinstance(actor, Wall) and check_collision(self, actor):
                self._x -= self._dx
                self._y -= self._dy
                arena.collisions()
                print(arena.collisions())
                arena.remove_collision_with(actor)
                break


    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h

    def sprite(self) -> Point:
        return 64, 0