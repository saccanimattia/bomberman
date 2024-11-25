#import unittest lib to run tests
from unittest import TestCase, main 

#import classes to test
from classes.actor import Arena, check_collision_coordinate
from classes.ballom import Ballom
from classes.bomberman import Bomberman
from classes.bomberman_gui import BombermanGui
from classes.wall import Wall

# import lib to test
from lib import g2d

#constants

DIFFICULTIES = ["easy", "medium", "hard"]

BOMBERMAN_STEPS = {
    "ArrowUp": {
      "sprites" : [(48, 16), (64, 16), (80, 16)],
      "movement": (0, -2)
    },
    "ArrowDown": {
      "sprites" : [(48, 0),(64, 0), (80, 0)],
      "movement": (0, 2)
    },
    "ArrowLeft": {
      "sprites" : [(0, 0), (16, 0), (32, 0)],
      "movement": (-2, 0)
    },
    "ArrowRight": {
      "sprites" : [(0, 16), (16, 16), (32, 16)],
      "movement": (2, 0)
    }
    }


#test class
class Test(TestCase):
  
    def populate_arena(self):
        """populate the arena with different difficulties"""   
        bomberman_guis = []
        for difficulty in DIFFICULTIES:
            bomberman_gui = BombermanGui(difficulty)
            self.assertTrue(bomberman_gui.create_arena(1, 1) != None)
            bomberman_guis.append(bomberman_gui)
        return bomberman_guis
      
    def simulate_death(self, arena: Arena):
        """simulate the death of the bomberman"""
        actors = arena.actors()
        for actor in actors:
            if isinstance(actor, Bomberman):
                actor.death_animation(1, 5, arena)
                break 
              
    def get_door_position(self, arena: Arena):
        """get the door position"""
        actors = arena.actors()
        for actor in actors:
           if isinstance(actor, Wall):
                if actor.is_door() == True:
                    actor.death_animation(1, 5, arena)
                    return actor.pos()
    
    def get_enemy_position(self, arena: Arena):
        """get the first enemy position"""
        actors = arena.actors()
        for actor in actors:
            if isinstance(actor, Ballom):
                return actor.pos()
              
    def make_collision(self, bomberman_gui: BombermanGui, enemy_position):
        """change the bomberman position to the enemy position"""
        actors = bomberman_gui.get_arena().actors()
        for actor in actors:
            if isinstance(actor, Bomberman):
                actor.set_pos(enemy_position[0], enemy_position[1])
                break
    
    def get_bomberman_position(self, bomberman_gui: BombermanGui):  
        """get the bomberman position"""
        actors = bomberman_gui.get_arena().actors()
        for actor in actors:
            if isinstance(actor, Bomberman):
                return actor.pos()
            
    def check_lost(self, bomberman_gui: BombermanGui):
        """check if the bomberman is dead"""
        actors = bomberman_gui.get_arena().actors()
        for actor in actors:
            if isinstance(actor, Bomberman):
                #check if the bomberman is dead by using assertTrue
                self.assertTrue(actor.is_dying() == True)
                break
            
    def check_win(self, bomberman_gui: BombermanGui, door_position):
        """check if the bomberman reached the door"""
        actors = bomberman_gui.get_arena().actors()
        for actor in actors:
            if isinstance(actor, Bomberman):
                actor.set_pos(door_position[0], door_position[1])
                break
        #check if the bomberman reached the door by using assertTrue
        self.assertTrue(bomberman_gui.check_win() == True)
    
    def check_bomberman_steps(self, bomberman_gui: BombermanGui, key, bomberman_position):
        """check if the bomberman steps (sprite, pos) are correct"""
        actors = bomberman_gui.get_arena().actors()
        for actor in actors:
            if isinstance(actor, Bomberman):
                #check if the bomberman sprite is correct by using assertTrue
                self.assertTrue(actor.sprite() in BOMBERMAN_STEPS[key]["sprites"])
                dx, dy = BOMBERMAN_STEPS[key]["movement"]
                x, y = actor.pos()
                #check if the bomberman can move in the direction
                for element in actors:
                    if check_collision_coordinate(element, (x+dx),  (y+dy), 16, 16) and isinstance(element, Wall):
                        dx, dy = 0, 0
                        break   
                #check if the bomberman position is correct by using assertTrue 
                self.assertTrue((x, y) == (bomberman_position[0] + dx, bomberman_position[1] + dy))
                actor.set_pos(bomberman_position[0], bomberman_position[1])  
                break
        
    def test_arena_game_over(self):
        """test if the bomberman is dead"""
        bomberman_guis = self.populate_arena()      
        for bomberman_gui in bomberman_guis:
            canvas_width, canvas_height = bomberman_gui.get_canvas_size()
            g2d.init_canvas((canvas_width, canvas_height))
            self.simulate_death(bomberman_gui.get_arena())
            self.check_lost(bomberman_gui)
    
    def test_arena_win(self):
        """test if the bomberman reached the door"""
        bomberman_guis = self.populate_arena()      
        for bomberman_gui in bomberman_guis:
            canvas_width, canvas_height = bomberman_gui.get_canvas_size()
            g2d.init_canvas((canvas_width, canvas_height))
            door_position = self.get_door_position(bomberman_gui.get_arena())
            self.check_win(bomberman_gui, door_position)
    
    def test_enemies_collisions(self):
        """test if the bomberman collides with an enemy"""
        bomberman_guis = self.populate_arena()       
        for bomberman_gui in bomberman_guis:
            canvas_width, canvas_height = bomberman_gui.get_canvas_size()
            g2d.init_canvas((canvas_width, canvas_height))
            enemy_position = self.get_enemy_position(bomberman_gui.get_arena())
            self.make_collision(bomberman_gui, enemy_position)
            bomberman_gui.tick()
            self.check_lost(bomberman_gui)
            
    def test_bomberman_steps(self):
        """test if the bomberman can move in the arena"""
        bomberman_guis = self.populate_arena()
        for bomberman_gui in bomberman_guis:
            canvas_width, canvas_height = bomberman_gui.get_canvas_size()
            g2d.init_canvas((canvas_width, canvas_height))
            #check position and sprite of the bomberman for every possible direction
            keys = ["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"]
            for key in keys:
                g2d.remove_keys()
                g2d.add_key(key)
                bomberman_position = self.get_bomberman_position(bomberman_gui)
                bomberman_gui.tick()
                self.check_bomberman_steps(bomberman_gui, key, bomberman_position)
     
if __name__ == "__main__":
  main()

