#--- Imports ---

import tkinter as tk
from tkinter import simpledialog, messagebox
import threading
import requests
import pygame
import os
import random
from pathlib import Path
import time
import csv

#--- Obtains the download link for the pokemon ---

def get_pokemon_info(name):
    base_url = "https://pokeapi.co/api/v2/pokemon/"  # Define the base URL for the Pokémon API.
    try:
        response = requests.get(f"{base_url}{name.lower()}") # Make a request to the API using the provided Pokémon name
    
        if response.status_code == 200: # If the response status code is 200, return the JSON data.
            return response.json()
        else: # If the response status is not 200, return nothing
            return None 
    except: # If an exception occurs during the API request return nothing.
        return None
    
#----- Playsound Function -----

def playsound(a):
    def ask_pokemon():
        poke = simpledialog.askstring("Pokémon Sound", "Enter Pokémon name:", parent=a) # Ask user to input a Pokémon name using a dialog window.
        if not poke: # Exit if the user doesn't give a name or closes the window.
            return
        
        
        pokemon_info = get_pokemon_info(poke) # Runs get_pokemon_info to get the 
        # Show an error message if the Pokemon is not found.
        if not pokemon_info:
            messagebox.showerror("Error", "Pokémon not found.")
            return
        
        pokeID = str(pokemon_info['id']) # Gets the pokemon Id
        pokesound = f"{pokeID.zfill(4)}_{pokemon_info['forms'][0]['name']}.latest" # Creates the filename to store the soundfile

        # Set up the directory to store the pokemon
        sound_dir = f"SoundStorage/{username}.poke"
        os.makedirs(sound_dir, exist_ok=True)  # Makes sure the directory exists
        out_file = Path(os.path.join(sound_dir, f"{pokesound}.ogg")).expanduser()
        
        # Check if the sound file has already been downloaded.
        already_stored = out_file.exists()

        # If the file isn't already been downloaded, it will download the file
        if not already_stored:
            try:
                resp = requests.get(f"https://raw.githubusercontent.com/PokeAPI/cries/main/cries/pokemon/latest/{pokeID}.ogg", stream=True)
                resp.raise_for_status()  # For error
                # Saves the file
                with open(out_file, "wb") as fout:
                    fout.write(resp.content)
            except:
                # Show an error message if the download fails.
                messagebox.showerror("Error", "Failed to download sound.")
                return
        
        # Attempt to play the sound file using pygame
        try:
            pygame.mixer.init()  # Initialize the Pygame sound mixer.
            pygame.mixer.music.load(str(out_file))  # Load the sound file.
            pygame.mixer.music.play()  # Play the sound.
            while pygame.mixer.music.get_busy():  # Wait until it has finished playing
                continue
        except Exception as e:
            # Show an error message if sound playback fails.
            messagebox.showerror("Error", f"Failed to play sound: {e}")
            return
        
        # Ask the user if they want to store the sound file
        if not already_stored:
            store_sound = messagebox.askyesno("Save Sound", "Do you want to store this Pokémon sound?")
            if not store_sound:
                # If the user chooses not to save, delete the file
                pygame.mixer.quit()
                time.sleep(0.5)
                os.remove(out_file)
        else:
            pass 

    a.after(0, ask_pokemon)

#----- Play Random Sound Function -----

