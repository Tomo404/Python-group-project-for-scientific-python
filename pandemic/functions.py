from pandemic import world_map_drawer
from pandemic import data_unloader
from typing import Any
import tkinter as tk
from tkinter import messagebox
from functools import partial
import random
import os
import sys

BUILDING_DOCS = os.environ.get("READTHEDOCS") == "True" or "sphinx" in sys.modules
# Define global variables to track remaining cards and actions
remaining_player_cards = 2  # The number of player cards to draw (fixed)
remaining_infection_cards = 2  # This depends on the infection rate (can be dynamic)
game_over = False # A variable signalling game over

if not BUILDING_DOCS:
    def discard(player_id, amount_to_discard, purpose):
        # Get the current player's hand
        player_hand = data_unloader.players_hands[player_id]
        selected_cards = []

        def submit_selection():
            nonlocal selected_cards
            # Gather the cards selected by the player (checkboxes)
            selected_cards = [card for name, (var, card) in card_vars.items() if var.get() == 1]

            # Check if the selected amount is correct
            if len(selected_cards) != amount_to_discard:
                messagebox.showerror("Invalid Selection", f"Please select exactly {amount_to_discard} card(s).")
                return

            # ===================== Purpose-specific validation =====================
            if purpose == "discover_cure":
                # For discovering a cure, all selected cards must be the same color
                colors = [data_unloader.city_colors[card] for card in selected_cards]
                if len(set(colors)) != 1:
                    messagebox.showerror("Invalid Selection", "You must select cards of the same color to discover a cure.")
                    return

            elif purpose == "direct_flight":
                # You must discard the card of the city you are flying to
                destination_card = selected_cards[0]
                current_city = data_unloader.players_locations[player_id]
                if destination_card["name"] not in data_unloader.cities or destination_card["name"] == current_city:
                    messagebox.showerror("Invalid Selection", f"You must discard a destination city card.")
                    return

            elif purpose == "charter_flight":
                # You must discard the card of the city you are currently in
                destination_card = selected_cards[0]
                current_city = data_unloader.players_locations[player_id]
                if destination_card["name"] != current_city:
                    messagebox.showerror("Invalid Selection", f"You must discard the current city card: {current_city}.")
                    return

                # Show a popup to select the destination city
                def choose_charter_destination():
                    dest_popup = tk.Toplevel()
                    dest_popup.title("Select Destination City")
                    dest_popup.geometry("400x300")

                    tk.Label(dest_popup, text="Choose a destination city:").pack(pady=10)

                    city_var = tk.StringVar(value=list(data_unloader.cities.keys())[0])  # default to the first city
                    city_menu = tk.OptionMenu(dest_popup, city_var, *data_unloader.cities.keys())
                    city_menu.pack(pady=10)

                    def confirm_destination():
                        destination = city_var.get()
                        messagebox.showinfo("Charter Flight", f"You will fly to {destination}.")
                        # Optionally move the player here, or return value for game logic
                        dest_popup.destroy()

                    tk.Button(dest_popup, text="Confirm", command=confirm_destination).pack(pady=10)
                    dest_popup.grab_set()
                    dest_popup.wait_window()

                choose_charter_destination()

            elif purpose == "build_research_center":
                current_city = data_unloader.players_locations[player_id]

                selected_card = selected_cards[0]

                if selected_card["name"] not in data_unloader.cities:
                    messagebox.showerror("Invalid Card", "You must discard a city card to build a research center.")
                    return

                if selected_card["name"] != current_city:
                    messagebox.showerror("Wrong City",
                                         f"You can only build a research center in your current city: {current_city}.")
                    return

                if data_unloader.cities[current_city]["research"] == 1:
                    messagebox.showinfo("Already Present", f"There is already a research center in {current_city}.")
                    return

                # Count total research centers
                total_research_centers = sum(city_data["research"] for city_data in data_unloader.cities.values())

                if total_research_centers >= 6:
                    # Let player choose one to remove
                    other_cities = [name for name, data in data_unloader.cities.items()
                                    if data["research"] == 1 and name != current_city]

                    def choose_research_center_to_remove():
                        select_popup = tk.Toplevel()
                        select_popup.title("Remove a Research Center")
                        select_popup.geometry("400x300")

                        tk.Label(select_popup, text="Choose a city to remove its research center:").pack(pady=10)

                        removable_city = tk.StringVar(value=other_cities[0])
                        city_menu = tk.OptionMenu(select_popup, removable_city, *other_cities)
                        city_menu.pack(pady=10)

                        def confirm_removal():
                            chosen_city = removable_city.get()
                            data_unloader.cities[chosen_city]["research"] = 0
                            data_unloader.cities[current_city]["research"] = 1
                            messagebox.showinfo("Moved", f"Moved research center from {chosen_city} to {current_city}.")
                            select_popup.destroy()

                        tk.Button(select_popup, text="Confirm", command=confirm_removal).pack(pady=10)
                        select_popup.grab_set()
                        select_popup.wait_window()

                    choose_research_center_to_remove()
                else:
                    # Add research center normally
                    data_unloader.cities[current_city]["research"] = 1
                    messagebox.showinfo("Built", f"Research center built in {current_city}.")

            elif purpose == "card_overflow":
                # No validation needed; player is just discarding any cards to reduce hand to 7
                pass

            # ===================== Apply Discard =====================
            for card in selected_cards:
                player_hand.remove(card)
                data_unloader.playercard_discard.append(card)

            # Update the player's hand in the global data structure
            data_unloader.players_hands[player_id] = player_hand

            # Close the discard popup
            popup.destroy()

        # ===================== Create Discard Popup =====================
        popup = tk.Toplevel()
        popup.title(f"Discard Cards ({purpose.replace('_', ' ').title()})")
        popup.geometry("800x400")
        popup.resizable(False, False)

        # Instruction label
        tk.Label(popup, text=f"Select {amount_to_discard} card(s) to discard:").pack(pady=10)

        # Dictionary to keep track of checkboxes
        card_vars = {}
        for card in player_hand:
            var = tk.IntVar()
            cb = tk.Checkbutton(popup, text=card, variable=var)
            cb.pack(anchor="w")
            card_vars[card["name"]] = (var, card)

        # Submit/discard button
        submit_btn = tk.Button(popup, text="Discard", command=submit_selection)
        submit_btn.pack(pady=20)
        popup.grab_set()  # Makes the popup modal — locks focus
        popup.wait_window()  # Waits until popup is destroyed before continuing

