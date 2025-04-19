import tkinter as tk
from PIL import Image, ImageTk

from pandemic import data_unloader
from pandemic.data_unloader import cities  # Import city data
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BUILDING_DOCS = os.environ.get("READTHEDOCS") == "True" or "sphinx" in sys.modules
scale_factor = 1
x_offset = 0
y_offset = 0
window_width = data_unloader.wwidth
window_height = data_unloader.wheight

if not BUILDING_DOCS:
    root = tk.Tk()
    canvas = tk.Canvas(root, width=window_width, height=window_height)
    # Load image
    image_path = os.path.join(BASE_DIR, "..", "pictures", "world_map.png")
    pil_image = Image.open(image_path)
    img_width, img_height = pil_image.size  # Get image size
    # Scale image while maintaining aspect ratio
    scale_factor = min(window_width / img_width, window_height / img_height)
    new_width = int(img_width * scale_factor)
    new_height = int(img_height * scale_factor)
    resized_image = pil_image.resize((new_width, new_height), Image.LANCZOS)

    # Load the background image
    bg_image_path = os.path.join(BASE_DIR, "..", "pictures", "background_image.png")
    bg_image = Image.open(bg_image_path)
    bg_image = bg_image.resize((window_width, window_height), Image.LANCZOS)

    x_offset = (window_width - new_width) // 2
    y_offset = (window_height - new_height) // 2
    background_image = None
    map_image = None

def create_window():
    global root, canvas, background_image, map_image
    root.geometry(f"{window_width}x{window_height}")
    root.title("Pandemic Game Map")
    canvas.pack(fill="both", expand=True)

    # Convert to Tkinter format
    bg_tk_image = ImageTk.PhotoImage(bg_image)
    map_image = ImageTk.PhotoImage(resized_image)

    # Prevent garbage collection
    canvas.bg_tk_image = bg_tk_image
    canvas.map_image = map_image

    # Place background image and map on the canvas (fills the whole window)
    canvas.create_image(0, 0, anchor=tk.NW, image=bg_tk_image)
    canvas.create_image(x_offset, y_offset, anchor=tk.NW, image=map_image)

def can_perform_action():
    if data_unloader.actions > 0:
        data_unloader.actions -= 1
        update_text(player_id) # Ensure UI updates
        return True
    else:
        import functions
        print("No remaining actions!")
        functions.skip_turn(player_id)  # Ends turn if actions are exhausted
        return False

# Store references to research center markers
research_center_markers = {}

def update_research_centers():
    """Updates the research center outlines on the map."""
    global research_center_markers

    # Remove previous research center outlines
    for marker in research_center_markers.values():
        canvas.delete(marker)

    research_center_markers.clear()  # Clear stored references

    # Redraw research center outlines
    for city_name, city_data in data_unloader.cities.items():
        if city_data["research_center"]:  # Only draw if there is a research center
            x, y = city_data["x"], city_data["y"]  # Extract coordinates

            # Scale coordinates correctly
            scaled_x = int(x * scale_factor) + x_offset
            scaled_y = int(y * scale_factor) + y_offset

            # Define the outline size
            outline_size = int(16 * scale_factor)  # Slightly larger than the base city marker

            # Draw only the white outline
            marker_id = canvas.create_oval(
                scaled_x - outline_size, scaled_y - outline_size,
                scaled_x + outline_size, scaled_y + outline_size,
                outline="white", width=3
            )

            # Store marker reference
            research_center_markers[city_name] = marker_id

#creating the inspector mode button

# Infection cube colors
infection_colors = ["yellow", "red", "blue", "black"]

# List to store infection markers
infection_markers = []

