from classes.actor import Actor, Point, Arena, check_collision_coordinate
from classes.wall import Wall
import lib.g2d as g2d


Bomb_steps = [(0, 48), (16, 48), (32, 48)]

Bomb_explosion = [(32, 96), (112, 96), (32, 176), (112, 176)]

Bomb_effect = {
    "up": {
      "middle": [(32, 80), (112, 80), (32, 160), (112, 160)],
       "end": [(32, 64), (112, 64), (32, 144), (112, 144)]
    },
    "down": {
        "middle": [(32, 112), (112, 112), (32, 192), (112, 192)],
        "end": [(32, 128), (112, 128), (32, 208), (112, 208)]
    },
    "left": {
        "middle": [(16, 96), (96, 96), (16, 176), (96, 176)],
        "end": [(0, 96), (80, 96), (0, 176), (80, 176)]
    },
    "right": {
        "middle": [(48, 96), (128, 96), (48, 176), (128, 176)],
        "end": [(64, 96), (144, 96), (64, 176), (144, 176)]
    }
}

TILE = 16

class Bomb(Actor):
    def __init__(self, pos):
        
        #position
        self._x, self._y = pos
        self._x = self._x // TILE * TILE
        self._y = self._y // TILE * TILE
        self._w, self._h = TILE, TILE
        
        #sprite
        self._bomb_step = 0
        self._bomb_explosion = 0
        self._counter = 0
        self._sprite = Bomb_steps[self._bomb_explosion]

    def move(self, arena: Arena):
        
        #bomb explosion animation
        self._counter += 1
        
        if self._counter % 20 == 0:
            if self._bomb_step > (len(Bomb_steps) - 1):
                if self._bomb_explosion > (len(Bomb_explosion) - 1):
                    
                    #destroy objects and bomb
                    self.destroy_objects(arena)
                    arena.kill(self)
                    
                else:
                    
                    #explosion animation
                    self._sprite = Bomb_explosion[self._bomb_explosion]
                    self._bomb_explosion += 1
                    
            else:
                
                #bomb animation
                self._bomb_step += 1

        if self._bomb_step < len(Bomb_steps):
            img = "img/bomberman.png"
            g2d.draw_image(img, (self._x, self._y ), Bomb_steps[self._bomb_step], (self._w, self._h)) 
        
        if self._bomb_explosion <= (len(Bomb_explosion) - 1) and self._bomb_step > (len(Bomb_steps) - 1):
            img = "img/bomberman.png"
            g2d.draw_image(img, (self._x, self._y), Bomb_explosion[self._bomb_explosion], (self._w, self._h))
            self.spawn_explosion(arena, img)


    def spawn_explosion(self, arena: Arena, img):

        center = self.is_colliding(self._x, self._y, arena)

        if(center == 3):
            self.destroy(self._x, self._y, arena)

        middle_up = self.is_colliding(self._x, self._y - 16 , arena)
        end_up = self.is_colliding(self._x, self._y - 32, arena)

        if(middle_up == 3): 
            self.destroy(self._x, self._y - 16, arena)
        if(end_up == 3 and (middle_up == 2 or middle_up == 3)):
            self.destroy(self._x, self._y - 32, arena)

        if(middle_up != 0):
            g2d.draw_image(img, (self._x, self._y - 16), Bomb_effect["up"]["end"][self._bomb_explosion], (self._w, self._h))
        if(middle_up == 2 or middle_up == 3):
            if end_up != 0:
                g2d.draw_image(img, (self._x, self._y - 16), Bomb_effect["up"]["middle"][self._bomb_explosion], (self._w, self._h))
                g2d.draw_image(img, (self._x, self._y - 32), Bomb_effect["up"]["end"][self._bomb_explosion], (self._w, self._h))

        middle_down = self.is_colliding(self._x, self._y + 16, arena)
        end_down = self.is_colliding(self._x, self._y + 32, arena)

        if(middle_down == 3):
            self.destroy(self._x, self._y + 16, arena)
        if(end_down == 3 and (middle_down == 2 or middle_down == 3)):
            self.destroy(self._x, self._y + 32, arena)

        if(middle_down != 0):
            g2d.draw_image(img, (self._x, self._y + 16), Bomb_effect["down"]["end"][self._bomb_explosion], (self._w, self._h))
        if(middle_down == 2 or middle_down == 3):
            if end_down != 0:
                g2d.draw_image(img, (self._x, self._y + 16), Bomb_effect["down"]["middle"][self._bomb_explosion], (self._w, self._h))
                g2d.draw_image(img, (self._x, self._y + 32), Bomb_effect["down"]["end"][self._bomb_explosion], (self._w, self._h))
        
        middle_left = self.is_colliding(self._x - 16, self._y, arena)
        end_left = self.is_colliding(self._x - 32, self._y, arena)

        if(middle_left == 3):
            self.destroy(self._x - 16, self._y, arena)
        if(end_left == 3 and (middle_left == 2 or middle_left == 3)):
            self.destroy(self._x - 32, self._y, arena)

        if(middle_left != 0):
            g2d.draw_image(img, (self._x - 16, self._y), Bomb_effect["left"]["end"][self._bomb_explosion], (self._w, self._h))
        if(middle_left == 2 or middle_left == 3):
            if end_left != 0:
                g2d.draw_image(img, (self._x - 16, self._y), Bomb_effect["left"]["middle"][self._bomb_explosion], (self._w, self._h))
                g2d.draw_image(img, (self._x - 32, self._y), Bomb_effect["left"]["end"][self._bomb_explosion], (self._w, self._h))

        middle_right = self.is_colliding(self._x + 16, self._y, arena)
        end_right = self.is_colliding(self._x + 32, self._y, arena)

        if(middle_right == 3):
            self.destroy(self._x + 16, self._y, arena)
        if(end_right == 3 and (middle_right == 2 or middle_right == 3)):
            self.destroy(self._x + 32, self._y, arena)

        if(middle_right != 0):
            g2d.draw_image(img, (self._x + 16, self._y), Bomb_effect["right"]["end"][self._bomb_explosion], (self._w, self._h))
        if(middle_right == 2 or middle_right == 3):
            if end_right != 0:
                g2d.draw_image(img, (self._x + 16, self._y), Bomb_effect["right"]["middle"][self._bomb_explosion], (self._w, self._h))
                g2d.draw_image(img, (self._x + 32, self._y), Bomb_effect["right"]["end"][self._bomb_explosion], (self._w, self._h))


    def is_colliding(self, x, y, arena: Arena):
        for actor in arena.actors():
            if isinstance(actor, Wall) and check_collision_coordinate(actor, x, y, self._w, self._h):
                if actor.getType() == "indestructible":
                    return 0
                return 1
            elif isinstance(actor, Wall) == False and check_collision_coordinate(actor, x, y, self._w, self._h) and isinstance(actor, Bomb) == False:
                return 3
        return 2

    def destroy_objects(self, arena: Arena):
        
        middle_up = self.is_colliding(self._x, self._y - 16, arena)
        end_up = self.is_colliding(self._x, self._y - 32, arena)
        middle_down = self.is_colliding(self._x, self._y + 16, arena)
        end_down = self.is_colliding(self._x, self._y + 32, arena)
        middle_left = self.is_colliding(self._x - 16, self._y, arena)
        end_left = self.is_colliding(self._x - 32, self._y, arena)
        middle_right = self.is_colliding(self._x + 16, self._y, arena)
        end_right = self.is_colliding(self._x + 32, self._y, arena)
        
        if middle_up != 0 and end_up == 1:
            self.destroy(self._x, self._y - 32, arena)
        if middle_up == 1 :
            self.destroy(self._x, self._y - 16, arena)

        if middle_down == 2 and end_down == 1:
            self.destroy(self._x, self._y + 32, arena)
        if middle_down == 1:
            self.destroy(self._x, self._y + 16, arena)
        
        if middle_left == 2 and end_left == 1:
            self.destroy(self._x - 32, self._y, arena)
        if middle_left == 1:
            self.destroy(self._x - 16, self._y, arena)

        if middle_right == 2 and end_right == 1:
            self.destroy(self._x + 32, self._y, arena)
        if middle_right == 1:
            self.destroy(self._x + 16, self._y, arena)
        
    
    def destroy(self, x, y, arena: Arena):
        for actor in arena.actors():
            if check_collision_coordinate(actor, x, y, self._w, self._h):
                if actor.isDying() == False and isinstance(actor, Bomb) == False:
                    actor.death_animation(5, 0)
                    break

    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h

    def sprite(self) -> Point:
        return self._sprite
    
    def death_animation(self, speed: int, awaiting: int):
        pass
    
    def isDying(self):
        return False