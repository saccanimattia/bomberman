from classes.actor import Actor, Point, Arena

TILE, STEP = 16, 4

Wall_types = {
    "destroyable": (64, 48),
    "indestructible": (48, 48),
    "door": (176, 48)
}

Wall_destroying_steps = [(80, 48), (96, 48), (112, 48), (128, 48), (144, 48), (160, 48)]

class Wall(Actor):
    def __init__(self, pos, wall_type: str, is_door: bool):
        
        #position
        self._x, self._y = pos
        self._w, self._h = TILE, TILE
        
        #sprite
        self._sprite = Wall_types[wall_type]
        self._type = wall_type
        
        #death
        self._death = False
        self._awaiting_death = 0
        self._death_animation = 1
        self._counter = 0
        self._death_step = 0
        
        #door
        self._is_door = is_door

    def move(self, arena: Arena):
        
        #death animation
        
        if self._death:
            if self._awaiting_death > 0:
                self._awaiting_death -= 1
                return
            if self._death_step > (len(Wall_destroying_steps) - 1):
                if self._is_door == True:
                    self._sprite = Wall_types["door"]
                    return
                else:
                    arena.kill(self)
                    return
            self._counter += 1
            if self._counter % self._death_speed == 0:
                self._sprite = Wall_destroying_steps[self._death_step]
                self._death_step += 1
            return
    
    def getType(self):
        return self._type

    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h

    def sprite(self) -> Point:
        return self._sprite
    
    def death_animation(self, speed: int, awaiting: int):
        self._death = True
        self._death_speed = 2
        self._awaiting_death = 0

    def isDying(self):
        return self._death
    
    def is_door(self):
        return self._is_door