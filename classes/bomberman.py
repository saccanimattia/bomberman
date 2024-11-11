from classes.actor import Actor, Point, Arena, check_collision
from classes.wall import Wall

TILE, STEP = 16, 4

Bomberman_steps = {
    "ArrowUp": [(48, 16), (64, 16), (80, 16)],
    "ArrowDown": [(48, 0),(64, 0), (80, 0)],
    "ArrowLeft": [(0, 0), (16, 0), (32, 0)],
    "ArrowRight": [(0, 16), (16, 16), (32, 16)],
}  

class Bomberman(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._dx, self._dy = 0, 0
        self._prev_dx, self._prev_dy = 0, 0
        self._w, self._h = TILE, TILE
        self._sprite = Bomberman_steps["ArrowDown"][1]
        self._speed = STEP
        self._same_direction_count = 1

    def move(self, arena: Arena):

        if self._x % TILE == 0 and self._y % TILE == 0:

            keys = arena.current_keys()
            direction_key = None
            self._prev_dx, self._prev_dy = self._dx, self._dy
            self._dx, self._dy = 0, 0

            if "ArrowUp" in keys:
                direction_key = "ArrowUp"
                self._dy = -self._speed
            elif "ArrowDown" in keys:
                direction_key = "ArrowDown"
                self._dy = self._speed
            elif "ArrowLeft" in keys:
                direction_key = "ArrowLeft"
                self._dx = -self._speed
            elif "ArrowRight" in keys:
                direction_key = "ArrowRight"
                self._dx = self._speed

            if self._dx == self._prev_dx and self._dy == self._prev_dy :
                self._same_direction_count += 1
            else:
                self._same_direction_count = 1
            
            if direction_key:
                self._sprite = Bomberman_steps[direction_key][self._same_direction_count % 3]


        self._x += self._dx
        self._y += self._dy

        for actor in arena.actors():
            if isinstance(actor, Wall) and check_collision(self, actor):
                self._x -= self._dx
                self._y -= self._dy
                break

    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h

    def sprite(self) -> Point:
        return self._sprite