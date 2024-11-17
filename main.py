import lib.g2d as g2d
from classes.bomberman_game_state import BombermanGameState


def tick(state: BombermanGameState):
    if state.get_phase() == "start":
        state.get_info_div().show(0)
        keys = g2d.current_keys()
        if "1" in keys:
            state.set_phase("level1")
            state.set_players(1)
            state.get_bombermanGui1().create_arena(1)
        elif "2" in keys:
            state.set_phase("level1")
            state.set_players(2)
            state.get_bombermanGui1().create_arena(2)
    elif state.get_phase() == "level1":
        game = state.get_bombermanGui1().tick()
        if game == False:
            state.set_phase("game_over")
            state.set_info_div("game_over")
            state.set_points(state.get_bombermanGui1().get_points())
            g2d.resize_canvas((info_div_w, info_div_h))
        elif game == True:
            state.set_phase("level1_finished")
            state.set_info_div("level_finished")
            state.set_points(state.get_bombermanGui1().get_points())
            g2d.resize_canvas((info_div_w, info_div_h))
    elif state.get_phase() == "game_over":
        keys = g2d.current_keys()
        state.get_info_div().show(state.get_points())
        if "Enter" in keys:
            state.set_phase("level1")
            state.get_bombermanGui1().create_arena(state.get_players())
    elif state.get_phase() == "level1_finished":
        keys = g2d.current_keys()
        state.get_info_div().show(state.get_points())
        if "Enter" in keys:
            state.set_phase("level2")
            state.get_bombermanGui2().create_arena(1)
            state.get_bombermanGui2().set_points(state.get_points())
    elif state.get_phase() == "level2":
        game = state.get_bombermanGui2().tick()
        if game == False:
            state.set_phase("game_over")
            state.set_info_div("game_over")
            state.set_points(state.get_bombermanGui2().get_points())
            g2d.resize_canvas((info_div_w, info_div_h))
        elif game == True:
            state.set_phase("level2_finished")
            state.set_info_div("level_finished")
            state.set_points(state.get_bombermanGui2().get_points())
            g2d.resize_canvas((info_div_w, info_div_h))
    elif state.get_phase() == "level2_finished":
        keys = g2d.current_keys()
        state.get_info_div().show(state.get_points())
        if "Enter" in keys:
            state.set_phase("level3")
            state.get_bombermanGui3().create_arena(1)
            state.get_bombermanGui3().set_points(state.get_points())
    elif state.get_phase() == "level3":
        game = state.get_bombermanGui3().tick()
        if game == False:
            state.set_phase("game_over")
            state.set_info_div("game_over")
            state.set_points(state.get_bombermanGui3().get_points())
            g2d.resize_canvas((info_div_w, info_div_h))
        elif game == True:
            state.set_phase("win")
            state.set_info_div("game_won")
            state.set_points(state.get_bombermanGui3().get_points())
            g2d.resize_canvas((info_div_w, info_div_h))
    elif state.get_phase() == "win":
        keys = g2d.current_keys()
        state.get_info_div().show(state.get_points())
        if "Enter" in keys:
            state.set_phase("start")
            state.get_bombermanGui1().create_arena()
            g2d.resize_canvas((info_div_w, info_div_h))
    
    

def main():
    state = BombermanGameState()
    global info_div_w
    info_div_w = 250
    global info_div_h
    info_div_h = 250
    g2d.init_canvas((info_div_w, info_div_h))
    g2d.main_loop(lambda: tick(state))  # Passa lo stato al tick

if __name__ == "__main__":
    main()
