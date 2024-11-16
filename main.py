import lib.g2d as g2d
from classes.bomberman_game_state import BombermanGameState


def tick(state: BombermanGameState):
    if state.get_phase() == "start":
        state.get_start().show()
        keys = g2d.current_keys()
        if "Enter" in keys:
            g2d.close_canvas()
            state.set_phase("game")
            state.get_bombermanGui1().create_arena()
    elif state.get_phase() == "game":
        state.get_bombermanGui1().tick()

def main():
    state = BombermanGameState()
    global info_div_w
    info_div_w = 500
    global info_div_h
    info_div_h = 500
    g2d.init_canvas((info_div_w, info_div_h))
    g2d.main_loop(lambda: tick(state))  # Passa lo stato al tick

if __name__ == "__main__":
    main()
