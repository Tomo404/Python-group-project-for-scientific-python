import data_unloader
import functions
import world_map_drawer
from world_map_drawer import canvas

players = data_unloader.in_game_roles  # List of player roles
game_over = False  # Tracks if the game is over
current_player_index = 0  # Tracks the current player's turn

# checks which button was clicked and calls it accordingly
def check_button_click():
    match True:
        case world_map_drawer.handle_click("drive_ferry"):
            functions.drive_ferry()
        case world_map_drawer.handle_click("direct_flight"):
            functions.direct_flight()
        case world_map_drawer.handle_click("charter_flight"):
            functions.charter_flight()
        case world_map_drawer.handle_click("shuttle_flight"):
            functions.shuttle_flight()
        case world_map_drawer.handle_click("build_research_center"):
            functions.build_research_center()
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

def check_game_over():
    """Checks if the game is over due to player deck depletion or outbreak limit."""
    global game_over
    if len(data_unloader.player_deck) < 2 or data_unloader.outbreak_marker == 8:
        game_over = True
        world_map_drawer.update_game_text("Game Over!")  # Display game over message
        return True  # Indicate that the game is over
    return False

def next_turn():
    """Handles the turn logic and schedules the next turn dynamically."""
    global current_player_index

    if check_game_over():
        return  # Stop if the game is over

    player_id = current_player_index
    player_role = players[player_id]

    # Update UI
    world_map_drawer.update_player_portrait(canvas, player_role, player_id + 1)
    world_map_drawer.update_game_text(f"{player_role}'s turn")

    # Get the current city of the player
    current_city = data_unloader.players_locations[player_id]
    world_map_drawer.update_player_marker(player_id, current_city)

    # Call phases
    # functions.action_phase(player_id)
    # functions.drawing_phase(player_id)
    # functions.infection_phase(player_id)

    # Move to the next player's turn
    current_player_index = (current_player_index + 1) % len(players)

    # Schedule the next turn after a delay (e.g., 1000 ms = 1 second, 1 action ~ 90 seconds)
    world_map_drawer.root.after(data_unloader.actions * 90000, next_turn)

# Start the game loop by calling next_turn once
world_map_drawer.root.after(1000, next_turn)

# Start the Tkinter event loop
world_map_drawer.root.mainloop()
