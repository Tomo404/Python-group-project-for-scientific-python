from pandemic import data_unloader
from pandemic import functions
from pandemic import world_map_drawer
import os
import sys

BUILDING_DOCS = os.environ.get("READTHEDOCS") == "True" or "sphinx" in sys.modules
if not BUILDING_DOCS:
    root = world_map_drawer.root
players = data_unloader.in_game_roles
current_player_index = 0

def check_button_click():
    match True:
        case world_map_drawer.handle_click("drive_ferry"):
            functions.drive_ferry(current_player_index)
        case world_map_drawer.handle_click("direct_flight"):
            functions.direct_flight(current_player_index)
        case world_map_drawer.handle_click("charter_flight"):
            functions.charter_flight(current_player_index)
        case world_map_drawer.handle_click("shuttle_flight"):
            functions.shuttle_flight()
        case world_map_drawer.handle_click("build_research_center"):
            functions.build_research_center(current_player_index)
        case world_map_drawer.handle_click("treat_disease"):
            functions.treat_disease()
        case world_map_drawer.handle_click("share_knowledge"):
            functions.share_knowledge()
        case world_map_drawer.handle_click("discover_cure"):
            functions.discover_cure()
        case world_map_drawer.handle_click("play_event_card"):
            functions.play_event_card()
        case world_map_drawer.handle_click("skip_turn"):
            functions.skip_turn()
        case _:
            print("Unknown button clicked!")

def next_turn():
    global current_player_index
    if functions.check_game_over():
        return

    functions.reset_card_draws()
    player_id = current_player_index
    player_role = players[player_id]
    world_map_drawer.update_player_portrait(world_map_drawer.canvas, player_role, player_id + 1)
    world_map_drawer.update_game_text(f"{player_role}'s turn")
    current_city = data_unloader.players_locations[player_id]
    world_map_drawer.update_player_marker(player_id, current_city)
    current_player_index = (current_player_index + 1) % len(players)
    world_map_drawer.root.after(data_unloader.actions * 10000, next_turn)

### --- ✅ INITIALIZE EVERYTHING --- ###
if not BUILDING_DOCS:
    world_map_drawer.create_window()  # creates root and canvas
    # Draw the background, buttons, cities, infection markers, and portraits

    # Ensure the background image is drawn (make sure world_map_drawer.create_window() does it)
    # If not, call world_map_drawer.draw_map_background() or similar manually

    world_map_drawer.root.after(0, lambda: world_map_drawer.start_gui(next_turn))

    # Start the Tkinter mainloop
    world_map_drawer.root.mainloop()
