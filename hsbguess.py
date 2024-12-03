import tkinter as tk
import random
import colorsys
import os

# Generate a random HSB color
def generate_random_hsb():
    h = random.uniform(0, 360)
    s = random.uniform(10, 100)
    b = random.uniform(10, 100)
    return (h, s, b)

# Convert HSB to RGB
def hsb_to_rgb(h, s, b):
    r, g, bl = colorsys.hsv_to_rgb(h / 360, s / 100, b / 100)
    return int(r * 255), int(g * 255), int(bl * 255)

# Initialize the game_won flag
game_won = False
hint_used = False
# Initialize game records
game_records = []

def is_correct_guess(target, guess, tolerance):
    return all(abs(t - g) <= tolerance for t, g in zip(target, guess))

# Submit guess function
def submit_guess():
    global guess_count, game_won, hint_used
    try:
        h = float(hue_entry.get())
        s = float(sat_entry.get().strip('%'))
        b = float(bri_entry.get().strip('%'))
        guess = (h, s, b)

        hint_label.config(text="")
        
        if not game_won:
            guess_count += 1
            guess_count_label.config(text=f"Number of guesses: {guess_count}")
        
        guessed_rgb = hsb_to_rgb(*guess)
        guessed_color = f'#{guessed_rgb[0]:02x}{guessed_rgb[1]:02x}{guessed_rgb[2]:02x}'
        guess_label.config(bg=guessed_color)
        
        tolerance = tolerance_slider.get()
        if is_correct_guess(target_color, guess, tolerance) or game_won:
            result_label.config(text=f"Correct! The exact color was H: {target_color[0]:.2f}, S: {target_color[1]:.2f}%, B: {target_color[2]:.2f}%\nYou can play around with the values or click 'Next Game' to start a new game.", justify="left")
            next_game_button.pack()  # Show the "Next Game" button
            game_won = True
            update_next_game_button_color()
        else:
            result_label.config(text="Incorrect! Try again.")
    except ValueError:
        result_label.config(text="Please enter valid numbers.")

# Update the next_game_button color to match the target color and ensure text visibility
def update_next_game_button_color():
    target_rgb = hsb_to_rgb(*target_color)
    target_color_hex = f'#{target_rgb[0]:02x}{target_rgb[1]:02x}{target_rgb[2]:02x}'
    next_game_button.config(bg=target_color_hex, fg="white" if sum(target_rgb) < 128 * 3 else "black")

# Call this function when updating the target color
def update_target_color():
    global target_color, target_rgb, target_color_hex, guess_count, game_records, game_won, hint_used
    # Record the number of guesses and hint usage for the previous game
    game_records.append((guess_count, hint_used, target_color))
    update_game_records_label()
    
    target_color = generate_random_hsb()
    target_rgb = hsb_to_rgb(*target_color)
    target_color_hex = f'#{target_rgb[0]:02x}{target_rgb[1]:02x}{target_rgb[2]:02x}'
    target_label.config(bg=target_color_hex)
    result_label.config(text="")
    guess_label.config(bg="white")
    next_game_button.pack_forget()  # Hide the "Next Game" button
    
    # Reset guess count, game_won flag, and hint_used flag for the new game
    guess_count = 0
    guess_count_label.config(text=f"Number of guesses: {guess_count}")
    game_won = False
    hint_used = False

# Update game records label
def update_game_records_label():
    for widget in game_records_label.winfo_children():
        widget.destroy()
    
    tk.Label(game_records_label, text="Game Records:").pack()
    
    for i, (count, hint, color) in enumerate(game_records):
        if not hint:
            target_rgb = hsb_to_rgb(*color)
            target_color_hex = f'#{target_rgb[0]:02x}{target_rgb[1]:02x}{target_rgb[2]:02x}'
            text_color = "white" if sum(target_rgb) < 128 * 3 else "black"
            record_text = f"Game {i+1}: {count} guesses (No hint)"
            tk.Label(game_records_label, text=record_text, bg=target_color_hex, fg=text_color).pack()
        else:
            record_text = f"Game {i+1}: {count} guesses"
            tk.Label(game_records_label, text=record_text).pack()

