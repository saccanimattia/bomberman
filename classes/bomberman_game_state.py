from classes.bomberman_gui import BombermanGui
from classes.info_div import InfoDiv

class BombermanGameState:
    def __init__(self):
        self._phase = "start"
        self._bombermanGui1 = BombermanGui("easy")
        self._bombermanGui2 = BombermanGui("medium")
        self._bombermanGui3 = BombermanGui("hard")
        self._start = InfoDiv("start", 500, 500)
        
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
    
    def get_start(self):
        return self._start