def playrandomsound():
    try:
        # Generate a random Pokémon ID between 1 and 1025.
        random_pokemon = random.randint(1, 1025)
        
        # Fetch Pokémon information using the ID
        pokemon_info = get_pokemon_info(str(random_pokemon))
        if not pokemon_info:  # If no information is found, exit
            return
        
        # Creates the Pokémon sound filename 
        pokesound = f"{str(random_pokemon).zfill(4)}_{pokemon_info['forms'][0]['name']}.latest"
        pokeID = str(pokemon_info['id'])
        
        # Define file paths for temporary sound storage
        out_file = Path(os.path.join("RandomSound", f"{pokesound}.ogg")).expanduser()
        # Defines the file path for the permernant sound storage of the user
        out_file2 = Path(os.path.join(f"SoundStorage/{username}.poke", f"{pokesound}.ogg")).expanduser()

        # Check if the Pokémon sound is already stored in the user's folder.
        already_stored = out_file2.exists()
        
        # If the sound file is not already downloaded, get it from the API
        if not out_file.exists():
            resp = requests.get(f"https://raw.githubusercontent.com/PokeAPI/cries/main/cries/pokemon/latest/{random_pokemon}.ogg")
            resp.raise_for_status()  # Error 
            with open(out_file, "wb") as fout:  # Save the downloaded file
                fout.write(resp.content)

        # Initialize the Pygame mixer to play the sound.
        pygame.mixer.init()
        pygame.mixer.music.load(str(out_file))  # Load the sound file.
        pygame.mixer.music.play()  # Play the sound.
        
        # Wait for the sound to finish playing.
        while pygame.mixer.music.get_busy():
            continue
        
        # If the sound is not stored, ask the user if they want to save it.
        if not already_stored:
            store_sound = messagebox.askyesno(pokemon_info['forms'][0]['name'].capitalize(), "Do you want to store this Pokémon sound?")
            
            if not store_sound:  # If the user declines to save the sound.
                pygame.mixer.quit()  # Stop the Pygame mixer.
                time.sleep(0.5)  # Wait for a moment.
                os.remove(out_file)  # Delete the temporary sound file.
            
            if store_sound:  # If the user decides to save the sound.
                pygame.mixer.quit()  # Stop the Pygame mixer.
                time.sleep(0.5)  # Wait for a moment.
                os.remove(out_file)  # Delete the temporary sound file.
                
                # Fetch the Pokémon sound again for storage in the user's folder.
                resp = requests.get(f"https://raw.githubusercontent.com/PokeAPI/cries/main/cries/pokemon/latest/{pokeID}.ogg", stream=True)
                resp.raise_for_status()  # Raise an error
                with open(out_file2, "wb") as fout:  # Save the file in the users folder.
                    fout.write(resp.content)

    except:
        # Display an error message
        messagebox.showerror("Error", "Failed to play random sound.")

#----- Play All Stored Sound Function -----

def playallstoredsound():
    try:
        # List all files in the user's Pokémon sound storage folder.
        list_of_songs = os.listdir(f"SoundStorage/{username}.poke")
        
        # Filter the list to include only sound files with the ".latest.ogg".
        songs = [song for song in list_of_songs if song.endswith(".latest.ogg")]
        
        # Check if there are any stored Pokémon sound files. If none, display:.
        if not songs:
            messagebox.showinfo("Stored Pokémon Sounds", "No stored sounds found.")
            return
        
        else:
            # For every song in list of songs it first:.
            for song in list_of_songs:
                if song.endswith(".ogg"):  # Checks for sound files with ".ogg" extension.
                    # Construct the full file path for each sound file.
                    file_path = os.path.join(f"SoundStorage/{username}.poke", song)
                    # Initialize Pygame mixer for playing sounds.
                    pygame.mixer.init()
                    # Load the sound file into Pygame.
                    pygame.mixer.music.load(str(file_path))
                    # Play the sound file.
                    pygame.mixer.music.play()
                    # Wait for the sound to finish playing then plays the next sound.
                    while pygame.mixer.music.get_busy():
                        continue
    
    except:
        # Display an error message
        messagebox.showerror("Error", "Failed to play all stored sounds.")

#----- View All Stored Sound Function -----

