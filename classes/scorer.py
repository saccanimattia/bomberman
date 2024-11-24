#imports
from classes.actor import Arena
import lib.g2d as g2d

#constants
FONT = "BombermanFont.ttf"
IMG = "src/img/bomberman.png"

#class
class Scorer:
    def __init__(self, pos, dimension, time, arena: Arena):
        self._type = type
        self._x, self._y = pos
        self._w, self._h = dimension
        self._time = time
        self._start_time = time
        self._arena = arena
        self._counter = 0
        
    def create(self):
        """create the scorer"""
        if self._counter == 30 and self._time > 0:
            self._time -= 1
            self._counter = 0
        self._counter += 1
        g2d.set_color((0, 120, 0))
        g2d.draw_rect((self._x, self._y), (self._w, self._h))
        self.create_borders()
        self.add_time()
        self.add_points()
        if self._time == 0:
            return False
        
        
    def create_borders(self):
        """create the borders of the scorer"""
        for x in range(0, self._w, 16):
            for y in range(0, self._h, 16):
                if x == 0 or y == 0 or x == self._w - 16:
                    g2d.draw_image(IMG, (x, y), (48, 48), (16, 16))
                    
    def add_time(self):
        #adding time to the scorer
        time_string = "time left : " + str(self._time)
        g2d.set_color((176, 176, 176))
        g2d.draw_text(str(time_string), (self._w//4, 32), 16, FONT, "center")
        
    def add_points(self):
        #adding points to the scorer
        points_string = "points : " + str(self._arena.get_points())
        g2d.set_color((176, 176, 176))
        g2d.draw_text(str(points_string), ((self._w//2 + self._w//4), 32), 16, FONT, "center")
    
    def reset(self):
        """reset the scorer"""
        self._time = self._start_time
        self._counter = 0