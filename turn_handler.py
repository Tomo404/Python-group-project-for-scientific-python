import tkinter as tk
import data_unloader
import functions
import world_map_drawer
from world_map_drawer import canvas, player_id

players = data_unloader.in_game_roles
game_over = False

def check_game_over():
    """Checks if the player deck has fewer than 2 cards, ending the game if true."""
    if len(data_unloader.player_deck) < 2:
        game_over = True
        exit()  # Ends the program
    elif data_unloader.outbreak_marker == 8:
        game_over = True
        exit()  # Ends the program

canvas = world_map_drawer.canvas
it = 0
while not game_over:
    for player in players:
        it = it % len(players) + 1
        world_map_drawer.update_player_portrait(canvas, player, it)
        world_map_drawer.update_game_text(f"{player}' turn")
        world_map_drawer.root.update()  # Refresh UI
        #print(input("Proceed? "))
        """functions.action_phase(player)
        functions.drawing_phase(player)
        functions.infection_phase(player)"""
        # Call action, draw, and infection phase functions here

world_map_drawer.root.mainloop()