def show_infections(event):
    """Displays infection markers around each city when hovering."""
    global infection_markers
    infection_markers.clear()  # Clear previous markers

    for city, data in cities.items():
        scale_x = int(data["x"] * scale_factor) + x_offset
        scale_y = int(data["y"] * scale_factor) + y_offset
        levels = data["infection_levels"]  # Infection amounts for each color

        offsets = [(-4, -4), (4, -4), (-4, 4), (4, 4)]  # 4 quarters
        for v in range(4):  # 4 infection types
            for _ in range(levels[v]): # One marker per infection level
                bubblesize = int((4 + (levels[v] - 1) * 2) * scale_factor)  # Scale size with infections
                marker = canvas.create_oval(
                    scale_x + offsets[v][0] - bubblesize, scale_y + offsets[v][1] - bubblesize,
                    scale_x + offsets[v][0] + bubblesize, scale_y + offsets[v][1] + bubblesize,
                    fill=infection_colors[v], outline="green", width = 2
                )
                infection_markers.append(marker)

    canvas.update()  # Force UI update

def hide_infections(event):
    """Hides infection markers when the cursor leaves the button."""
    global infection_markers
    for marker in infection_markers:
        canvas.delete(marker)
    infection_markers.clear()

def show_infection_popup(event):
    """Opens a new pop-up window listing infections grouped by color."""
    if not BUILDING_DOCS:
        popup = tk.Toplevel(root)
        popup.title("Infection Overview")
        popup.geometry("400x600")  # Adjusted size for better readability

        colors = ["Yellow", "Red", "Blue", "Black"]
        tk.Label(popup, text="City Infections by Disease Type", font=("Arial", 12, "bold")).pack(pady=5)

        for v in range(4):  # Loop through colors
            infected_cities = [f"{city} ({data['infection_levels'][v]})" for city, data in cities.items() if data["infection_levels"][v] > 0]

            if infected_cities:  # Only add section if there are infections
                tk.Label(popup, text=f"{colors[v]} Infections:", font=("Arial", 11, "bold"), fg=infection_colors[v]).pack(anchor="w", padx=10, pady=3)
                tk.Label(popup, text=", ".join(infected_cities), font=("Arial", 10), wraplength=350, justify="left").pack(anchor="w", padx=20)

if not BUILDING_DOCS:
    hover_button = tk.Button(root, text="Show Infections", bg="green3", fg="black")
    canvas.create_window(4+(495 * scale_factor) + x_offset, (1070 * scale_factor) + y_offset, window=hover_button, width = 180 * scale_factor, height = 60 * scale_factor)
    hover_button.bind("<Button-1>", show_infection_popup)  # Left-click opens popup

    # Bind hover events
    hover_button.bind("<Enter>", show_infections)
    hover_button.bind("<Leave>", hide_infections)

# Store text references
text_elements = {}

def draw_initial_text():
    if not BUILDING_DOCS:
        """Creates the initial text elements on the map."""
        global text_elements
        i = data_unloader.infection_rate_marker  # Infection rate index

        text_elements["infection_rate"] = canvas.create_text((1034 * scale_factor) + x_offset, (198 * scale_factor) + y_offset, text=f"{data_unloader.infection_rate_marker_amount[i]}", font=("Arial", int(27 * scale_factor), "bold"), fill="black")
        text_elements["research_centers"] = canvas.create_text((1520 * scale_factor) + x_offset, (954 * scale_factor) + y_offset, text=f" x {data_unloader.research_centers}", font=("Arial", int(36 * scale_factor), "bold"), fill="black")
        text_elements["infection_yellow"] = canvas.create_text((1520 * scale_factor) + x_offset, (1004 * scale_factor) + y_offset, text=f" x {data_unloader.infection_cubes[0]}", font=("Arial", int(27 * scale_factor), "bold"), fill="black")
        text_elements["infection_red"] = canvas.create_text((1520 * scale_factor) + x_offset, (1054 * scale_factor) + y_offset, text=f" x {data_unloader.infection_cubes[1]}", font=("Arial", int(27 * scale_factor), "bold"), fill="black")
        text_elements["infection_blue"] = canvas.create_text((1520 * scale_factor) + x_offset, (1104 * scale_factor) + y_offset, text=f" x {data_unloader.infection_cubes[2]}", font=("Arial", int(27 * scale_factor), "bold"), fill="black")
        text_elements["infection_black"] = canvas.create_text((1520 * scale_factor) + x_offset, (1154 * scale_factor) + y_offset, text=f" x {data_unloader.infection_cubes[3]}", font=("Arial", int(27 * scale_factor), "bold"), fill="black")
        text_elements["remaining_actions"] = canvas.create_text((501 * scale_factor) + x_offset, (938 * scale_factor) + y_offset, text=f" remaining actions: {data_unloader.actions}", font=("Arial", int(12 * scale_factor), "bold"), fill="black")
        text_elements["hand_size"] = canvas.create_text((501 * scale_factor) + x_offset, (963 * scale_factor) + y_offset, text=f" hand size: {len(data_unloader.players_hands[0])}", font=("Arial", int(12 * scale_factor), "bold"), fill="black")
        text_elements["player_deck"] = canvas.create_text((501 * scale_factor) + x_offset, (988 * scale_factor) + y_offset, text=f" player cards: {len(data_unloader.player_deck)}", font=("Arial", int(12 * scale_factor), "bold"), fill="black")
        text_elements["player_city"] = canvas.create_text((501 * scale_factor) + x_offset, (1013 * scale_factor) + y_offset, text=f" city: {data_unloader.players_locations[0]}", font=("Arial", int(12 * scale_factor), "bold"), fill="black")

