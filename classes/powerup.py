from classes.actor import Actor, Point, Arena
from random import randint

TILE, STEP = 16, 4

Powerup_types = {
    "bomb": (0, 224),
    "speed": (16, 224),
    "bomb_immunity": (64, 224),
}

class Powerup(Actor):
    def __init__(self, pos, type: str):
        
        #position
        self._x, self._y = pos
        self._w, self._h = TILE, TILE
        
        #sprite
        self._sprite = Powerup_types[type]
        self._type = type
        
        #expiration
        self._expiration = False
        self._expiration_time = 10
        self._counter = 0



    def move(self, arena: Arena):
        #expiration
        if self._expiration:
            self._sprite = (224, 0)
            if self._counter == 30 :
                self._expiration_time -= 1
                self._counter = 0
            self._counter += 1
            if self._expiration_time == 0:
                arena.kill(self, 0)
                return
    
    def get_type(self):
        return self._type

    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h

    def sprite(self) -> Point:
        return self._sprite
    
    def death_animation(self, speed: int, awaiting: int, arena: Arena):
        self._expiration = True

    def isDying(self):
        return self._expiration
