#!/usr/bin/env python3
"""
@author  Michele Tomaiuolo - https://tomamic.github.io/
@license This software is free - https://opensource.org/license/mit
"""

from classes.actor import Arena
from classes.wall import Wall
from classes.bomberman import Bomberman
from classes.ballom import Ballom


def tick():
    g2d.clear_canvas()
    img = "https://fondinfo.github.io/sprites/bomberman.png"
    for a in arena.actors():
        g2d.draw_image(img, a.pos(), a.sprite(), a.size())

    arena.tick(g2d.current_keys())  # Game logic


def main():
    global arena, g2d
    import lib.g2d as g2d  # game classes do not depend on g2d
    

    arena = Arena((480, 360))
    arena.spawn(Ballom((48, 80)))
    arena.spawn(Ballom((80, 48)))
    arena.spawn(Wall((128, 80)))
    arena.spawn(Bomberman((240, 160)))

    g2d.init_canvas(arena.size())
    g2d.main_loop(tick)

if __name__ == "__main__":
    main()


