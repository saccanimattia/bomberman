#!/usr/bin/env python3
"""
@author  Michele Tomaiuolo - https://tomamic.github.io/
@license This software is free - https://opensource.org/license/mit
"""

from classes.actor import Arena, check_collision
from classes.bomb import Bomb
from classes.wall import Wall
from classes.bomberman import Bomberman
from classes.ballom import Ballom

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
                arena.spawn(Wall((x, y), "indestructible"))

def create_field():
    for x in range(32, canvas_width - 32, 32):
        for y in range(32, canvas_height - 32, 32):
            arena.spawn(Wall((x, y), "indestructible"))

def insert_destroyable_walls():
    safe_zone_x, safe_zone_y = 0, 0
    safe_zone_size = 64

    for x in range(16, canvas_width - 16, 32):
        for y in range(32, canvas_height - 16, 32):
            if (x < safe_zone_x + safe_zone_size and y < safe_zone_y + safe_zone_size):
                continue
            if randint(0, 1) == 0:
                arena.spawn(Wall((x, y), "destroyable"))

    for x in range(32, canvas_width - 16, 32):
        for y in range(16, canvas_height - 16, 32):
            if (x < safe_zone_x + safe_zone_size and y < safe_zone_y + safe_zone_size):
                continue
            if randint(0, 1) == 0:
                arena.spawn(Wall((x, y), "destroyable"))

    for x in range(16, canvas_width - 16, 32):
        for y in range(16, canvas_height - 16, 32):
            if (x < safe_zone_x + safe_zone_size and y < safe_zone_y + safe_zone_size):
                continue
            if randint(0, 1) == 0:
                arena.spawn(Wall((x, y), "destroyable"))

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
        enemy = Ballom((x, y))
        if isinstance(actor, Wall) and check_collision(enemy, actor):
            return True
    return False


def tick():
    canvas_size = g2d.canvas_size()
    g2d.clear_canvas()
    g2d.set_color((0, 120, 0))
    g2d.draw_rect((0, 0), canvas_size)
    img = "img/bomberman.png"
    for a in arena.actors():
        g2d.draw_image(img, a.pos(), a.sprite(), a.size())
    arena.tick(g2d.current_keys())  # Game logic

def main():
    global arena, g2d
    global canvas_height, canvas_width
    global enemies
    import lib.g2d as g2d  # game classes do not depend on g2d
    canvas_width, canvas_height = 432, 336
    enemies = 5
    arena = Arena((canvas_width, canvas_height))

    create_arena()
    arena.spawn(Bomberman((16, 16)))

    g2d.init_canvas(arena.size())
    g2d.main_loop(tick)

if __name__ == "__main__":
    main()