def check_game_over(): #checks if one of the game over requirements is met: 3 losing and 1 winning situation
    global game_over
    if len(data_unloader.player_deck) < 2: # We lose if the player deck runs out of cards
        game_over = True
        world_map_drawer.update_game_text("Game Over! Ran out of player cards!")
        return True
    elif data_unloader.outbreak_marker == 8: # We lose if 8 or more outbreaks occur
        game_over = True
        world_map_drawer.update_game_text("Game Over! Too many outbreaks occurred!")
        return True
    elif any(cube < 0 for cube in data_unloader.infection_cubes): # We lose if we can't place infection cubes
        game_over = True
        world_map_drawer.update_game_text("Game Over! Ran out of infection cubes!")
        return True
    elif all(status > 0 for status in data_unloader.infection_status): # We win if all diseases are cured
        game_over = True
        world_map_drawer.update_game_text("You've successfully cured all diseases!")
        return True
    return False

# Function to reset the card draws at the start of each phase
def reset_card_draws():
    global remaining_player_cards, remaining_infection_cards
    remaining_player_cards = 2  # Reset player card draws (fixed)
    remaining_infection_cards = data_unloader.infection_rate_marker_amount[data_unloader.infection_rate_marker]  # Set infection card draws based on infection rate
    data_unloader.actions = 4

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


def direct_flight(player_id) -> None:
    """Perform the Direct Flight action by discarding a city card."""
    if world_map_drawer.can_perform_action():
        discard(player_id, 1, "direct_flight")

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

