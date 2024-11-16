from classes.actor import Arena, check_collision_coordinate, Point
from classes.bomb import Bomb
from classes.wall import Wall
from classes.bomberman import Bomberman
from classes.ballom import Ballom
from classes.scorer import Scorer
import lib.g2d as g2d

from random import randint

difficulties = {
    "easy": {
        "arena_width": 368,
        "arena_height": 240,
        "scorer_height": 64,
        "time": 5,
        "actor_file_path": "src/actors/easy.txt"
    }, 
    "medium": {
        "arena_width": 496,
        "arena_height": 336,
        "scorer_height": 64,
        "time": 240,
        "actor_file_path": "src/actors/medium.txt"
    },
    "hard": {
        "arena_width": 560,
        "arena_height": 336,
        "scorer_height": 64,
        "time": 300,
        "actor_file_path": "src/actors/high.txt"
    }
}

class BombermanGui:
    def __init__(self, difficulty):
        if difficulty not in difficulties:
            raise ValueError("Invalid difficulty")
        
        self._difficulty = difficulty
        self._arena_width = difficulties[difficulty]["arena_width"]
        self._arena_height = difficulties[difficulty]["arena_height"]
        self._scorer_height = difficulties[difficulty]["scorer_height"]
        self._time = difficulties[difficulty]["time"]
        self._actors_file_path = difficulties[difficulty]["actor_file_path"]
        self._arena = Arena((self._arena_width, self._arena_height))
        self._scorer = Scorer((0,0),(self._arena_width, self._scorer_height), self._time, self._arena)
        
    def create_arena(self):
        
        g2d.init_canvas((self._arena_width, self._arena_height + self._scorer_height))    
        
        self.create_border()
        self.create_field()
        
        self.spawn_actors()
        
        return

    def create_border(self):
        for x in range(0, self._arena_width, 16):
            for y in range(self._scorer_height, (self._arena_height + self._scorer_height), 16):
                if x == 0 or y == self._scorer_height or x == self._arena_width - 16 or y ==  (self._arena_height + self._scorer_height) - 16:
                    self._arena.spawn(Wall((x, y), "indestructible", False))

    def create_field(self):
        for x in range(32, self._arena_width - 32, 32):
            for y in range((self._scorer_height + 32), (self._arena_height + self._scorer_height - 32), 32):
                self._arena.spawn(Wall((x, y), "indestructible", False))
                
    def spawn_actors(self):
        with open(self._actors_file_path, mode='r', encoding='utf-8') as file:
            content = file.read()
            door_index = self.get_door_index(content)
            actors = content.split("\n")
            for i in range(len(actors)):
                if actors[i] == "":
                    continue
                actor = actors[i].split(",")
                
                if actor[0] == "Wall":
                    if door_index == i:
                        self._arena.spawn(Wall((int(actor[1]), ( int(actor[2]) + self._scorer_height )), actor[3], True))
                    else:
                        self._arena.spawn(Wall((int(actor[1]), ( int(actor[2]) + self._scorer_height )), actor[3], False))
                
                elif actor[0] == "Ballom":
                    self._arena.spawn(Ballom((int(actor[1]), ( int(actor[2]) + self._scorer_height ))))
                
                elif actor[0] == "Bomberman":
                    self._arena.spawn(Bomberman((int(actor[1]), ( int(actor[2]) + self._scorer_height ))))
                
    def getArena(self):
        return self._arena
    
    def get_door_index(self, content):
        wall_number = self.get_wall_numbers(content)
        return randint(0, wall_number - 1)
    
    def get_wall_numbers(self, content):
        wall_numbers = 0
        for actor in content.split("\n"):
            if actor == "":
                continue
            actor = actor.split(",")
            if actor[0] == "Wall":
                wall_numbers += 1
        return wall_numbers
    
    def is_bomberman_died(self):
        for actor in self._arena.actors():
            if isinstance(actor, Bomberman):
                return actor   
        return True
    
    def check_win(self):
        bomberman = self.is_bomberman_died()
        
        if isinstance(bomberman, Bomberman) == False:
            return False
        
        for actor in self._arena.actors():
            if isinstance(actor, Wall):
                if actor.is_door() == True and actor.isDying() == True:
                    if actor.pos() == bomberman.pos():
                        self._arena.add_points(1000)
                        return True      
        return False
            
    
    def tick(self):
        g2d.clear_canvas()
        g2d.set_color((0, 120, 0))
        g2d.draw_rect((0, self._scorer_height), (self._arena_width, self._arena_height))
        img = "src/img/bomberman.png"
        for a in self._arena.actors():
            if isinstance(a, Bomb) :
                continue
            g2d.draw_image(img, a.pos(), a.sprite(), a.size())
        keys = g2d.current_keys()
        self._arena.tick(keys)  # Game logic
        if self.is_bomberman_died() == True:
            g2d.set_color((255, 255, 255))
            g2d.draw_rect((0,0), (self._arena_width, (self._arena_height + self._scorer_height)))
            g2d.set_color((255, 0, 0))
            g2d.draw_text("game over", (self._arena_width//2, (self._arena_height + self._scorer_height)//2), 30, "BombermanFont.ttf", "center")
            
        if self.check_win() == True:
            g2d.set_color((255, 255, 255))
            g2d.draw_rect((0,0), (self._arena_width, (self._arena_height + self._scorer_height)))
            g2d.set_color((0, 0, 255))
            g2d.draw_text("hai vinto", (self._arena_width//2, (self._arena_height + self._scorer_height)//2), 30, "BombermanFont.ttf", "center")
            
        if self._scorer.create() == False:
            g2d.set_color((255, 255, 255))
            g2d.draw_rect((0,0), (self._arena_width, (self._arena_height + self._scorer_height)))
            g2d.set_color((255, 0, 0))
            g2d.draw_text("game over", (self._arena_width//2, (self._arena_height + self._scorer_height)//2), 30, "BombermanFont.ttf", "center")