def viewstoresound():
    try:
        # List all files in the user's Pokémon sound storage directory.
        list_of_songs = os.listdir(f"SoundStorage/{username}.poke")
        
        # Filter the list to include only sound files with the ".latest.ogg".
        songs = [song for song in list_of_songs if song.endswith(".latest.ogg")]

        # If no Pokémon sound files are found, show the message:.
        if not songs:
            messagebox.showinfo("Stored Pokémon Sounds", "No stored sounds found.")
            return

        # Initialize a new Tkinter window to display stored sounds.
        a = tk.Tk()
        a.title("Stored Pokémon Sounds")

        # Define a function to play a sound file when its button is clicked.
        def play_sound(file_path):
            try:
                pygame.mixer.init()  # Initialize the Pygame mixer.
                pygame.mixer.music.load(file_path)  # Load the sound file.
                pygame.mixer.music.play()  # Play the sound.
            except Exception as e:
                # Show an error message if the sound cannot be played.
                messagebox.showerror("Error", f"Failed to play sound: {e}")

        # Loop through each stored sound file and create a button for it.
        for song in songs:
            # Set the size of the Tkinter window.
            a.geometry("400x300")
            
            # Gets the Pokémon name
            pokemon_name = song.replace(song[0:5], "", 1).replace(".latest.ogg", "").capitalize()
            
            # Construct the full file path for the Pokémon sound file.
            file_path = os.path.join(f"SoundStorage/{username}.poke", song)
            
            # Generate a random background color for the button from the COLORS list.
            COLORS = ['snow', 'ghost white', 'white smoke', 'gainsboro', 'floral white', 'old lace', 'linen', 'antique white', 'papaya whip', 'blanched almond', 'bisque', 'peach puff', 'navajo white', 'lemon chiffon', 'mint cream', 'azure', 'alice blue', 'lavender', 'lavender blush', 'misty rose', 'dark slate gray', 'dim gray', 'slate gray', 'light slate gray', 'gray', 'light grey', 'midnight blue', 'navy', 'cornflower blue', 'dark slate blue', 'slate blue', 'medium slate blue', 'light slate blue', 'medium blue', 'royal blue',  'blue', 'dodger blue', 'deep sky blue', 'sky blue', 'light sky blue', 'steel blue', 'light steel blue', 'light blue', 'powder blue', 'pale turquoise', 'dark turquoise', 'medium turquoise', 'turquoise', 'cyan', 'light cyan', 'cadet blue', 'medium aquamarine', 'aquamarine', 'dark green', 'dark olive green', 'dark sea green', 'sea green', 'medium sea green', 'light sea green', 'pale green', 'spring green', 'lawn green', 'medium spring green', 'green yellow', 'lime green', 'yellow green', 'forest green', 'olive drab', 'dark khaki', 'khaki', 'pale goldenrod', 'light goldenrod yellow', 'light yellow', 'yellow', 'gold', 'light goldenrod', 'goldenrod', 'dark goldenrod', 'rosy brown', 'indian red', 'saddle brown', 'sandy brown', 'dark salmon', 'salmon', 'light salmon', 'orange', 'dark orange', 'coral', 'light coral', 'tomato', 'orange red', 'red', 'hot pink', 'deep pink', 'pink', 'light pink', 'pale violet red', 'maroon', 'medium violet red', 'violet red', 'medium orchid', 'dark orchid', 'dark violet', 'blue violet', 'purple', 'medium purple', 'thistle', 'snow2', 'snow3', 'snow4', 'seashell2', 'seashell3', 'seashell4', 'AntiqueWhite1', 'AntiqueWhite2', 'AntiqueWhite3', 'AntiqueWhite4', 'bisque2', 'bisque3', 'bisque4', 'PeachPuff2', 'PeachPuff3', 'PeachPuff4', 'NavajoWhite2', 'NavajoWhite3', 'NavajoWhite4', 'LemonChiffon2', 'LemonChiffon3', 'LemonChiffon4', 'cornsilk2', 'cornsilk3', 'cornsilk4', 'ivory2', 'ivory3', 'ivory4', 'honeydew2', 'honeydew3', 'honeydew4', 'LavenderBlush2', 'LavenderBlush3', 'LavenderBlush4', 'MistyRose2', 'MistyRose3', 'MistyRose4', 'azure2', 'azure3', 'azure4', 'SlateBlue1', 'SlateBlue2', 'SlateBlue3', 'SlateBlue4', 'RoyalBlue1', 'RoyalBlue2', 'RoyalBlue3', 'RoyalBlue4', 'blue2', 'blue4', 'DodgerBlue2', 'DodgerBlue3', 'DodgerBlue4', 'SteelBlue1', 'SteelBlue2', 'SteelBlue3', 'SteelBlue4', 'DeepSkyBlue2', 'DeepSkyBlue3', 'DeepSkyBlue4', 'SkyBlue1', 'SkyBlue2', 'SkyBlue3', 'SkyBlue4', 'LightSkyBlue1', 'LightSkyBlue2', 'LightSkyBlue3', 'LightSkyBlue4', 'SlateGray1', 'SlateGray2', 'SlateGray3', 'SlateGray4', 'LightSteelBlue1', 'LightSteelBlue2', 'LightSteelBlue3', 'LightSteelBlue4', 'LightBlue1', 'LightBlue2', 'LightBlue3', 'LightBlue4', 'LightCyan2', 'LightCyan3', 'LightCyan4', 'PaleTurquoise1', 'PaleTurquoise2', 'PaleTurquoise3', 'PaleTurquoise4', 'CadetBlue1', 'CadetBlue2', 'CadetBlue3', 'CadetBlue4', 'turquoise1', 'turquoise2', 'turquoise3', 'turquoise4', 'cyan2', 'cyan3', 'cyan4', 'DarkSlateGray1', 'DarkSlateGray2', 'DarkSlateGray3', 'DarkSlateGray4', 'aquamarine2', 'aquamarine4', 'DarkSeaGreen1', 'DarkSeaGreen2', 'DarkSeaGreen3', 'DarkSeaGreen4', 'SeaGreen1', 'SeaGreen2', 'SeaGreen3', 'PaleGreen1', 'PaleGreen2', 'PaleGreen3', 'PaleGreen4', 'SpringGreen2', 'SpringGreen3', 'SpringGreen4', 'green2', 'green3', 'green4', 'chartreuse2', 'chartreuse3', 'chartreuse4', 'OliveDrab1', 'OliveDrab2', 'OliveDrab4', 'DarkOliveGreen1', 'DarkOliveGreen2', 'DarkOliveGreen3', 'DarkOliveGreen4', 'khaki1', 'khaki2', 'khaki3', 'khaki4', 'LightGoldenrod1', 'LightGoldenrod2', 'LightGoldenrod3', 'LightGoldenrod4', 'LightYellow2', 'LightYellow3', 'LightYellow4', 'yellow2', 'yellow3', 'yellow4', 'gold2', 'gold3', 'gold4', 'goldenrod1', 'goldenrod2', 'goldenrod3', 'goldenrod4', 'DarkGoldenrod1', 'DarkGoldenrod2', 'DarkGoldenrod3', 'DarkGoldenrod4', 'RosyBrown1', 'RosyBrown2', 'RosyBrown3', 'RosyBrown4', 'IndianRed1', 'IndianRed2', 'IndianRed3', 'IndianRed4', 'sienna1', 'sienna2', 'sienna3', 'sienna4', 'burlywood1', 'burlywood2', 'burlywood3', 'burlywood4', 'wheat1', 'wheat2', 'wheat3', 'wheat4', 'tan1', 'tan2', 'tan4', 'chocolate1', 'chocolate2', 'chocolate3', 'firebrick1', 'firebrick2', 'firebrick3', 'firebrick4', 'brown1', 'brown2', 'brown3', 'brown4', 'salmon1', 'salmon2', 'salmon3', 'salmon4', 'LightSalmon2', 'LightSalmon3', 'LightSalmon4', 'orange2', 'orange3', 'orange4', 'DarkOrange1', 'DarkOrange2', 'DarkOrange3', 'DarkOrange4', 'coral1', 'coral2', 'coral3', 'coral4', 'tomato2', 'tomato3', 'tomato4', 'OrangeRed2', 'OrangeRed3', 'OrangeRed4', 'red2', 'red3', 'red4', 'DeepPink2', 'DeepPink3', 'DeepPink4', 'HotPink1', 'HotPink2', 'HotPink3', 'HotPink4', 'pink1', 'pink2', 'pink3', 'pink4', 'LightPink1', 'LightPink2', 'LightPink3', 'LightPink4', 'PaleVioletRed1', 'PaleVioletRed2', 'PaleVioletRed3', 'PaleVioletRed4', 'maroon1', 'maroon2', 'maroon3', 'maroon4', 'VioletRed1', 'VioletRed2', 'VioletRed3', 'VioletRed4', 'magenta2', 'magenta3', 'magenta4', 'orchid1', 'orchid2', 'orchid3', 'orchid4', 'plum1', 'plum2', 'plum3', 'plum4', 'MediumOrchid1', 'MediumOrchid2', 'MediumOrchid3', 'MediumOrchid4', 'DarkOrchid1', 'DarkOrchid2', 'DarkOrchid3', 'DarkOrchid4', 'purple1', 'purple2', 'purple3', 'purple4', 'MediumPurple1', 'MediumPurple2', 'MediumPurple3', 'MediumPurple4', 'thistle1', 'thistle2', 'thistle3', 'thistle4', 'gray1', 'gray2', 'gray3', 'gray4', 'gray5', 'gray6', 'gray7', 'gray8', 'gray9', 'gray10', 'gray11', 'gray12', 'gray13', 'gray14', 'gray15', 'gray16', 'gray17', 'gray18', 'gray19', 'gray20', 'gray21', 'gray22', 'gray23', 'gray24', 'gray25', 'gray26', 'gray27', 'gray28', 'gray29', 'gray30', 'gray31', 'gray32', 'gray33', 'gray34', 'gray35', 'gray36', 'gray37', 'gray38', 'gray39', 'gray40', 'gray42', 'gray43', 'gray44', 'gray45', 'gray46', 'gray47', 'gray48', 'gray49', 'gray50', 'gray51', 'gray52', 'gray53', 'gray54', 'gray55', 'gray56', 'gray57', 'gray58', 'gray59', 'gray60', 'gray61', 'gray62', 'gray63', 'gray64', 'gray65', 'gray66', 'gray67', 'gray68', 'gray69', 'gray70', 'gray71', 'gray72', 'gray73', 'gray74', 'gray75', 'gray76', 'gray77', 'gray78', 'gray79', 'gray80', 'gray81', 'gray82', 'gray83', 'gray84', 'gray85', 'gray86', 'gray87', 'gray88', 'gray89', 'gray90', 'gray91', 'gray92', 'gray93', 'gray94', 'gray95', 'gray97', 'gray98', 'gray99']  
            # A list of colors for the button background. Beware sometimes it might be black

            # Create a Tkinter button for the Pokémon sound
            button = tk.Button(
                a,
                text=pokemon_name,  # Button text displays the Pokémon's name.
                command=lambda path=file_path: play_sound(path),  # Play the sound when clicked.
                bg=COLORS[random.randint(0, len(COLORS) - 1)]  # Assign a random color.
            )
            button.pack(pady=2)  # Add space between buttons.

        a.mainloop()

    except Exception as e:
        # Show an error message 
        messagebox.showerror("Error", f"Failed to load stored sounds: {e}")