def update_text(current_player_id):
    if not BUILDING_DOCS:
        """Updates the text elements dynamically based on the current player."""
        i = data_unloader.infection_rate_marker  # Get updated infection rate index

        canvas.itemconfig(text_elements["infection_rate"], text=f"{data_unloader.infection_rate_marker_amount[i]}")
        canvas.itemconfig(text_elements["research_centers"], text=f" x {data_unloader.research_centers}")
        canvas.itemconfig(text_elements["infection_yellow"], text=f" x {data_unloader.infection_cubes[0]}")
        canvas.itemconfig(text_elements["infection_red"], text=f" x {data_unloader.infection_cubes[1]}")
        canvas.itemconfig(text_elements["infection_blue"], text=f" x {data_unloader.infection_cubes[2]}")
        canvas.itemconfig(text_elements["infection_black"], text=f" x {data_unloader.infection_cubes[3]}")
        canvas.itemconfig(text_elements["remaining_actions"], text=f" remaining actions: {data_unloader.actions}")
        canvas.itemconfig(text_elements["hand_size"], text=f" hand size: {len(data_unloader.players_hands[current_player_id])}")
        canvas.itemconfig(text_elements["player_deck"], text=f" player cards: {len(data_unloader.player_deck)}")
        canvas.itemconfig(text_elements["player_city"], text=f" city: {data_unloader.players_locations[current_player_id]}")

# Role-to-color mapping
role_colors = {
    "Medic": "chocolate1",
    "Scientist": "gray70",
    "Operations Expert": "lawn green",
    "Quarantine Specialist": "purple2"
}

# Dictionary to store player markers on the map
player_markers = {}

# Function to update player markers when they move
def update_player_marker(player_id, new_city):
    if not BUILDING_DOCS:
        """Moves a player's marker on the map."""
        global player_markers  # Track player markers

        # Get new coordinates
        city_x = data_unloader.cities[new_city]["x"] * scale_factor + x_offset
        city_y = data_unloader.cities[new_city]["y"] * scale_factor + y_offset

        # Get the assigned role color
        player_role = data_unloader.in_game_roles[player_id]
        role_color = role_colors.get(player_role, "pink")  # Default to pink if role not found

        # Remove the old marker if it exists
        if player_id in player_markers:
            canvas.delete(player_markers[player_id])

        # Draw the new marker at the updated location
        new_marker = canvas.create_oval(city_x - int(7.5 * scale_factor), city_y - int(7.5 * scale_factor), city_x + int(7.5 * scale_factor), city_y + int(7.5 * scale_factor), fill=role_color, outline="black")

        # Store the new marker
        player_markers[player_id] = new_marker


# Initial placement of players
for player_id, (player, city) in enumerate(data_unloader.players_locations.items()):
    update_player_marker(player_id, city)  # Call function to create initial markers

