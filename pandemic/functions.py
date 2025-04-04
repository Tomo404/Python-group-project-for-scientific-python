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

def drive_ferry() -> None:
    if world_map_drawer.can_perform_action():
        """Perform the Drive/Ferry action."""
        print("Drive/Ferry action triggered!")

def direct_flight() -> None:
    if world_map_drawer.can_perform_action():
        """Perform the Direct Flight action."""
        print("Direct Flight action triggered!")

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

def action_phase(player: Any) -> None:
    """
    Execute the action phase for the given player.

    Args:
        player (Any): The current player object.
    """
    data_unloader.actions = 4
    print("Player X's action phase begins.")
    # TODO: Implement action loop

def drawing_phase(player: Any) -> None:
    """
    Execute the drawing phase for the given player.

    Args:
        player (Any): The current player object.
    """
    print("Player X's drawing phase begins.")
    # TODO: Handle drawing logic and epidemic card

def infection_phase(player: Any) -> None:
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
