import tkinter as tk
from PIL import Image, ImageTk

import data_unloader
import functions
from data_unloader import cities  # Import city data

# Initialize Tkinter
root = tk.Tk()
root.title("Pandemic Game Map")

# Window size
window_width, window_height = 1550, 800
root.geometry(f"{window_width}x{window_height}")

# Load image
image_path = "../pictures/world_map.png"  # Ensure correct path
pil_image = Image.open(image_path)
img_width, img_height = pil_image.size  # Get image size

# Scale image while maintaining aspect ratio
scale_factor = min(window_width / img_width, window_height / img_height)
new_width = int(img_width * scale_factor)
new_height = int(img_height * scale_factor)
resized_image = pil_image.resize((new_width, new_height), Image.LANCZOS)

# Convert to Tkinter format
map_image = ImageTk.PhotoImage(resized_image)

# Create canvas
canvas = tk.Canvas(root, width=window_width, height=window_height)
canvas.pack(fill="both", expand=True)

# Load the background image
bg_image_path = "../pictures/background_image.png"  # Replace with your actual image file
bg_image = Image.open(bg_image_path)
bg_image = bg_image.resize((window_width, window_height), Image.LANCZOS)
bg_tk_image = ImageTk.PhotoImage(bg_image)

# Place background image on the canvas (fills the whole window)
canvas.create_image(0, 0, anchor=tk.NW, image=bg_tk_image)

# Center image in canvas
x_offset = (window_width - new_width) // 2
y_offset = (window_height - new_height) // 2
canvas.create_image(x_offset, y_offset, anchor=tk.NW, image=map_image)

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
            outline_size = 12  # Slightly larger than the base city marker

            # Draw only the white outline
            marker_id = canvas.create_oval(
                scaled_x - outline_size, scaled_y - outline_size,
                scaled_x + outline_size, scaled_y + outline_size,
                outline="white", width=3
            )

            # Store marker reference
            research_center_markers[city_name] = marker_id

update_research_centers()  # Update UI
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
                bubblesize = 4 + (levels[v] - 1) * 2  # Scale size with infections
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
    popup = tk.Toplevel(root)
    popup.title("Infection Overview")
    popup.geometry("400x400")  # Adjusted size for better readability

    colors = ["Yellow", "Red", "Blue", "Black"]
    tk.Label(popup, text="City Infections by Disease Type", font=("Arial", 12, "bold")).pack(pady=5)

    for v in range(4):  # Loop through colors
        infected_cities = [f"{city} ({data['infection_levels'][v]})" for city, data in cities.items() if data["infection_levels"][v] > 0]

        if infected_cities:  # Only add section if there are infections
            tk.Label(popup, text=f"{colors[v]} Infections:", font=("Arial", 11, "bold"), fg=infection_colors[v]).pack(anchor="w", padx=10, pady=3)
            tk.Label(popup, text=", ".join(infected_cities), font=("Arial", 10), wraplength=350, justify="left").pack(anchor="w", padx=20)

# Create the hover and pop-up button
hover_button = tk.Button(root, text="Show Infections", bg="green3", fg="black")
canvas.create_window(575, 710, window=hover_button)
hover_button.bind("<Button-1>", show_infection_popup)  # Left-click opens popup

# Bind hover events
hover_button.bind("<Enter>", show_infections)
hover_button.bind("<Leave>", hide_infections)

# Store text references
text_elements = {}

