import lib.g2d as g2d
from classes.bomberman_game_state import BombermanGameState


def tick(state: BombermanGameState):
    """game loop"""
    
    keys = g2d.current_keys()
    
    if state.get_phase() == "start":
        # show starting div
        state.get_info_div().show(0)
        
        if "1" in keys:
            #start game with 1 player
            state.set_phase("level1")
            state.set_players(1)
            state.get_bomberman_gui1().create_arena(1)
        elif "2" in keys:
            #start game with 2 players
            state.set_phase("level1")
            state.set_players(2)
            state.get_bomberman_gui1().create_arena(2)
    
    elif state.get_phase() == "level1":
        #show 1 level
        game = state.get_bomberman_gui1().tick()
        
        if game == False:
            #game over
            state.set_phase("game_over")
            state.set_info_div("game_over")
            state.set_points(state.get_bomberman_gui1().get_points())
            g2d.resize_canvas((info_div_w, info_div_h))
        elif game == True:
            #level finished
            state.set_phase("level1_finished")
            state.set_info_div("level_finished")
            state.set_points(state.get_bomberman_gui1().get_points())
            g2d.resize_canvas((info_div_w, info_div_h))
            
    elif state.get_phase() == "game_over":
        #show game over div
        state.get_info_div().show(state.get_points())
        
        if "Enter" in keys:
            #restart game
            state.set_phase("level1")
            state.get_bomberman_gui1().create_arena(state.get_players())
            
    elif state.get_phase() == "level1_finished":
        #show level finished div
        state.get_info_div().show(state.get_points())
        
        if "Enter" in keys:
            #start level 2
            state.set_phase("level2")
            state.get_bomberman_gui2().create_arena(1)
            state.get_bomberman_gui2().set_points(state.get_points())
            
    elif state.get_phase() == "level2":
        #show level 2
        game = state.get_bomberman_gui2().tick()
        
        if game == False:
            #game over
            state.set_phase("game_over")
            state.set_info_div("game_over")
            state.set_points(state.get_bomberman_gui2().get_points())
            g2d.resize_canvas((info_div_w, info_div_h))
        elif game == True:
            #level finished
            state.set_phase("level2_finished")
            state.set_info_div("level_finished")
            state.set_points(state.get_bomberman_gui2().get_points())
            g2d.resize_canvas((info_div_w, info_div_h))
            
    elif state.get_phase() == "level2_finished":
        #show level finished div
        state.get_info_div().show(state.get_points())
        
        if "Enter" in keys:
            #start level 3
            state.set_phase("level3")
            state.get_bomberman_gui3().create_arena(1)
            state.get_bomberman_gui3().set_points(state.get_points())
            
    elif state.get_phase() == "level3":
        #show level 3
        game = state.get_bomberman_gui3().tick()
        
        if game == False:
            #game over
            state.set_phase("game_over")
            state.set_info_div("game_over")
            state.set_points(state.get_bomberman_gui3().get_points())
            g2d.resize_canvas((info_div_w, info_div_h))
        elif game == True:
            #level finished
            state.set_phase("win")
            state.set_info_div("game_won")
            state.set_points(state.get_bomberman_gui3().get_points())
            g2d.resize_canvas((info_div_w, info_div_h))
            
    elif state.get_phase() == "win":
        #show game won div
        state.get_info_div().show(state.get_points())
        
        if "Enter" in keys:
            #restart game
            state.set_phase("start")
            state.get_bomberman_gui1().create_arena()
            g2d.resize_canvas((info_div_w, info_div_h))
    
def main():
    state = BombermanGameState()
    global info_div_w, info_div_h
    info_div_w, info_div_h = 250, 250
    g2d.init_canvas((info_div_w, info_div_h))
    g2d.main_loop(lambda: tick(state))  # start the game loop

if __name__ == "__main__":
    main() # start the game
