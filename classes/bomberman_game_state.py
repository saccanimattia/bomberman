from classes.bomberman_gui import BombermanGui
from classes.info_div import InfoDiv

class BombermanGameState:
    def __init__(self):
        self._phase = "start"
        self._points = 0
        self._players = 1
        self._bombermanGui1 = BombermanGui("easy")
        self._bombermanGui2 = BombermanGui("medium")
        self._bombermanGui3 = BombermanGui("hard")
        self._info_div = InfoDiv("start", 250, 250)
        
    def get_phase(self):
        return self._phase
    
    def set_phase(self, phase):
        self._phase = phase
        
    def get_bombermanGui1(self):
        return self._bombermanGui1
    
    def get_bombermanGui2(self):
        return self._bombermanGui2
    
    def get_bombermanGui3(self):
        return self._bombermanGui3
    
    def get_info_div(self):
        return self._info_div
    
    def set_info_div(self, type):
        self._info_div.set_type(type)
        
    def get_points(self):
        return self._points
    
    def set_points(self, points: int):
        self._points = points
        
    def get_players(self):
        return self._players

    def set_players(self, players: int):
        self._players = players