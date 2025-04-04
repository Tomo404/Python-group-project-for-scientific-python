import world_map_drawer
from typing import Any

def drive_ferry() -> None:
    """Perform the Drive/Ferry action."""
    print("Drive/Ferry action triggered!")

def direct_flight() -> None:
    """Perform the Direct Flight action."""
    print("Direct Flight action triggered!")

def charter_flight() -> None:
    """Perform the Charter Flight action."""
    print("Charter Flight action triggered!")

def shuttle_flight() -> None:
    """Perform the Shuttle Flight action."""
    print("Shuttle Flight action triggered!")

def build_research_center() -> None:
    """Perform the action of building a research center."""
    print("Building a Research Center!")

def treat_disease() -> None:
    """Perform the Treat Disease action."""
    print("Treating disease!")

def share_knowledge() -> None:
    """Perform the Share Knowledge action."""
    print("Sharing knowledge!")

def discover_cure() -> None:
    """Perform the Discover Cure action."""
    print("Discovering cure!")

def play_event_card() -> None:
    """Perform the Play Event Card action."""
    print("Playing an event card!")

def skip_turn() -> None:
    """Skip the current player's turn."""
    print("Turn skipped!")

def action_phase(player: Any) -> None:
    """
    Execute the action phase for the given player.

    Args:
        player (Any): The current player object.
    """
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
    drawing_phase(world_map_drawer.current_playerturn)

def draw_infection_card() -> None:
    """Draw an infection card for the current player."""
    infection_phase(world_map_drawer.current_playerturn)
