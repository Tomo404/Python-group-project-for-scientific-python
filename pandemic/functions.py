import world_map_drawer

def drive_ferry():
    print("Drive/Ferry action triggered!")

def direct_flight():
    print("Direct Flight action triggered!")

def charter_flight():
    print("Charter Flight action triggered!")

def shuttle_flight():
    print("Shuttle Flight action triggered!")

def build_research_center():
    print("Building a Research Center!")

def treat_disease():
    print("Treating disease!")

def share_knowledge():
    print("Sharing knowledge!")

def discover_cure():
    print("Discovering cure!")

def play_event_card():
    print("Playing an event card!")

def skip_turn():
    print("Turn skipped!")

def action_phase(player):
    print("Player X's action phase begins.")
    #for n in actions:
    #blablabla
    #n += 1

def drawing_phase(player):
    print("Player X's drawing phase begins.")
    #if card == epidemic
    #showtime

def infection_phase(player):
    #if infection_phase preventing card was played, skip this
    print("Player X's infection phase begins.")

def draw_player_card():
    drawing_phase(world_map_drawer.current_playerturn)

def draw_infection_card():
    infection_phase(world_map_drawer.current_playerturn)