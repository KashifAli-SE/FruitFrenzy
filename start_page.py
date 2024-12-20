from tkinter import *
from final_main_game import final_main_game  # Ensure this is correctly implemented in main_game.py
from PIL import Image, ImageTk

# Create the main application window
root = Tk()
root.title("FRUIT-FRENZY")
root.attributes('-fullscreen', True)  # Enable fullscreen

# Global variable to store selected difficulty
selected_difficulty = StringVar(value="EASY")  # Default difficulty

# Function to exit fullscreen
def exit_fullscreen(event=None):
    root.attributes('-fullscreen', False)

# Function to display the difficulty selection window
def  difficulty():
    difficulty_window = Toplevel(root)
    difficulty_window.title("DIFFICULTY LEVEL")
    difficulty_window.geometry("600x400+330+200")
    difficulty_window.resizable(False, False)

    Label(difficulty_window, text="SELECT DIFFICULTY", font=("Arial", 16, "bold")).pack(pady=20)

    # Radio buttons for difficulty levels
    difficulties = ["EASY", "MEDIUM", "HARD"]
    for level in difficulties:
        Radiobutton(difficulty_window, bg='light pink', text=level,
            variable=selected_difficulty, value=level, font=("Arial", 14),
            anchor=W).pack(pady=10, anchor=CENTER)

    # Confirm button to close the difficulty window
    Button(difficulty_window, text="CONFIRM", command=difficulty_window.destroy,
        font=("Arial", 12, "bold"), bg="light green", padx=10, pady=5).pack(pady=20)

# Function to load and display the background image
def display_background():
    try:
        image = Image.open('start_page_bg.jpeg')
        image = image.resize((root.winfo_screenwidth(), root.winfo_screenheight()))
        photo = ImageTk.PhotoImage(image)
        image_label = Label(root, image=photo)
        image_label.image = photo  # Keep a reference to prevent garbage collection
        image_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print("Error loading image:", e)
        # Fallback to a solid color if the image fails to load
        root.config(bg="#202020")


# Function to start the game
def start_game():
    difficulty = selected_difficulty.get()  # Get the selected difficulty
    final_main_game(difficulty)  # Call the main_game function with the selected difficulty

# Function to create buttons
def create_buttons():
    # Frame for buttons
    button_frame = Frame(root, bg="#202020")  # Match fallback background
    button_frame.place(relx=0.5, rely=0.6, anchor=CENTER)  # Center frame

    # Button hover effect
    def on_enter(event, button):
        button.config(bg="orange", fg="white")

    def on_leave(event, button):
        button.config(bg="light green", fg="black")

    # Button definitions
    buttons = [
        {"text": "PLAY", "command": start_game},
        {"text": "DIFFICULTY", "command": difficulty},
        {"text": "EXIT", "command": root.destroy}]

    for idx, button_data in enumerate(buttons):
        button = Button(button_frame, text=button_data["text"], command=button_data["command"],
            font=("Arial", 16, "bold"), bg="light green", width=12, height=2)
        button.grid(row=0, column=idx, padx=10, pady=5)
        button.bind("<Enter>", lambda event, btn=button: on_enter(event, btn))
        button.bind("<Leave>", lambda event, btn=button: on_leave(event, btn))

# Add a welcome label
def display_welcome_text():
    name_frame = Frame(root, bg="#202020") # frame to display game name
    name_frame.place(relx=0.5, rely=0.4, anchor=CENTER)
    name = Label(name_frame, text="FRUIT FRENZY", font=("Arial", 64, "bold"), bg="green", fg='white')
    name.pack(padx=10, pady=5, anchor=CENTER)

# Initialize the GUI
display_background()
display_welcome_text()
create_buttons()

# Bind Escape key to exit fullscreen
root.bind("<Escape>", exit_fullscreen)

# Start the Tkinter main loop
root.mainloop()