def charter_flight(player_id) -> None:
    if world_map_drawer.can_perform_action():
        """Perform the Charter Flight action."""
        print("Charter Flight action triggered!")
        discard(player_id, 1, "charter_flight")

def shuttle_flight() -> None:
    if world_map_drawer.can_perform_action():
        """Perform the Shuttle Flight action."""
        world_map_drawer.setup_shuttle_flight_popup()


def build_research_center(player_id) -> None:
    if world_map_drawer.can_perform_action():
        """Perform the action of building a research center."""
        print("Building a Research Center!")
        discard(player_id, 1, "build_research_center")

def treat_disease() -> None:
    if not world_map_drawer.can_perform_action():
        return

    import tkinter as tk
    from tkinter import messagebox

    player_id = world_map_drawer.current_playerturn
    current_city = data_unloader.players_locations[player_id]
    infection_levels = data_unloader.cities[current_city]["infection_levels"]
    role = data_unloader.in_game_roles[player_id]

    # Find which diseases are present
    present_diseases = [(i, level) for i, level in enumerate(infection_levels) if level > 0]

    if not present_diseases:
        world_map_drawer.update_game_text(f"No disease to treat in {current_city}.")
        return

    def perform_treatment(disease_index: int):
        cubes = infection_levels[disease_index]
        disease_color = ["yellow", "red", "blue", "black"][disease_index]
        is_cured = data_unloader.infection_status[disease_index] >= 1

        if role == "Medic" and is_cured:
            # Remove all cubes of that disease
            data_unloader.infection_cubes[disease_index] += cubes
            data_unloader.cities[current_city]["infection_levels"][disease_index] = 0
            message = f"Player {player_id + 1} (Medic) treated all {disease_color} cubes in {current_city}."
        else:
            # Remove one cube
            data_unloader.infection_cubes[disease_index] += 1
            data_unloader.cities[current_city]["infection_levels"][disease_index] -= 1
            message = f"Player {player_id + 1} treated 1 {disease_color} cube in {current_city}."

        world_map_drawer.update_game_text(message)
        world_map_drawer.update_text(player_id)
        popup.destroy()

    if len(present_diseases) == 1:
        # Only one disease present: treat automatically
        perform_treatment(present_diseases[0][0])
    else:
        # Multiple diseases present: show popup to choose
        popup = tk.Toplevel(world_map_drawer.root)
        popup.title("Choose Disease to Treat")
        popup.geometry("300x200")

        tk.Label(popup, text=f"{current_city} has multiple diseases. Choose one to treat:").pack(pady=10)

        for index, count in present_diseases:
            color = ["yellow", "red", "blue", "black"][index]
            btn = tk.Button(
                popup,
                text=f"{color.capitalize()} ({count} cubes)",
                command=lambda i=index: perform_treatment(i)
            )
            btn.pack(pady=5)

        popup.grab_set()
        popup.wait_window()

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

def drawing_phase() -> None:
    """
    Execute the drawing phase for the current player.
    Draws 2 player cards, handles epidemic logic, and transitions to infection phase.
    """
    import time

    player_id = world_map_drawer.current_playerturn
    hand = data_unloader.players_hands[player_id]

    for _ in range(remaining_player_cards):
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
            # ✅ Remove epidemic card from the game by tracking it explicitly
            data_unloader.epidemiccard_discard.append(card)
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

playercards_drawn = 0
def draw_player_card() -> None:
    """Draw a player card for the current player."""
    global playercards_drawn
    if playercards_drawn<remaining_player_cards:
        drawing_phase()
        playercards_drawn += 1
        print("Drawing playercard!")
    else:
        print("No more cards to draw!")

infectioncards_drawn = 0

def draw_infection_card() -> None:
    """Draw an infection card for the current player."""
    global infectioncards_drawn
    if infectioncards_drawn < remaining_infection_cards:
        infection_phase()
        infectioncards_drawn += 1
        print("Drawing infectioncard!")
    else:
        print("End of turn!")
        transition_to_next_phase()

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