#player hand management
def player_hand_popup():
    if not BUILDING_DOCS:
        """Opens a pop-up window listing the cards in each player's hand."""
        popup2 = tk.Toplevel(root)
        popup2.title("Player Hands")
        popup2.geometry("700x400")  # Adjust window size
        tk.Label(popup2, text="Players' Hands", font=("Arial", int(18 * scale_factor), "bold")).pack(pady=5)

        # Loop through each player and list their cards
        for player_id, role in enumerate(data_unloader.in_game_roles):  # or player_roles
            hand = data_unloader.players_hands[player_id]
            if hand:  # Only show players who have cards
                tk.Label(popup2, text=f"Player {player_id + 1}: {role}", font=("Arial", 11, "bold")).pack(pady=3)
                for card in hand:
                    tk.Label(popup2, text=card, font=("Arial", 10)).pack(anchor="center", padx=20)

if not BUILDING_DOCS:
    # Create the button properly
    player_button = tk.Button(root, text="Show Player's Hand", command=player_hand_popup, bg="grey30", fg="black", width=int(36 * scale_factor), height=int(12 * scale_factor), font=("Arial", int(18 * scale_factor), "bold"))
    canvas.create_window((1199 * scale_factor) + x_offset, (1056 * scale_factor) + y_offset, window=player_button)

def handle_click(action):
    """Handles button clicks by executing the corresponding action."""
    from pandemic import functions
    if action in functions.__dict__:
        functions.__dict__[action](current_playerturn)
    elif action in globals():
        globals()[action]()
    else:
        print(f"Action '{action}' not found in functions.")