def draw_initial_text():
    """Creates the initial text elements on the map."""
    global text_elements
    i = data_unloader.infection_rate_marker  # Infection rate index

    text_elements["infection_rate"] = canvas.create_text(930, 132, text=f"{data_unloader.infection_rate_marker_amount[i]}", font=("Arial", 18, "bold"), fill="black")
    text_elements["research_centers"] = canvas.create_text(1255, 635, text=f" x {data_unloader.research_centers}", font=("Arial", 24, "bold"), fill="black")
    text_elements["infection_yellow"] = canvas.create_text(1255, 671, text=f" x {data_unloader.infection_cubes[0]}", font=("Arial", 18, "bold"), fill="black")
    text_elements["infection_red"] = canvas.create_text(1255, 704, text=f" x {data_unloader.infection_cubes[1]}", font=("Arial", 18, "bold"), fill="black")
    text_elements["infection_blue"] = canvas.create_text(1255, 737, text=f" x {data_unloader.infection_cubes[2]}", font=("Arial", 18, "bold"), fill="black")
    text_elements["infection_black"] = canvas.create_text(1255, 770, text=f" x {data_unloader.infection_cubes[3]}", font=("Arial", 18, "bold"), fill="black")
    text_elements["remaining_actions"] = canvas.create_text(572, 626, text=f" remaining actions: {data_unloader.actions}", font=("Arial", 8, "bold"), fill="black")
    text_elements["hand_size"] = canvas.create_text(572, 645, text=f" hand size: {len(data_unloader.players_hands[0])}", font=("Arial", 8, "bold"), fill="black")
    text_elements["player_deck"] = canvas.create_text(572, 663, text=f" player cards: {len(data_unloader.player_deck)}", font=("Arial", 8, "bold"), fill="black")
    text_elements["player_city"] = canvas.create_text(572, 680, text=f" city: {data_unloader.players_locations[0]}", font=("Arial", 8, "bold"), fill="black")

draw_initial_text()

def update_text(current_player_id):
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
    new_marker = canvas.create_oval(city_x - 5, city_y - 5, city_x + 5, city_y + 5, fill=role_color, outline="black")

    # Store the new marker
    player_markers[player_id] = new_marker


# Initial placement of players
for player_id, (player, city) in enumerate(data_unloader.players_locations.items()):
    update_player_marker(player_id, city)  # Call function to create initial markers

#player hand management
def player_hand_popup():
    """Opens a pop-up window listing the cards in each player's hand."""
    popup2 = tk.Toplevel(root)
    popup2.title("Player Hands")
    popup2.geometry("700x400")  # Adjust window size
    tk.Label(popup2, text="Players' Hands", font=("Arial", 12, "bold")).pack(pady=5)

    # Loop through each player and list their cards
    for player_id, hand in enumerate(data_unloader.players_hands):
        if hand:  # Only show players who have cards
            tk.Label(popup2, text=f"Player {player_id + 1}:", font=("Arial", 11, "bold")).pack(pady=3)
            for card in hand:
                tk.Label(popup2, text=card, font=("Arial", 10)).pack(anchor="center", padx=20)

# Create the button properly
player_button = tk.Button(root, text="Show Player's Hand", command=player_hand_popup, bg="grey30", fg="black", width=24, height=8, font=("Arial", 12, "bold"))
canvas.create_window((1199 * scale_factor) + x_offset, (1056 * scale_factor) + y_offset, window=player_button)

def handle_click(action):
    """Handles button clicks by executing the corresponding action."""
    if action in functions.__dict__:
        functions.__dict__[action]()  # Calls the function dynamically
    else:
        print(f"Action '{action}' not found in functions.")

def setup_buttons(event):
    button_width = 120  # Approximate width of the buttons
    button_height = 20  # Approximate height of the buttons

    buttons = [
        ("Drive/Ferry", 440, 625, "drive_ferry"),
        ("Direct Flight", 440, 647, "direct_flight"),
        ("Charter Flight", 440, 669, "charter_flight"),
        ("Shuttle Flight", 440, 691, "shuttle_flight"),
        ("Build R.C.", 440, 713, "build_research_center"),
        ("Treat Disease", 440, 735, "treat_disease"),
        ("Share Knowledge", 440, 757, "share_knowledge"),
        ("Discover Cure", 440, 779, "discover_cure"),
        ("Play Event Card", 573, 774, "play_event_card")
    ]

    for text, x, y, action in buttons:
        button = tk.Button(root, text=text, font=("Arial", 8), bg="grey30", fg="black",
                           command=lambda a=action: handle_click(a))
        button.place(x=4 + x - button_width // 2, y=y - button_height // 2, width=button_width, height=button_height)

setup_buttons(canvas)

def setup_skip_turn_button(event):
    skip_button = tk.Button(root, text="Skip Turn", font=("Arial", 8), bg="grey30", fg="black",
                            command=lambda: handle_click("skip_turn"))
    button_width = 120
    button_height = 20
    skip_button.place(x=4 + 573 - button_width // 2, y=744 - button_height // 2, width=button_width, height=button_height)

setup_skip_turn_button(canvas)

outbreak_marker_id = None

def update_outbreak_marker():
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
    outbreak_marker_id = canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="green4", outline="black")

update_outbreak_marker()

cure_markers = [((695 * scale_factor) + x_offset, (1049 * scale_factor) + y_offset),
                ((761 * scale_factor) + x_offset, (1049 * scale_factor) + y_offset),
                ((827 * scale_factor) + x_offset, (1049 * scale_factor) + y_offset),
                ((885 * scale_factor) + x_offset, (1049 * scale_factor) + y_offset)]


def update_disease_status(disease_index):
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
        cure_markers[disease_index][0] - 10, cure_markers[disease_index][1] - 10,
        cure_markers[disease_index][0] + 10, cure_markers[disease_index][1] + 10,
        fill=color, width=2
    )

