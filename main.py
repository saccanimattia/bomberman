#!/usr/bin/env python3
"""
@author  Michele Tomaiuolo - https://tomamic.github.io/
@license This software is free - https://opensource.org/license/mit
"""

from classes.actor import Arena
from classes.wall import Wall
from classes.bomberman import Bomberman
from classes.ballom import Ballom

def create_arena():
    create_border()
    create_field()

def create_border():
    for x in range(0, 496, 16):
        arena.spawn(Wall((x, 0)))
        arena.spawn(Wall((x, 360)))
    for y in range(16, 360, 16):
        arena.spawn(Wall((0, y)))
        arena.spawn(Wall((480, y)))

def create_field():
    for x in range(canvas_width):
        for y in range(canvas_height):
            if x % 32 == 0 and y % 32 == 0:
                arena.spawn(Wall((x, y)))


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
    import lib.g2d as g2d  # game classes do not depend on g2d
    canvas_width, canvas_height = 496, 376
    arena = Arena((canvas_width, canvas_height))

    create_arena()

    arena.spawn(Bomberman((240, 160)))

    g2d.init_canvas(arena.size())
    g2d.main_loop(tick)

if __name__ == "__main__":
    main()