def setup_buttons(event):
    if not BUILDING_DOCS:
        button_width = 180 * scale_factor  # Approximate width of the buttons
        button_height = 30 * scale_factor  # Approximate height of the buttons

        buttons = [
            ("Drive/Ferry", (295 * scale_factor) + x_offset, (940 * scale_factor) + y_offset, "drive_ferry"),
            ("Direct Flight", (295 * scale_factor) + x_offset, (972 * scale_factor) + y_offset, "direct_flight"),
            ("Charter Flight", (295 * scale_factor) + x_offset, (1004 * scale_factor) + y_offset, "charter_flight"),
            ("Shuttle Flight", (295 * scale_factor) + x_offset, (1036 * scale_factor) + y_offset, "shuttle_flight"),
            ("Build R.C.", (295 * scale_factor) + x_offset, (1068 * scale_factor) + y_offset, "build_research_center"),
            ("Treat Disease", (295 * scale_factor) + x_offset, (1100 * scale_factor) + y_offset, "treat_disease"),
            ("Share Knowledge", (295 * scale_factor) + x_offset, (1132 * scale_factor) + y_offset, "share_knowledge"),
            ("Discover Cure", (295 * scale_factor) + x_offset, (1164 * scale_factor) + y_offset, "discover_cure"),
            ("Play Event Card", (495 * scale_factor) + x_offset, (1164 * scale_factor) + y_offset, "play_event_card")
        ]

        for text, x, y, action in buttons:
            button = tk.Button(root, text=text, font=("Arial", 8), bg="grey30", fg="black",
                               command=lambda a=action: handle_click(a))
            button.place(x=4 + x - button_width // 2, y=y - button_height // 2, width=button_width, height=button_height)

def setup_skip_turn_button(event):
    if not BUILDING_DOCS:
        skip_button = tk.Button(root, text="Skip Turn", font=("Arial", 8), bg="grey30", fg="black",
                                command=lambda: handle_click("skip_turn"))
        button_width = 180 * scale_factor
        button_height = 30 * scale_factor
        x = (495 * scale_factor) + x_offset
        y = (1122 * scale_factor) + y_offset
        skip_button.place(x=4 + x - button_width // 2, y=y - button_height // 2, width=button_width, height=button_height)

outbreak_marker_id = None
outbreak_marker = 0

def update_outbreak_marker():
    if not BUILDING_DOCS:
        """Updates the outbreak marker position when an outbreak occurs."""
        global outbreak_marker, outbreak_marker_id

        # Delete the previous outbreak marker
        if outbreak_marker_id:
            canvas.delete(outbreak_marker_id)

        # Determine the new position
        if outbreak_marker % 2 == 1:
            x, y = (201 * scale_factor) + x_offset, ((548 + outbreak_marker * 36.5) * scale_factor) + y_offset
        elif outbreak_marker % 2 == 0 and outbreak_marker > 0:
            x, y = (157 * scale_factor) + x_offset, ((587 + (outbreak_marker - 1) * 35.5) * scale_factor) + y_offset
        else:
            x, y = (157 * scale_factor) + x_offset, (547 * scale_factor) + y_offset

        # Draw the new outbreak marker and store its ID
        outbreak_marker_id = canvas.create_oval(x - int(7.5 * scale_factor), y - int(7.5 * scale_factor), x + int(7.5 * scale_factor), y + int(7.5 * scale_factor), fill="green4", outline="black")

cure_markers = [((695 * scale_factor) + x_offset, (1049 * scale_factor) + y_offset),
                ((761 * scale_factor) + x_offset, (1049 * scale_factor) + y_offset),
                ((827 * scale_factor) + x_offset, (1049 * scale_factor) + y_offset),
                ((885 * scale_factor) + x_offset, (1049 * scale_factor) + y_offset)]


def update_disease_status(disease_index):
    if not BUILDING_DOCS:
        """Updates the displayed disease status marker for a specific disease."""

        # Determine the new color based on status
        status = data_unloader.infection_status[disease_index]
        if status == 0:
            color = "white"  # Not cured
        elif status == 1:
            color = infection_colors[disease_index]  # Cured
        elif status == 2:
            color = "green"  # Eradicated

        # Draw over the existing marker
        canvas.create_oval(
            cure_markers[disease_index][0] - int(15 * scale_factor), cure_markers[disease_index][1] - int(15 * scale_factor),
            cure_markers[disease_index][0] + int(15 * scale_factor), cure_markers[disease_index][1] + int(15 * scale_factor),
            fill=color, width=2
        )

def initialize_disease_status():
    """Draws all disease status markers at the start of the game."""
    for disease_index in range(4):  # Assuming 4 diseases
        update_disease_status(disease_index)

# Dictionary to hold loaded images
role_images = {}
portrait_position = ((101 * scale_factor) + x_offset, (1063 * scale_factor) + y_offset+5)

# Variable to store the current portrait
current_portrait = None
current_playerid = None
current_playerturn = None

import os

def load_role_images():
    if not BUILDING_DOCS:
        """Loads all role images into memory."""
        roles = data_unloader.player_roles
        for role in roles:
            try:
                filename = f"{role.lower().replace(' ', '_')}.png"
                img_path = os.path.join(os.path.dirname(__file__), "../pictures", filename)

                img = Image.open(img_path)
                img = img.resize((int(150 * scale_factor), int(210 * scale_factor)))  # Resize to fit UI

                role_images[role] = ImageTk.PhotoImage(img)

                # Optional: Prevent garbage collection if you're assigning these to widgets later
                if 'loaded_role_images' not in globals():
                    global loaded_role_images
                    loaded_role_images = {}
                loaded_role_images[role] = role_images[role]

            except Exception as e:
                print(f"[WARNING] Could not load image for {role}: {e}")


def update_player_portrait(canvas, current_player, iter):
    if not BUILDING_DOCS:
        """Updates the canvas with the current player's role portrait."""
        global current_portrait
        global current_playerid
        global current_playerturn

        if not canvas.winfo_exists():
            print("Error: Canvas does not exist.")
            return
        # Get the player's role
        role = current_player.role if hasattr(current_player, "role") else current_player  # Adjust this based on your data structure
        current_playerturn = iter - 1  # Store actual player ID (0, 1, 2...)
        # Remove the previous portrait if it exists
        if current_portrait:
            canvas.delete(current_portrait)
        if current_playerid:
            canvas.delete(current_playerid)

        # Draw the new portrait
        if role in role_images:
            rolex, roley = portrait_position
            current_portrait = canvas.create_image(rolex, roley, image=role_images[role], anchor="center")

        # Get the assigned role for the current player
        role_color2 = role_colors.get(role, "pink")  # Default to gray if role not found

        current_playerid = canvas.create_text((98 * scale_factor) + x_offset, (936 * scale_factor) + y_offset, text=f"Player {iter}", font=("Arial", 8), fill="black")
        canvas.create_oval((98 * scale_factor+30) + x_offset - int(7.5 * scale_factor), (936 * scale_factor) + y_offset - int(7.5 * scale_factor),
                           (98 * scale_factor+30) + x_offset + int(7.5 * scale_factor), (936 * scale_factor) + y_offset + int(7.5 * scale_factor), fill=role_color2, outline="black")

# Load images before displaying them
#To check if the data is being updated in the cities database
#data_unloader.print_city_data()

# Variable to store the current turn text object
current_game_text = None

def update_game_text(message):
    if __name__ == "__main__" or "SPHINX_BUILD" in os.environ:
        """Updates the displayed text to indicate whose turn it is and what they did."""
        global current_game_text  # Allow modification of the global variable

        turn_text_x, turn_text_y = 797 * scale_factor + x_offset, 1129 * scale_factor + y_offset

        # Remove previous turn text (if it exists)
        if current_game_text:
            canvas.delete(current_game_text)

        # Draw the new turn text
        current_game_text = canvas.create_text(
            turn_text_x, turn_text_y,
            text=message,
            font=("Arial", int(15 * scale_factor), "bold"),
            fill="black"
        )

def rotate_player_hand(player_id):
    data_unloader.current_hand = data_unloader.players_hands[player_id]

if not BUILDING_DOCS:
    try:
        # Load and resize infection card image
        infection_img_path = os.path.join(os.path.dirname(__file__), "../pictures/infection_card_back.png")
        player_img_path = os.path.join(os.path.dirname(__file__), "../pictures/player_card_back.png")

        original_infection = Image.open(infection_img_path)
        resized_infection = original_infection.resize((int((original_infection.width + 134) * scale_factor), int((original_infection.height + 76) * scale_factor)))

        original_player = Image.open(player_img_path)
        resized_player = original_player.resize((int((original_player.width + 46) * scale_factor), int((original_player.height + 67) * scale_factor)))

        # Convert to Tk images
        button_background_image2 = ImageTk.PhotoImage(resized_infection)
        button_background_image1 = ImageTk.PhotoImage(resized_player)

        # Create and place buttons
        button2 = tk.Button(
            root,
            image=button_background_image2,
            text="Draw Infection Card",
            compound="center",
            fg="white",
            bg="#44B996",
            activebackground="SystemButtonFace",
            borderwidth=0,
            highlightthickness=0,
            font=("Arial", int(18 * scale_factor), "bold"),
            relief="flat",
            command=lambda: handle_click("draw_infection_card")
        )
        button1 = tk.Button(
            root,
            image=button_background_image1,
            text="Draw Player Card",
            compound="center",
            fg="white",
            bg="#163B66",
            activebackground="SystemButtonFace",
            borderwidth=0,
            highlightthickness=1,
            font=("Arial", int(18 * scale_factor), "bold"),
            relief="flat",
            command=lambda: handle_click("draw_player_card")
        )

        # Place them using offsets and scaling
        x_coord2 = (1099 * scale_factor) + x_offset
        y_coord2 = (714 * scale_factor) + y_offset
        x_coord1 = (1282 * scale_factor) + x_offset
        y_coord1 = (200 * scale_factor) + y_offset

        button1.place(x=x_coord2, y=y_coord2, anchor="center")
        button2.place(x=x_coord1, y=y_coord1, anchor="center")

        # Keep a reference to avoid garbage collection
        root.button_background_image1 = button_background_image1
        root.button_background_image2 = button_background_image2

    except Exception as e:
        print(f"[WARNING] Failed to load button images: {e}")


def start_gui(player_id, player_role):
    create_window()
    update_research_centers()
    draw_initial_text()
    setup_buttons(canvas)
    setup_skip_turn_button(canvas)
    update_outbreak_marker()
    initialize_disease_status()
    load_role_images()
    update_player_portrait(canvas, player_role, player_id + 1)
    rotate_player_hand(player_id)
    from pandemic import turn_handler  # ← avoid circular import early
    root.after(1000, turn_handler.next_turn)

