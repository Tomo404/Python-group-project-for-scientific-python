import tkinter as tk
import data_unloader
import functions
import world_map_drawer
from world_map_drawer import canvas

players = data_unloader.in_game_roles  # List of player roles
game_over = False  # Tracks if the game is over

def check_game_over():
    """Checks if the player deck has fewer than 2 cards, ending the game if true."""
    global game_over  # Ensure we're modifying the global variable
    if len(data_unloader.player_deck) < 2 or data_unloader.outbreak_marker == 8:
        game_over = True
        exit()  # Ends the program

canvas = world_map_drawer.canvas  # Access canvas from world_map_drawer

turn_counter = 0  # Keeps track of turns

"""# TESTING: Move player 1 and 2 (index 0-based) to Miami
test_player_id = 1  # Second player (indexing starts from 0)
data_unloader.players_locations[test_player_id] = "Miami"
test_player_id = 2  # Second player (indexing starts from 0)
data_unloader.players_locations[test_player_id] = "Miami"

# Update UI to reflect the movement
world_map_drawer.update_player_marker(test_player_id, "Miami")"""

while not game_over:
    for player_id, player in enumerate(players):  # Get both player_id and role
        turn_counter = (turn_counter % len(players)) + 1  # Increment turn

        # Update UI elements
        world_map_drawer.update_player_portrait(canvas, player, turn_counter)
        world_map_drawer.update_game_text(f"{player}'s turn")

        # Get the current city of the player
        current_city = data_unloader.players_locations[player_id]

        # Update the player's marker on the map
        world_map_drawer.update_player_marker(player_id, current_city)

        world_map_drawer.root.update()  # Refresh UI

        # Call action, draw, and infection phase functions here
        # functions.action_phase(player_id)
        # functions.drawing_phase(player_id)
        # functions.infection_phase(player_id)

world_map_drawer.root.mainloop()  # Keep Tkinter window open
