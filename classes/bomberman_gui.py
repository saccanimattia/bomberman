from classes.actor import Arena, check_collision_coordinate, Point
from classes.bomb import Bomb
from classes.wall import Wall
from classes.bomberman import Bomberman
from classes.ballom import Ballom
import lib.g2d as g2d

from random import randint

difficulties = {
    "easy": {
        "arena_width": 432,
        "arena_height": 336,
        "scorer_height": 50,
        "time": 180
    }, 
    "medium": {
        "arena_width": 496,
        "arena_height": 336,
        "scorer_height": 50,
        "time": 240
    },
    "hard": {
        "arena_width": 560,
        "arena_height": 336,
        "scorer_height": 50,
        "time": 300
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
        self._arena = Arena((self._arena_width, self._arena_height))
        
    def create_arena(self):
        
        g2d.init_canvas((self._arena_width, self._arena_height + self._scorer_height))    
        
        self.create_border()
        self.create_field()
        
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
                
    def getArena(self):
        return self._arena
    
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