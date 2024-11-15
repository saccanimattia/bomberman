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

def create_arena():
    create_border()
    create_field()
    insert_destroyable_walls()
    spawn_balloms()

def create_border():
    for x in range(0, canvas_width, 16):
        for y in range(0, canvas_height, 16):
            if x == 0 or y == 0 or x == canvas_width - 16 or y == canvas_height - 16:
                arena.spawn(Wall((x, y), "indestructible", False))

def create_field():
    for x in range(32, canvas_width - 32, 32):
        for y in range(32, canvas_height - 32, 32):
            arena.spawn(Wall((x, y), "indestructible", False))

def insert_destroyable_walls():
    safe_zone_x, safe_zone_y = 0, 0
    safe_zone_size = 64

    for x in range(16, canvas_width - 16, 32):
        for y in range(32, canvas_height - 16, 32):
            if (x < safe_zone_x + safe_zone_size and y < safe_zone_y + safe_zone_size):
                continue
            if randint(0, 10) == 0:
                arena.spawn(Wall((x, y), "destroyable", False))

    for x in range(32, canvas_width - 16, 32):
        for y in range(16, canvas_height - 16, 32):
            if (x < safe_zone_x + safe_zone_size and y < safe_zone_y + safe_zone_size):
                continue
            if randint(0, 10) == 0:
                arena.spawn(Wall((x, y), "destroyable", False))

    for x in range(16, canvas_width - 16, 32):
        for y in range(16, canvas_height - 16, 32):
            if (x < safe_zone_x + safe_zone_size and y < safe_zone_y + safe_zone_size):
                continue
            if randint(0, 10) == 0:
                arena.spawn(Wall((x, y), "destroyable", False))

def spawn_balloms():
    x_start_field = 32
    y_start_field = 64
    x_end_field = canvas_width - 16
    y_end_field = canvas_height - 16
    field_width_cells = (x_end_field - x_start_field) // 16
    field_height_cells = (y_end_field - y_start_field) // 16

    for i in range(enemies):
        x = randint(0, field_width_cells - 1) * 16 + x_start_field
        y = randint(0, field_height_cells - 1) * 16 + y_start_field
        is_colliding = is_enemy_colliding(x, y)
        if not is_colliding:
            arena.spawn(Ballom((x, y)))
        else:
            while is_colliding:
                x = randint(0, field_width_cells - 1) * 16 + x_start_field
                y = randint(0, field_height_cells - 1) * 16 + y_start_field
                is_colliding = is_enemy_colliding(x, y)
                if not is_colliding:
                    arena.spawn(Ballom((x, y)))


def is_enemy_colliding(x,y):
    for actor in arena.actors():
        if isinstance(actor, Wall) and check_collision_coordinate(actor, x, y, 16, 16):
            return True
    return False

def is_bomberman_died() -> Bomberman or True:
    for actor in arena.actors():
        if isinstance(actor, Bomberman):
            return actor
        
    return True

def is_bomberman_win():
    bomberman = is_bomberman_died()
    for actor in arena.actors():
        if isinstance(actor, Wall):
            if actor.isDying() == True and actor.is_door() == True:
                if actor.pos() == bomberman.pos():
                    return True
    return False

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


