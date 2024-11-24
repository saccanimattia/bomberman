#imports
from classes.actor import Actor, Point, Arena
from random import randint

#constants
TILE, STEP = 16, 4

POWERUP_TYPES = {
    "speed": (32, 224),
    "bomb_immunity": (96, 224),
}

#class
class Powerup(Actor):
    def __init__(self, pos, type: str):
        
        #position
        self._x, self._y = pos
        self._w, self._h = TILE, TILE
        
        #sprite
        self._sprite = POWERUP_TYPES[type]
        self._type = type
        
        #expiration
        self._expiration = False
        self._expiration_time = 5
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
                arena.kill(self, 25)
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

    def is_dying(self):
        return self._expiration
