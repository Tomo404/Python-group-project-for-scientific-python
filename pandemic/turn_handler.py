from pandemic import data_unloader
from pandemic import functions
from pandemic import world_map_drawer
import os
import sys

BUILDING_DOCS = os.environ.get("READTHEDOCS") == "True" or "sphinx" in sys.modules
if not BUILDING_DOCS:
    root = world_map_drawer.root
players = data_unloader.in_game_roles
current_player_index = world_map_drawer.player_id
game_start = True
game_started = False  # Flag to ensure we only start the game once

def next_turn():
    global current_player_index

    if functions.check_game_over():
        return

    functions.reset_card_draws(player_id=current_player_index)
    player_id = current_player_index
    player_role = players[player_id]
    world_map_drawer.update_player_portrait(world_map_drawer.canvas, player_role, player_id + 1)
    world_map_drawer.update_game_text(f"{player_role}'s turn")
    current_city = data_unloader.players_locations[player_id]
    world_map_drawer.update_player_marker(player_id, current_city)
    current_player_index = (current_player_index + 1) % len(players)
    world_map_drawer.rotate_player_hand(player_id)
    # turn_handler.py — inside next_turn()
    world_map_drawer.current_player_id = player_id
    world_map_drawer.current_playerturn = player_role  # or player_role if your other code expects role

def start_game():
    global game_started
    if game_started:
        return
    game_started = True

    print("🎮 Starting Pandemic...")
    world_map_drawer.create_window()
    world_map_drawer.start_gui(current_player_index, players[current_player_index])

    # 🚨 Do NOT call `next_turn()` here immediately
    # We'll call it AFTER start_gui schedules it
    world_map_drawer.root.mainloop()

def end_game(game_over):
    if game_over:
        root.after(5000, root.destroy)

if __name__ == "__main__":
    start_game()
