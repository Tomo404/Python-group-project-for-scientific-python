import tkinter as tk
from tkinter import messagebox

# Mock data
infection_levels = [1, 2, 0, 1]  # yellow, red, blue, black
infection_cubes = [23, 22, 24, 23]
infection_status = [0, 1, 0, 1]  # red and black are cured
player_role = "Medic"  # Try "Scientist" or others
current_city = "London"
player_id = 0

def treat_disease():
    global infection_levels

    # Find which diseases are present
    present_diseases = [(i, level) for i, level in enumerate(infection_levels) if level > 0]

    def perform_treatment(disease_index: int):
        cubes = infection_levels[disease_index]
        disease_color = ["yellow", "red", "blue", "black"][disease_index]
        is_cured = infection_status[disease_index] >= 1

        if player_role == "Medic" and is_cured:
            infection_cubes[disease_index] += cubes
            infection_levels[disease_index] = 0
            message = f"Medic treated ALL {disease_color} cubes in {current_city}."
        else:
            infection_cubes[disease_index] += 1
            infection_levels[disease_index] -= 1
            message = f"Treated 1 {disease_color} cube in {current_city}."

        print(message)
        messagebox.showinfo("Treatment Result", message)
        popup.destroy()

    if not present_diseases:
        messagebox.showinfo("Info", f"No disease to treat in {current_city}.")
        return

    if len(present_diseases) == 1:
        perform_treatment(present_diseases[0][0])
    else:
        # Popup to choose disease
        global popup
        popup = tk.Toplevel(root)
        popup.title("Choose Disease to Treat")
        popup.geometry("300x200")

        tk.Label(popup, text=f"{current_city} has multiple diseases.\nChoose one to treat:").pack(pady=10)

        for index, count in present_diseases:
            color = ["yellow", "red", "blue", "black"][index]
            btn = tk.Button(
                popup,
                text=f"{color.capitalize()} ({count} cubes)",
                command=lambda i=index: perform_treatment(i)
            )
            btn.pack(pady=5)

        popup.grab_set()

# GUI setup
root = tk.Tk()
root.title("Treat Disease Test")
root.geometry("400x200")

tk.Button(root, text="Treat Disease", font=("Arial", 14), command=treat_disease).pack(pady=40)

root.mainloop()
