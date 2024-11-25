#imports
from classes.actor import Arena, Point
from classes.bomb import Bomb
from classes.wall import Wall
from classes.bomberman import Bomberman
from classes.ballom import Ballom
from classes.scorer import Scorer
from classes.powerup import Powerup
import lib.g2d as g2d

from random import randint

# constants

DIFFICULTIES = {
    "easy": {
        "arena_width": 368,
        "arena_height": 240,
        "scorer_height": 64,
        "time": 180,
        "actor_file_path": "src/actors/easy.txt"
    }, 
    "medium": {
        "arena_width": 400,
        "arena_height": 240,
        "scorer_height": 64,
        "time": 240,
        "actor_file_path": "src/actors/medium.txt"
    },
    "hard": {
        "arena_width": 432,
        "arena_height": 272,
        "scorer_height": 64,
        "time": 300,
        "actor_file_path": "src/actors/high.txt"
    }
}

IMG = "src/img/bomberman.png"

# class
class BombermanGui:
    
    def __init__(self, difficulty):
        
        if difficulty not in DIFFICULTIES:
            raise ValueError("Invalid difficulty")

        # initialized attributes with predefined settings
        
        self._difficulty = difficulty
        self._arena_width = DIFFICULTIES[difficulty]["arena_width"]
        self._arena_height = DIFFICULTIES[difficulty]["arena_height"]
        self._scorer_height = DIFFICULTIES[difficulty]["scorer_height"]
        self._time = DIFFICULTIES[difficulty]["time"]
        self._actors_file_path = DIFFICULTIES[difficulty]["actor_file_path"]
        
        # initialized game objects
        
        self._arena = Arena((self._arena_width, self._arena_height))
        self._scorer = Scorer((0,0),(self._arena_width, self._scorer_height), self._time, self._arena)
        
    def create_arena(self, players, scale):
        """create the arena with the given number of players"""
        
        # reset the arena and scorer in case of a restart
        
        self._arena.reset()
        self._scorer.reset()
        
        g2d.resize_canvas((self._arena_width, self._arena_height + self._scorer_height), scale)
        
        # create the field and spawn the actors
        self.create_border()
        self.create_field()
        self.spawn_actors()
        
        # spawn the second bomberman if there are two players
        if players == 2:
            self._arena.spawn(Bomberman((self._arena_width - 32, (self._arena_height + self._scorer_height) - 32), "second"))
        
        return self._arena.actors()

    def create_border(self):
        """create the border of the arena"""
        
        for x in range(0, self._arena_width, 16):
            for y in range(self._scorer_height, (self._arena_height + self._scorer_height), 16):
                if x == 0 or y == self._scorer_height or x == self._arena_width - 16 or y ==  (self._arena_height + self._scorer_height) - 16:
                    self._arena.spawn(Wall((x, y), "indestructible", False))

    def create_field(self):
        """create the field of the arena"""
        
        for x in range(32, self._arena_width - 32, 32):
            for y in range((self._scorer_height + 32), (self._arena_height + self._scorer_height - 32), 32):
                self._arena.spawn(Wall((x, y), "indestructible", False))
                
    def spawn_actors(self):
        """spawn the actors from the actors file"""
        
        #read the actors file and spawn the actors
        with open(self._actors_file_path, mode='r', encoding='utf-8') as file:
            
            content = file.read()
            
            #get the door index
            door_index = self.get_door_index(content)
            
            actors = content.split("\n")
            for i in range(len(actors)):
                
                #continue if the line is empty
                if actors[i] == "":
                    continue
                actor = actors[i].split(",")
                
                #spawn wall and door
                if actor[0] == "Wall":
                    if door_index == i:
                        self._arena.spawn(Wall((int(actor[1]), ( int(actor[2]) + self._scorer_height )), actor[3], True))
                    else:
                        self._arena.spawn(Wall((int(actor[1]), ( int(actor[2]) + self._scorer_height )), actor[3], False))
                
                #spawn bomberman and ballom
                elif actor[0] == "Ballom":
                    self._arena.spawn(Ballom((int(actor[1]), ( int(actor[2]) + self._scorer_height )), actor[3]))
                
                elif actor[0] == "Bomberman":
                    self._arena.spawn(Bomberman((int(actor[1]), ( int(actor[2]) + self._scorer_height)), "first"))
    
    def get_door_index(self, content):
        """return the index of the door in the actors file in base of wall number"""
        wall_number = self.get_wall_numbers(content)
        return randint(0, wall_number - 1)
    
    def get_wall_numbers(self, content):
        """return the number of walls in the actors file"""
        wall_numbers = 0
        for actor in content.split("\n"):
            if actor == "":
                continue
            actor = actor.split(",")
            if actor[0] == "Wall":
                wall_numbers += 1
        return wall_numbers
    
    def is_bomberman_died(self):
        """check if the bomberman object isn't in the arena"""
        for actor in self._arena.actors():
            if isinstance(actor, Bomberman):
                return actor   
        return True
    
    def check_win(self):
        """check if the bomberman reached the door"""
        bomberman = self.is_bomberman_died()
        
        #check if the bomberman object isn't in the arena
        if isinstance(bomberman, Bomberman) == False:
            return False
        
        for actor in self._arena.actors():
            if isinstance(actor, Wall):
                if actor.is_door() == True and actor.is_dying() == True:
                    if actor.pos() == bomberman.pos():
                        self._arena.add_points(500)
                        return True      
        return False

    def _check_powerups(self):
        """check if the bomberman reached a powerup"""
        bomberman = self.is_bomberman_died()
        
        #check if the bomberman object isn't in the arena
        if isinstance(bomberman, Bomberman) == False:
            return
        for actor in self._arena.actors():
            if isinstance(actor, Powerup):
                if actor.pos() == bomberman.pos():
                    actor.death_animation(0,0, Arena)
            
    
    def tick(self):
        """game loop"""
        
        #clear the canvas and draw the actors
        g2d.clear_canvas()
        g2d.set_color((0, 120, 0))
        g2d.draw_rect((0, self._scorer_height), (self._arena_width, self._arena_height))
        for a in self._arena.actors():
            if isinstance(a, Bomb) :
                continue
            g2d.draw_image(IMG, a.pos(), a.sprite(), a.size())

        # Game logic
        keys = g2d.current_keys()
        self._arena.tick(keys)  
        self._check_powerups()

        if self.is_bomberman_died() == True:
            return False
            
        if self.check_win() == True:
           return True
            
        if self._scorer.create() == False:
            return False
        
    def get_points(self):
        """return the points of the arena"""
        return self._arena.get_points()
    
    def set_points(self, points):
        """set the points of the arena"""
        self._arena.add_points(points)
        
    def get_arena(self):
        """return the arena"""
        return self._arena
    
    def get_canvas_size(self):
        """return the size of the arena"""
        return self._arena_width, self._arena_height + self._scorer_height