#----- Main Function -----

def main():
    # Create the main Tkinter window for the Pokémon Sound Player application.
    a = tk.Tk()
    a.title("Pokémon Sound Player")  # Set the window title.
    a.geometry("400x300")  # Set the window size.
    
    # Add a label to the window with the application's title.
    tk.Label(
        a,
        text="Pokémon Sound Player",
        font=("Arial", 14, "bold")
    ).pack(pady=10)  # Add spacing
    # Button to play a Pokémon sound.
    tk.Button(
        a,
        text="Play Pokémon Sound",
        command=lambda: threading.Thread(target=playsound, args=(a,)).start(),
        width=30,  # Set button width.
        bg="light blue"  # Set background color.
    ).pack(pady=5)  # Add spacing 

    # Button to play a random Pokémon sound.
    tk.Button(
        a,
        text="Play Random Pokémon Sound",
        command=lambda: threading.Thread(target=playrandomsound).start(),
        width=30,
        bg="light blue"
    ).pack(pady=5)

    # Button to view stored Pokémon sounds.
    tk.Button(
        a,
        text="View Stored Pokémon Sounds",
        command=lambda: threading.Thread(target=viewstoresound).start(),
        width=30,
        bg="light blue"
    ).pack(pady=5)

    # Button to play all stored Pokémon sounds.
    tk.Button(
        a,
        text="Play All Stored Sounds",
        command=lambda: threading.Thread(target=playallstoredsound).start(),
        width=30,
        bg="light blue"
    ).pack(pady=5)

    # Button to exit the application.
    tk.Button(
        a,
        text="Exit",
        command=a.quit,  # Close the application.
        width=30,
        bg='red'  # Set background color to red for emphasis.
    ).pack(pady=5)

    a.mainloop()  # Run the Tkinter event loop.

