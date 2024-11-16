from classes.actor import Actor, Point, Arena, check_collision
from classes.ballom import Ballom
from classes.powerup import Powerup
from classes.wall import Wall
from classes.bomb import Bomb

TILE, STEP = 16, 2

Bomberman_steps = {
    "ArrowUp": [(48, 16), (64, 16), (80, 16)],
    "ArrowDown": [(48, 0),(64, 0), (80, 0)],
    "ArrowLeft": [(0, 0), (16, 0), (32, 0)],
    "ArrowRight": [(0, 16), (16, 16), (32, 16)],
}  

Bomberman_destroying_steps = [(0, 32), (16, 32), (32, 32), (48, 32), (64, 32), (80, 32), (96, 32)]

class Bomberman(Actor):
    def __init__(self, pos):
        
        #position
        self._x, self._y = pos
        self._dx, self._dy = 0, 0
        self._prev_dx, self._prev_dy = 0, 0
        self._w, self._h = TILE, TILE
        
        #sprite
        self._sprite = Bomberman_steps["ArrowDown"][1]
        
        #movement
        self._speed = STEP
        self._same_direction_count = 1
        
        #death
        self._death = False
        self._death_step = 0
        self._death_speed = 1
        self._awaiting_death = 40
        self._counter = 0

    def move(self, arena: Arena):

        #death animation
        if self._death:
            if self._awaiting_death > 0:
                self._awaiting_death -= 1
                return
            if self._death_step > (len(Bomberman_destroying_steps) - 1):
                arena.kill(self, 0)
                return
            self._counter += 1
            if self._counter % self._death_speed == 0:
                self._sprite = Bomberman_destroying_steps[self._death_step]
                self._death_step += 1
            return
        
        #powerup
        powerups = self._check_powerup_types(arena)
        if "speed" in powerups:
            self._speed = 4
        else:
            self._speed = 2
            
        #movement
        if self._x % TILE == 0 and self._y % TILE == 0:
            keys = arena.current_keys()
            direction_key = None
            self._prev_dx, self._prev_dy = self._dx, self._dy
            self._dx, self._dy = 0, 0

            if "Spacebar" in keys and not self.check_if_bomb(arena):
                arena.spawn(Bomb((self._x, self._y)))

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

        #collision with walls
        for actor in arena.actors():
            if isinstance(actor, Wall) and check_collision(self, actor):
                if actor.isDying() == True and actor.is_door() == True:
                    break
                self._x -= self._dx
                self._y -= self._dy
                break
            
        #collision with ballom
        for actor in arena.actors():
            if isinstance(actor, Ballom) and check_collision(self, actor):
                self.death_animation(1, 5, arena)
                break
                    

    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h

    def sprite(self) -> Point:
        return self._sprite
    
    def death_animation(self, speed: int, awaiting: int, arena: Arena):
        powerups = self._check_powerup_types(arena)
        if "bomb_immunity" in powerups:
            if self.check_enemies_collisions(arena) == True:
                self._death = True
                self._death_speed = speed
                self._awaiting_death = awaiting 
            return
    
        self._death = True
        self._death_speed = speed
        self._awaiting_death = awaiting
        
    
    def check_if_bomb(self, arena: Arena):
        for actor in arena.actors():
            if isinstance(actor, Bomb):
                return True
        return False
    
    def isDying(self):
        return self._death
    
    def _check_powerup_types(self, arena: Arena):
        powerups = []
        for actor in arena.actors():
            if isinstance(actor, Powerup):
                if actor.get_type() == "speed" and actor.isDying() == True:
                    powerups.append("speed")
                if actor.get_type() == "bomb_immunity" and actor.isDying() == True:
                    powerups.append("bomb_immunity")
        return powerups
    
    def check_enemies_collisions(self, arena: Arena):
        for actor in arena.actors():
            if isinstance(actor, Ballom) and check_collision(self, actor):
                return True
        return False