# Group-project-for-scientific-python
We are coding Pandemic. Keep out.

This project is a simplified version of the boardgame Pandemic. For more information of the actual game, look it up at boardgamegeek.com.

## Explanation:

# variables: city_data, infection_cards and other_cards
These are imported into the main files, and include all informations on:
cities: name, coordinates, infection level, infection color, connections, player amounts, research center
infections: city name, infection color
city cards: name, coordinates, infection color
event cards: name, effect

# pictures
Picture of the game board, the UI and the character roles

# data_unloader
Unloads all the data from txt files to database, puts them in directories for easy access, creates the decks and initializes the game

# world_map_drawer
Draws the map with clickable UI functions, updates whenever an action is done

# functions
Contains all the functions connected to movements and actions, as well as card draw and infection outbreaks, checking for game over conditions

# turn_handler
Manages players' turns and the game overall