def initialize_disease_status():
    """Draws all disease status markers at the start of the game."""
    for disease_index in range(4):  # Assuming 4 diseases
        update_disease_status(disease_index)

initialize_disease_status()

# Dictionary to hold loaded images
role_images = {}
portrait_position = ((101 * scale_factor) + x_offset, (1063 * scale_factor) + y_offset+5)

# Variable to store the current portrait
current_portrait = None
current_playerid = None
current_playerturn = None

def load_role_images():
    """Loads all role images into memory."""
    roles = data_unloader.player_roles
    for role in roles:
        try:
            img = Image.open(f"../pictures/{role.lower().replace(' ', '_')}.png")  # Ensure correct file naming
            img = img.resize((100, 140))  # Resize to fit UI
            role_images[role] = ImageTk.PhotoImage(img)

        except Exception as e:
            print(f"Error loading {role}: {e}")

def update_player_portrait(canvas, current_player, iter):
    """Updates the canvas with the current player's role portrait."""
    global current_portrait
    global current_playerid
    global current_playerturn

    if not canvas.winfo_exists():
        print("Error: Canvas does not exist.")
        return
    # Get the player's role
    role = current_player.role if hasattr(current_player, "role") else current_player  # Adjust this based on your data structure
    current_playerturn = current_player
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
    canvas.create_oval((98 * scale_factor+30) + x_offset - 5, (936 * scale_factor) + y_offset - 5,
                       (98 * scale_factor+30) + x_offset + 5, (936 * scale_factor) + y_offset + 5, fill=role_color2, outline="black")

# Load images before displaying them
load_role_images()
#To check if the data is being updated in the cities database
#data_unloader.print_city_data()

# Variable to store the current turn text object
current_game_text = None

def update_game_text(message):
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
        font=("Arial", 10, "bold"),
        fill="black"
    )
# Putting on the player and infection card backs onto the map, with buttons as well
original_image1 = Image.open("../pictures/infection_card_back.png")
resized_image2 = original_image1.resize((original_image1.width + 10, original_image1.height - 5))
original_image2 = Image.open("../pictures/player_card_back.png")
resized_image1 = original_image2.resize((original_image2.width - 25, original_image2.height - 25))

button_background_image2 = ImageTk.PhotoImage(resized_image2)
button_background_image1 = ImageTk.PhotoImage(resized_image1)

# Create buttons with text overlay
button2_action="draw_infection_card"
button2 = tk.Button(
    root,
    image=button_background_image2,
    text="Draw Infection Card",
    compound="center",
    fg="white",
    font=("Arial", 12, "bold"),
    relief="flat",
    command=lambda a=button2_action: handle_click(a)
)

button1_action="draw_player_card"
button1 = tk.Button(
    root,
    image=button_background_image1,
    text="Draw Player Card",
    compound="center",
    fg="white",
    font=("Arial", 12, "bold"),
    relief="flat",
    command=lambda a=button1_action: handle_click(a)
)

# Place buttons at specified coordinates
x_coord2 = (1099 * scale_factor) + x_offset  # x-coordinate for center
y_coord2 = (714 * scale_factor) + y_offset  # y-coordinate for center
x_coord1 = (1282 * scale_factor) + x_offset  # x-coordinate for center
y_coord1 = (200 * scale_factor) + y_offset  # y-coordinate for center

button1.place(x=x_coord2, y=y_coord2, anchor="center")
button2.place(x=x_coord1, y=y_coord1, anchor="center")

if __name__ == "__main__":
    root.mainloop()