def main_action(action):
    # Global username
    global username
    username = username_entry.get()  # Get the entered username.
    password = password_entry.get()  # Get the entered password.

    # Makes sure that username and password are not empty.
    if not username or not password:
        messagebox.showerror("Error", "Username and password cannot be empty.")
        return

    # If they press Create Account
    if action == "Create Account":
        # Check if the username already exists in the Login.csv file.
        if os.path.exists("Login.csv"):
            with open("Login.csv", mode="r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == username:  # If username exists, show an error message.
                        messagebox.showerror("Error", "Username already exists. Please choose a different one.")
                        return

        # Adds the new username and password to the Login.csv file.
        with open("Login.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([username, password])

        # Create a folder to store the user's Pokémon sounds.
        poke_folder = os.path.join(os.getcwd(), f"SoundStorage/{username}.poke")
        os.makedirs(poke_folder, exist_ok=True)

        # Notify the user of successful account creation.
        messagebox.showinfo("Account Created", "Account created successfully!")
        
        # Reset the input form and redirect to the choice screen.
        reset_form()
        root.destroy()
        main()

    # If the action is to log in:
    elif action == "Login":
        # Check if the Login.csv file exists.
        if os.path.exists("Login.csv"):
            with open("Login.csv", mode="r") as file:
                reader = csv.reader(file)
                for row in reader:
                    # Verify the username and password exists 
                    if len(row) == 2 and row[0] == username and row[1] == password:
                        root.destroy()  # Close the login window.
                        main()  # Open the main application window.
                        return
            
            # Error handleing
            messagebox.showerror("Login Failed", "Invalid username or password")

def reset_form():
    # Clear the username and password input in the login form.
    username_entry.delete(0, tk.END)  # Deletes all text from the username.
    password_entry.delete(0, tk.END)  # Deletes all text from the password.

def show_choice_screen():
    # Hide the login frame (if it is currently visible).
    login_frame.pack_forget()
    
    # Display the choice frame with some padding for spacing.
    choice_frame.pack(pady=20)  # Adds vertical spacing (padding) between the frame and other elements.

def show_form(action):
    # Hide the choice frame (if it is currently visible).
    choice_frame.pack_forget()
    login_frame.pack(pady=20)
    
    action_button.config(
        text=action,  # Set the button text to the given action
        command=lambda: main_action(action)  # Link the button to call main_action with the specified action.
    )


# Create the main application window
root = tk.Tk()
root.title("Login or Create Account")  # Set the title of the window

# Create a frame for the initial options (Login or Create Account)
choice_frame = tk.Frame(root)
choice_frame.pack(pady=20)  # Spacing

# Add a label to ask the user to choose an option
choose_label = tk.Label(choice_frame, text="Choose an option:")
choose_label.pack()  # Place the label inside the frame

# Add a button for the "Login" option
# The button calls the function show_form with "Login" as an argument when clicked
login_button = tk.Button(choice_frame, text="Login", command=lambda: show_form("Login"))
login_button.pack(pady=5)  # Add spacing

# Add a button for the "Create Account" option
# The button calls the function show_form with "Create Account" as an argument when clicked
create_button = tk.Button(choice_frame, text="Create Account", command=lambda: show_form("Create Account"))
create_button.pack(pady=5)  # Add spacing

# Create a frame for the login form
login_frame = tk.Frame(root)

# Add a label for the username input
username_label = tk.Label(login_frame, text="Username:")
username_label.pack(pady=5)  # Add spacing

# Create an entry box
username_entry = tk.Entry(login_frame)
username_entry.pack(pady=5)  # Add spacing

# Add a label for the password input
password_label = tk.Label(login_frame, text="Password:")
password_label.pack(pady=5)  # Add spacing

# Create an entry box
# The shows the password as "*"
password_entry = tk.Entry(login_frame, show="*")
password_entry.pack(pady=5)  # Add spacing

# Add a button for performing the main action (Login)
# The button calls the function main_action with "Login" as an argument when clicked
action_button = tk.Button(login_frame, text="Login", command=lambda: main_action("Login"))
action_button.pack(pady=10)  # Add padding below the button for spacing

# Add a button to return to the initial choice screen
# The button calls the show_choice_screen function when clicked
back_button = tk.Button(login_frame, text="Back", command=show_choice_screen)
back_button.pack(pady=5)  # Add padding below the button for spacing

# Start the Tkinter event loop to display the window and wait for user interaction
root.mainloop()