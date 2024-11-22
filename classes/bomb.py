#imports
from classes.actor import Actor, Point, Arena, check_collision_coordinate
from classes.powerup import Powerup
from classes.wall import Wall
import lib.g2d as g2d

#constants
TILE = 16
IMG = "src/img/bomberman.png"
BOMB_STEPS = [(0, 48), (16, 48), (32, 48)]
BOMB_EFFECTS = {
    "center": [(32, 96), (112, 96), (32, 176), (112, 176)],
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

#class
class Bomb(Actor):
    
    def __init__(self, pos, spawned_key):
        
        #position
        self._x, self._y = pos
        self._x = self._x // TILE * TILE
        self._y = self._y // TILE * TILE
        self._w, self._h = TILE, TILE
        
        #sprite
        self._bomb_step = 0
        self._bomb_explosion = 0
        self._counter = 0
        self._sprite = BOMB_STEPS[self._bomb_explosion]
        
        #spawned key for check who spawned the bomb
        self._spawned_key = spawned_key
        

    def move(self, arena: Arena):
        
        #bomb explosion animation
        if self._counter % 15 == 0:
            if self._bomb_step > (len(BOMB_STEPS) - 1):
                if self._bomb_explosion < len(BOMB_EFFECTS["center"]):
                    #explosion animation
                    self._sprite = BOMB_EFFECTS["center"][self._bomb_explosion]
                    self._bomb_explosion += 1       
            else:   
                #bomb animation
                self._bomb_step += 1
        self._counter += 1

        #bomb animation
        if self._bomb_step < len(BOMB_STEPS):
            g2d.draw_image(IMG, (self._x, self._y ), BOMB_STEPS[self._bomb_step], (self._w, self._h))
        
        if self._bomb_explosion <= (len(BOMB_EFFECTS["center"]) - 1) and self._bomb_step > (len(BOMB_STEPS) - 1):
            g2d.draw_image(IMG, (self._x, self._y), BOMB_EFFECTS["center"][self._bomb_explosion], (self._w, self._h))
            explosion_collisions = self.get_explosion_collisions(arena)
            self.spawn_explosion(explosion_collisions)
            self.destroy_objects_during_explosion(arena, explosion_collisions)
        
        #destroy walls
        if self._bomb_explosion > (len(BOMB_EFFECTS["center"]) - 1):    
            #destroy objects and bomb
            self.destroy_objects(arena)
            arena.kill(self, -50)


    def spawn_explosion(self, explosion_collisions: dict[str, int]):
        """draw explosion based on the collisions"""
        
        if(explosion_collisions["middle_up"] != "indestructibleWall"):
            g2d.draw_image(IMG, (self._x, self._y - 16), BOMB_EFFECTS["up"]["end"][self._bomb_explosion], (self._w, self._h))
        if(explosion_collisions["middle_up"] == "actor" or explosion_collisions["middle_up"] == "empty"):
            if explosion_collisions["end_up"] != "indestructibleWall":
                g2d.draw_image(IMG, (self._x, self._y - 16), BOMB_EFFECTS["up"]["middle"][self._bomb_explosion], (self._w, self._h))
                g2d.draw_image(IMG, (self._x, self._y - 32), BOMB_EFFECTS["up"]["end"][self._bomb_explosion], (self._w, self._h))

        if(explosion_collisions["middle_down"] != "indestructibleWall"):
            g2d.draw_image(IMG, (self._x, self._y + 16), BOMB_EFFECTS["down"]["end"][self._bomb_explosion], (self._w, self._h))
        if(explosion_collisions["middle_down"] == "actor" or explosion_collisions["middle_down"] == "empty"):
            if explosion_collisions["end_down"] != "indestructibleWall":
                g2d.draw_image(IMG, (self._x, self._y + 16), BOMB_EFFECTS["down"]["middle"][self._bomb_explosion], (self._w, self._h))
                g2d.draw_image(IMG, (self._x, self._y + 32), BOMB_EFFECTS["down"]["end"][self._bomb_explosion], (self._w, self._h))

        if(explosion_collisions["middle_left"] != "indestructibleWall"):
            g2d.draw_image(IMG, (self._x - 16, self._y), BOMB_EFFECTS["left"]["end"][self._bomb_explosion], (self._w, self._h))
        if(explosion_collisions["middle_left"] == "actor" or explosion_collisions["middle_left"] == "empty"):
            if explosion_collisions["end_left"] != "indestructibleWall":
                g2d.draw_image(IMG, (self._x - 16, self._y), BOMB_EFFECTS["left"]["middle"][self._bomb_explosion], (self._w, self._h))
                g2d.draw_image(IMG, (self._x - 32, self._y), BOMB_EFFECTS["left"]["end"][self._bomb_explosion], (self._w, self._h))

        if(explosion_collisions["middle_right"] != "indestructibleWall"):
            g2d.draw_image(IMG, (self._x + 16, self._y), BOMB_EFFECTS["right"]["end"][self._bomb_explosion], (self._w, self._h))
        if(explosion_collisions["middle_right"] == "actor" or explosion_collisions["middle_right"] == "empty"):
            if explosion_collisions["end_right"] != "indestructibleWall":
                g2d.draw_image(IMG, (self._x + 16, self._y), BOMB_EFFECTS["right"]["middle"][self._bomb_explosion], (self._w, self._h))
                g2d.draw_image(IMG, (self._x + 32, self._y), BOMB_EFFECTS["right"]["end"][self._bomb_explosion], (self._w, self._h))
         
        
    def destroy_objects_during_explosion(self, arena: Arena, explosion_collisions: dict[str, int]):
        
        if(explosion_collisions["center"] == "actor"):
            self.destroy(self._x, self._y, arena)

        if(explosion_collisions["middle_up"] == "actor"): 
            self.destroy(self._x, self._y - 16, arena)
        if(explosion_collisions["end_up"] == "actor" and (explosion_collisions["middle_up"] == "actor" or explosion_collisions["middle_up"] == "empty")):
            self.destroy(self._x, self._y - 32, arena)
            
        if(explosion_collisions["middle_down"] == "actor"):
            self.destroy(self._x, self._y + 16, arena)
        if(explosion_collisions["end_down"] == "actor" and (explosion_collisions["middle_down"] == "actor" or explosion_collisions["middle_down"] == "empty")):
            self.destroy(self._x, self._y + 32, arena)
            
        if(explosion_collisions["middle_left"] == "actor"):
            self.destroy(self._x - 16, self._y, arena)
        if(explosion_collisions["end_left"] == "actor" and (explosion_collisions["middle_left"] == "actor" or explosion_collisions["middle_left"] == "empty")):
            self.destroy(self._x - 32, self._y, arena)
                   
        if(explosion_collisions["middle_right"] == "actor"):
            self.destroy(self._x + 16, self._y, arena)
        if(explosion_collisions["end_right"] == "actor" and (explosion_collisions["middle_right"] == "actor" or explosion_collisions["middle_right"] == "empty")):
            self.destroy(self._x + 32, self._y, arena)

    def destroy_objects(self, arena: Arena):
        
        explosion_collisions = self.get_explosion_collisions(arena)
        
        if explosion_collisions["middle_up"] == "empty" and explosion_collisions["end_up"] == "destroyableWall":
            self.destroy(self._x, self._y - 32, arena)
        if explosion_collisions["middle_up"] == "destroyableWall" :
            self.destroy(self._x, self._y - 16, arena)

        if explosion_collisions["middle_down"] == "empty" and explosion_collisions["end_down"] == "destroyableWall":
            self.destroy(self._x, self._y + 32, arena)
        if explosion_collisions["middle_down"] == "destroyableWall":
            self.destroy(self._x, self._y + 16, arena)
        
        if explosion_collisions["middle_left"] == "empty" and explosion_collisions["end_left"] == "destroyableWall":
            self.destroy(self._x - 32, self._y, arena)
        if explosion_collisions["middle_left"] == "destroyableWall":
            self.destroy(self._x - 16, self._y, arena)

        if explosion_collisions["middle_right"] == "empty" and explosion_collisions["end_right"] == "destroyableWall":
            self.destroy(self._x + 32, self._y, arena)
        if explosion_collisions["middle_right"] == "destroyableWall":
            self.destroy(self._x + 16, self._y, arena)
            
    def is_colliding(self, x, y, arena: Arena):
        """check who's colliding with the explosion"""
        for actor in arena.actors():
            if isinstance(actor, Wall) and check_collision_coordinate(actor, x, y, self._w, self._h):
                if actor.getType() == "indestructible":
                    return "indestructibleWall"
                return "destroyableWall"
            elif isinstance(actor, Wall) == False and isinstance(actor, Powerup) == False and isinstance(actor, Bomb) == False and check_collision_coordinate(actor, x, y, self._w, self._h):
                return "actor"
        return "empty"
    
    def get_explosion_collisions(self, arena: Arena):
        
        return {
            "center": self.is_colliding(self._x, self._y, arena),
            "middle_up": self.is_colliding(self._x, self._y - 16, arena),
            "end_up" : self.is_colliding(self._x, self._y - 32, arena),
            "middle_down" : self.is_colliding(self._x, self._y + 16, arena),
            "end_down" : self.is_colliding(self._x, self._y + 32, arena),
            "middle_left" : self.is_colliding(self._x - 16, self._y, arena),
            "end_left" : self.is_colliding(self._x - 32, self._y, arena),
            "middle_right" : self.is_colliding(self._x + 16, self._y, arena),
            "end_right" : self.is_colliding(self._x + 32, self._y, arena)
        }
        
    
    def destroy(self, x, y, arena: Arena):
        for actor in arena.actors():
            if check_collision_coordinate(actor, x, y, self._w, self._h):
                if actor.is_dying() == False and isinstance(actor, Bomb) == False:
                    actor.death_animation(5, 5, arena)
                    break

    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h

    def sprite(self) -> Point:
        return self._sprite
    
    def death_animation(self, speed: int, awaiting: int, arena: Arena):
        pass
    
    def is_dying(self):
        return False
    
    def get_spawned_key(self):
        return self._spawned_key