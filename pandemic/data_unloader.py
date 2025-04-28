import json
import random
import os

def load_cities():
    """Loads and formats city data from the file."""
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Then use that to build a path to your data file
    cities_path = os.path.join(BASE_DIR, '../variables/cities_data.txt')

    with open(cities_path, 'r', encoding='utf-8') as file:
        cities_data = json.load(file)

    # Process each city and store it in a structured dictionary
    formatted_cities = {}
    for city in cities_data:
        name = city["name"]  # String
        x, y = city["coordinates"]  # Integers for coordinates
        infection_levels = [0, 0, 0, 0]  # Default infection levels for 4 viruses
        research_center = bool(city["research_center"])  # Convert to Boolean
        player_amount = int(city["player_amount"])  # Integer
        relations = list(city["relations"])  # List of connected cities
        color = city["color"]  # String
        in_game_roles =[]

        # Store structured city data
        formatted_cities[name] = {
            "x": x,
            "y": y,
            "infection_levels": infection_levels,
            "research_center": research_center,
            "player_amount": player_amount,
            "relations": relations,
            "color": color
        }

    return formatted_cities  # Returns a dictionary where keys are city names

cities = load_cities()

# Global variables
infection_cubes = [24, 24, 24, 24]  # Yellow, Red, Blue, Black
research_centers = 5
infection_rate_marker_amount = [2, 2, 2, 3, 3, 4, 4]
infection_rate_marker = 0
infection_status = [0, 0, 0, 0] #0: free, 1: cured, 2: eradicated
actions = 4
outbreak_marker = 0
player_roles = ["Medic", "Scientist", "Operations Expert", "Quarantine Specialist"]

def load_infections():
    """Loads and formats city data from the file."""
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Then use that to build a path to your data file
    infection_cards_path = os.path.join(BASE_DIR, '../variables/infection_cards.txt')

    with open(infection_cards_path, 'r', encoding='utf-8') as file:
        infection_data = json.load(file)

    # Process each city and store it in a structured dictionary
    infection_deck = []
    for infection_card in infection_data:
        infection_deck.append({
            "name": infection_card["name"],
            "color": infection_card["infection_color"]
        })

    random.shuffle(infection_deck)

    return infection_deck  # Returns a dictionary where keys are city names

infections = load_infections()

infection_discard = []  # Discard pile for used infection cards
playercard_discard = []
epidemiccard_discard = []
wwidth = 0
wheight = 0
def set_game_settings():
    """Asks for player count and epidemic cards with validation."""
    global players, epidemic_cards, wwidth, wheight
    if not os.environ.get("READTHEDOCS"):
        while True:
            try:
                wwidth = int(input("Give screenwidth (1000-1600): "))
                wheight = int(input("Give screenheight (600-800): "))
                if 1000<=wwidth<=1600 and 600<=wheight<=800:
                    break
                print("❌ Invalid input! Please enter correct screen dimensions.")
            except ValueError:
                print("❌ Invalid input! Please enter valid numbers.")
            # Validate player count (between 2 and 4)
        while True:
            try:
                players = int(input("How many players? (2-4): "))
                if 2 <= players <= 4:
                    break  # Valid input, exit loop
                print("❌ Invalid input! Please enter a number between 2 and 4.")
            except ValueError:
                print("❌ Invalid input! Please enter a valid number.")

            # Validate epidemic card count (4 to 6)
        while True:
            try:
                epidemic_cards = int(input("Choose difficulty: [easy: 4] [medium: 5] [heroic: 6]: "))
                if 4 <= epidemic_cards <= 6:
                    break
                print("❌ Invalid input! Please enter 4, 5, or 6.")
            except ValueError:
                print("❌ Invalid input! Please enter a valid number.")
    else:
        epidemic_cards = 4 # Set a default value for documentation
        players = 2 # Set a default value for documentation
        wwidth = 1000
        wheight = 600

    print(f"✅ Game settings: {players} players, {epidemic_cards} epidemic cards.")

# Call the function to get user input
set_game_settings()

def draw_initial_infections():
    """Draws the 9 starting infected cities and places down the first infection cubes."""
    global infection_deck, infection_discard, infection_cubes, cities

    # Draw 9 cards and apply infection cube placement
    for i in range(9):
        infection_card = infections.pop(0)  # Remove the first card from the deck
        infection_discard.append(infection_card)  # Move to discard pile

        city_name = infection_card["name"]
        city_color = infection_card["color"]
        color_index = ["yellow", "red", "blue", "black"].index(city_color)  # Find index for infection_cubes list

        # Determine number of cubes based on draw order
        cubes_to_add = 3 if i < 3 else 2 if i < 6 else 1
        infection_cubes[color_index] -= cubes_to_add  # Reduce available cubes

        # Update infection levels in the city data
        if city_name in cities:
            current_infection = cities[city_name]["infection_levels"][color_index]
            new_infection = min(current_infection + cubes_to_add, 3)  # Max infection is 3
            cities[city_name]["infection_levels"][color_index] = new_infection

draw_initial_infections()

epidemic_card = {
    "name": "Epidemic",
    "effect": "Increase, Infect, and Intensify"
}

def load_player_cards():
    """Loads city and event cards from file, adds epidemic cards, and shuffles the player deck."""
    global epidemic_cards  # Access global variable

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Then use that to build a path to your data file
    other_cards_path = os.path.join(BASE_DIR, '../variables/other_cards.txt')

    with open(other_cards_path, 'r', encoding='utf-8') as file:
        cards_data = json.load(file)

    city_cards = []
    event_cards = []

    for card in cards_data:
        if card["cardtype"] == "city_card":
            city_cards.append({
                "name": card["name"],
                "coordinates": tuple(card["coordinates"]),
                "color": card["color"]
            })
        elif card["cardtype"] == "event_card":
            event_cards.append({
                "name": card["name"],
                "effect": card["effect"],
                "active": card["active"]
            })

    # Create the initial player deck (city + event cards)
    player_deck = city_cards + event_cards

    # Shuffle the deck
    random.shuffle(player_deck)

    return player_deck

# Example Usage
player_deck = load_player_cards()
players_hands = []  # Stores each player's starting cards

def deal_starting_hands():
    """Deals starting player cards before adding epidemic cards."""
    global players_hands, player_deck, players

    # Determine cards per player
    cards_per_player = {2: 4, 3: 3, 4: 2}[players]

    # Create empty hands for each player
    players_hands = [[] for _ in range(players)]

    # Deal cards
    for _ in range(cards_per_player):
        for player in range(players):
            if player_deck:  # Ensure deck isn't empty
                card = player_deck.pop(0)  # Take from top of deck
                players_hands[player].append(card)

deal_starting_hands()  # Give players their starting hands
current_hand = []

def assign_player_roles():
    """Randomly assigns unique roles to players and stores them in `in_game_roles`."""
    global players_hands, players, player_roles, in_game_roles

    in_game_roles = random.sample(player_roles, players)  # Pick unique roles

    return in_game_roles  # Use this list throughout the game

in_game_roles = assign_player_roles()

def finalize_player_deck():
    """Adds epidemic cards and shuffles the remaining deck."""
    global player_deck, epidemic_cards

    # Add epidemic cards
    for _ in range(epidemic_cards):
        player_deck.append(epidemic_card)

    # Shuffle deck
    random.shuffle(player_deck)

    print("\n✅ Player deck is finalized and shuffled.")

finalize_player_deck()  # Add epidemic cards and shuffle

players_locations = {i: "Atlanta" for i in range(players)}

if "Atlanta" in cities:
    cities["Atlanta"]["player_amount"] = players
