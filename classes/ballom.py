#imports
from classes.actor import Actor, Point, Arena, check_collision
from classes.wall import Wall
from random import choice

#constants

TILE, STEP = 16, 2
BALLOM_DESTROYING_STEPS = {
    "first": [(96, 240), (112, 240), (128, 240), (144, 240), (160, 240)],
    "second": [(96, 256), (112, 288), (128, 288), (144, 288), (160, 288)],
    "third": [(96, 320), (112, 272), (128, 272), (144, 272), (160, 272)]
}
BALLOM_MOVING_STEPS = {
    "first": [(0, 240), (16, 240), (32, 240), (48, 240), (64, 240), (80, 240)],
    "second": [(0, 256), (16, 256), (32, 256), (48, 256), (64, 256), (80, 256)],
    "third": [(0, 320), (16, 320), (32, 320), (48, 320), (64, 320), (80, 320)]
}

#class
class Ballom(Actor):
    
    def __init__(self, pos, type):
           
        #position
        self._x, self._y = pos
        self._x = self._x // TILE * TILE
        self._y = self._y // TILE * TILE
        self._w, self._h = TILE, TILE
        
        #sprite
        self._timer = 0
        self._type = type
        self._sprite_index = 0
        if type == "first":
            self._sprite = BALLOM_MOVING_STEPS["first"][self._sprite_index]
        elif type == "second":
            self._sprite = BALLOM_MOVING_STEPS["second"][self._sprite_index]
        elif type == "third":
            self._sprite = BALLOM_MOVING_STEPS["third"][self._sprite_index]
        else:
            raise ValueError("Invalid type")
        
        #movement
        self._speed = STEP
        self._dx, self._dy = choice([(0, -STEP), (STEP, 0), (0, STEP), (-STEP, 0)])
        
        #death
        self._death = False
        self._death_step = 0
        self._awaiting_death = 40
        self._counter = 0
        self._death_speed = 1


    def move(self, arena: Arena):
        
        #death animation
        if self._death:
            if self._awaiting_death > 0:
                self._awaiting_death -= 1
                return
            if self._death_step > (len(BALLOM_DESTROYING_STEPS) - 1):
                arena.kill(self, 100)
                return
            self._counter += 1
            if self._counter % self._death_speed == 0:
                self._sprite = BALLOM_DESTROYING_STEPS[self._type][self._death_step]
                self._death_step += 1
            return
        
        #movement
        if self._x % TILE == 0 and self._y % TILE == 0:
            self._dx, self._dy = choice([(0, -STEP), (STEP, 0), (0, STEP), (-STEP, 0)])
        self._x += self._dx
        self._y += self._dy
        
        #sprite
        if self._timer % 10 == 0:
            self._sprite = BALLOM_MOVING_STEPS[self._type][self._sprite_index]
            self._sprite_index += 1
            if self._sprite_index > (len(BALLOM_MOVING_STEPS[self._type]) - 1):
                self._sprite_index = 0
        self._timer += 1
        
        #collision with walls and bomberman
        for actor in arena.actors():
            if isinstance(actor, Wall) and check_collision(self, actor):
                self._x -= self._dx
                self._y -= self._dy

    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h

    def sprite(self) -> Point:
        return self._sprite
    
    def death_animation(self, speed: int, awaiting: int, arena: Arena):
        self._death = True
        self._death_speed = speed
        self._awaiting_death = awaiting

    def is_dying(self):
        return self._death