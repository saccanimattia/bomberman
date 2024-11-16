#!/usr/bin/env python3
"""
@author  Michele Tomaiuolo - https://tomamic.github.io/
@license This software is free - https://opensource.org/license/mit
"""

from classes.actor import Arena, check_collision_coordinate, Point
from classes.bomb import Bomb
from classes.wall import Wall
from classes.bomberman import Bomberman
from classes.ballom import Ballom
from classes.bomberman_gui import BombermanGui

from random import randint

def tick():
    bombermanGui.tick()

def main():
    global bombermanGui
    bombermanGui = BombermanGui("easy")
    bombermanGui.create_arena()
    import lib.g2d as g2d
    g2d.main_loop(tick)
    
   

if __name__ == "__main__":
    main()