# Function to provide a hint
def provide_hint():
    global hint_used
    try:
        h = float(hue_entry.get())
        s = float(sat_entry.get().strip('%'))
        b = float(bri_entry.get().strip('%'))
        guess = (h, s, b)
        
        # Calculate cyclic difference for hue
        hue_diff = min(abs(target_color[0] - h), 360 - abs(target_color[0] - h))
        sat_diff = abs(target_color[1] - s)
        bri_diff = abs(target_color[2] - b)
        
        differences = [hue_diff, sat_diff, bri_diff]
        max_diff_index = differences.index(max(differences))
        components = ["Hue", "Saturation", "Brightness"]
        hint_label.config(text=f"Furthest component: {components[max_diff_index]}")
        if not game_won:
            hint_used = True
    except ValueError:
        hint_label.config(text="Please enter valid numbers.")


if __name__ == "__main__":

    basedir = os.path.dirname(__file__)

    # Main UI setup
    root = tk.Tk()
    root.title("HSB Color Guess")
    root.iconbitmap(os.path.join(basedir,'huewheel.ico'))
    root.minsize(500, 0)  # Set a fixed width and allow height to be self-adapted

    target_color = generate_random_hsb()
    target_rgb = hsb_to_rgb(*target_color)
    target_color_hex = f'#{target_rgb[0]:02x}{target_rgb[1]:02x}{target_rgb[2]:02x}'
    guess_count = 0
    game_records = []

    tolerance_frame = tk.Frame(root)
    tolerance_frame.pack()

    tk.Label(tolerance_frame, text="Tolerance for correct guess:").pack(side=tk.LEFT)
    tolerance_slider = tk.Scale(tolerance_frame, from_=1, to_=10, orient=tk.HORIZONTAL)
    tolerance_slider.set(10)  # Default tolerance value
    tolerance_slider.pack(side=tk.LEFT, padx=10)

    frame = tk.Frame(root)
    frame.pack()

    tk.Label(frame, text="Target Color:").grid(row=0, column=0)
    target_label = tk.Label(frame, bg=target_color_hex, width=20, height=2)
    target_label.grid(row=1, column=0)

    tk.Label(frame, text="Your Guess Color:").grid(row=0, column=1, padx=(10, 0))  # Add padding to the left
    guess_label = tk.Label(frame, width=20, height=2, bg="white")
    guess_label.grid(row=1, column=1, padx=(10, 0))  # Add padding to the left

    tk.Label(root, text="Enter your guess:").pack()

    guess_frame = tk.Frame(root)
    guess_frame.pack()

    tk.Label(guess_frame, text="Hue (0-360):").grid(row=0, column=0)
    hue_entry = tk.Entry(guess_frame)
    hue_entry.grid(row=0, column=1)

    tk.Label(guess_frame, text="Saturation (%, 10-100):").grid(row=1, column=0)
    sat_entry = tk.Entry(guess_frame)
    sat_entry.grid(row=1, column=1)

    tk.Label(guess_frame, text="Brightness (%, 10-100):").grid(row=2, column=0)
    bri_entry = tk.Entry(guess_frame)
    bri_entry.grid(row=2, column=1)

    tk.Button(guess_frame, text="Hint", command=provide_hint, width=15).grid(row=0, column=2, padx=(20, 0))  # Add padding to the left
    hint_label = tk.Label(guess_frame, text="", wraplength=140)  # Set wraplength to handle long text
    hint_label.grid(row=1, column=2, rowspan=2, padx=(10, 0))  # Add padding to the left

    tk.Button(root, text="Submit Guess", command=submit_guess).pack()

    result_label = tk.Label(root, text="")
    result_label.pack()

    guess_count_label = tk.Label(root, text=f"Number of guesses: {guess_count}")
    guess_count_label.pack()

    # Game records label
    game_records_label = tk.Label(root)
    game_records_label.pack()

    next_game_button = tk.Button(root, text="Next Game", command=update_target_color)
    next_game_button.pack_forget()  # Initially hide the "Next Game" button

    root.mainloop()
