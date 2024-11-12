from classes.actor import Actor, Point, Arena, check_collision
from classes.wall import Wall
from random import choice

TILE, STEP = 16, 2

Ballom_destroying_steps = [(96, 240), (112, 240), (128, 240), (144, 240), (160, 240)]

class Ballom(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._x = self._x // TILE * TILE
        self._y = self._y // TILE * TILE
        self._w, self._h = TILE, TILE
        self._speed = STEP
        self._sprite = (0, 240)
        self._dx, self._dy = choice([(0, -STEP), (STEP, 0), (0, STEP), (-STEP, 0)])
        self._death = False
        self._awaiting_death = 40
        self._death_step = 0
        self._counter = 0

    def move(self, arena: Arena):
        if self._death:
            if self._awaiting_death > 0:
                self._awaiting_death -= 1
                return
            if self._death_step > (len(Ballom_destroying_steps) - 1):
                arena.kill(self)
                return
            self._counter += 1
            if self._counter % 15 == 0:
                self._sprite = Ballom_destroying_steps[self._death_step]
                self._death_step += 1
            return
        
        if self._x % TILE == 0 and self._y % TILE == 0:
            self._dx, self._dy = choice([(0, -STEP), (STEP, 0), (0, STEP), (-STEP, 0)])
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
    
    def death_animation(self):
        self._death = True

    def isDying(self):
        return self._death