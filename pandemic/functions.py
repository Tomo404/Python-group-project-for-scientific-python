from pandemic import world_map_drawer
from pandemic import data_unloader
from typing import Any

# Define global variables to track remaining cards and actions
remaining_player_cards = 2  # The number of player cards to draw (fixed)
remaining_infection_cards = 4  # This depends on the infection rate (can be dynamic)

# Function to reset the card draws at the start of each phase
def reset_card_draws():
    global remaining_player_cards, remaining_infection_cards
    remaining_player_cards = 2  # Reset player card draws (fixed)
    remaining_infection_cards = data_unloader.infection_rate_marker_amount[data_unloader.infection_rate_marker]  # Set infection card draws based on infection rate

def drive_ferry(destination: str) -> None:
    """
    Perform the Drive/Ferry action.

    This action moves the current player to an adjacent city
    without discarding any cards.
    """
    if not world_map_drawer.can_perform_action():
        return

    player_id = world_map_drawer.current_playerturn
    current_city = data_unloader.players_locations[player_id]
    neighbors = data_unloader.cities[current_city]["relations"]

    if destination in neighbors:
        data_unloader.players_locations[player_id] = destination
        world_map_drawer.update_player_marker(player_id, destination)
        world_map_drawer.update_game_text(f"Player {player_id + 1} moved from {current_city} to {destination} via Drive/Ferry.")
    else:
        print(f"Invalid move: {destination} is not adjacent to {current_city}.")

def direct_flight() -> None:
    if world_map_drawer.can_perform_action():
        """Perform the Direct Flight action."""
        if not world_map_drawer.can_perform_action():
            return

        player_id = world_map_drawer.current_playerturn
        hand = data_unloader.players_hands[player_id]

        # Check if player has the city card
        for card in hand:
            if card["name"] == city_name:
                hand.remove(card)  # Discard the card
                data_unloader.players_locations[player_id] = city_name
                world_map_drawer.update_player_marker(player_id, city_name)
                world_map_drawer.update_text(player_id)
                world_map_drawer.update_game_text(f"Player {player_id + 1} flew directly to {city_name}.")
                return

        print(f"You don't have the card for {city_name}!")

def charter_flight() -> None:
    if world_map_drawer.can_perform_action():
        """Perform the Charter Flight action."""
        print("Charter Flight action triggered!")

def shuttle_flight() -> None:
    if world_map_drawer.can_perform_action():
        """Perform the Shuttle Flight action."""
        print("Shuttle Flight action triggered!")

def build_research_center() -> None:
    if world_map_drawer.can_perform_action():
        """Perform the action of building a research center."""
        print("Building a Research Center!")

def treat_disease() -> None:
    if world_map_drawer.can_perform_action():
        """Perform the Treat Disease action."""
        print("Treating disease!")

def share_knowledge() -> None:
    if world_map_drawer.can_perform_action():
        """Perform the Share Knowledge action."""
        print("Sharing knowledge!")

def discover_cure() -> None:
    if world_map_drawer.can_perform_action():
        """Perform the Discover Cure action."""
        print("Discovering cure!")

def play_event_card() -> None:
    if world_map_drawer.can_perform_action():
        """Perform the Play Event Card action."""
        print("Playing an event card!")

def skip_turn() -> None:
    """Skip the current player's turn."""
    if data_unloader.actions != 0:
        data_unloader.actions = 0
        print("Turn skipped!")
        drawing_phase()

def action_phase() -> None:
    """
    Execute the action phase for the given player.

    Args:
        player (Any): The current player object.
    """
    data_unloader.actions = 4
    print("Player X's action phase begins.")
    # TODO: Implement action loop

def drawing_phase() -> None:
    """
    Execute the drawing phase for the current player.
    Draws 2 player cards, handles epidemic logic, and transitions to infection phase.
    """
    import time

    player_id = world_map_drawer.current_playerturn
    hand = data_unloader.players_hands[player_id]

    for _ in range(2):
        if not data_unloader.player_deck:
            print("🔚 Player deck is empty! Game over.")
            world_map_drawer.update_game_text("Game Over – player deck exhausted!")
            return

        card = data_unloader.player_deck.pop(0)
        print(f"🎴 Player {player_id + 1} drew: {card['name']}")

        if card["name"] == "Epidemic":
            print("🧨 Epidemic card drawn!")
            world_map_drawer.update_game_text("Epidemic! Increase, Infect, and Intensify")
            handle_epidemic()
        else:
            hand.append(card)

    # Update text on the map to reflect new hand size
    world_map_drawer.update_text(player_id)
    time.sleep(1.5)  # Small pause for readability
    infection_phase()  # Proceed to infection phase


def infection_phase() -> None:
    """
    Execute the infection phase for the given player.

    Args:
        player (Any): The current player object.
    """
    print("Player X's infection phase begins.")
    # TODO: Skip if prevention card played

def draw_player_card() -> None:
    """Draw a player card for the current player."""
    drawing_phase()

def draw_infection_card() -> None:
    """Draw an infection card for the current player."""
    infection_phase()

# Call this function before transitioning to a new phase
def transition_to_next_phase():
    reset_card_draws()  # Reset the draws for the new phase
    # Additional logic for transitioning phases can go here

def handle_epidemic():
    """
    Handles the effects of an epidemic card:
    1. Increase infection rate
    2. Infect a city with 3 cubes
    3. Intensify (shuffle discard pile and place it on top)
    """
    # 1. Increase infection rate marker
    data_unloader.infection_rate_marker = min(data_unloader.infection_rate_marker + 1, 6)

    # 2. Infect: Draw bottom card from infection deck
    if data_unloader.infections:
        bottom_card = data_unloader.infections.pop(-1)
        city = bottom_card["name"]
        color = bottom_card["color"]
        color_index = ["yellow", "red", "blue", "black"].index(color)

        print(f"☣️ Epidemic in {city}! Adding 3 {color} cubes.")

        current_level = data_unloader.cities[city]["infection_levels"][color_index]
        new_level = min(current_level + 3, 3)
        data_unloader.cities[city]["infection_levels"][color_index] = new_level
        data_unloader.infection_cubes[color_index] -= min(3, 3 - current_level)

        data_unloader.infection_discard.append(bottom_card)
    else:
        print("⚠️ No more infection cards!")

    # 3. Intensify: Shuffle discard pile and place on top
    random.shuffle(data_unloader.infection_discard)
    data_unloader.infections = data_unloader.infection_discard + data_unloader.infections
    data_unloader.infection_discard.clear()

