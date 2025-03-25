import requests
import pygame
import time
from pathlib import Path
import random
import os
import tkinter as tk

pygame.init()
pygame.mixer.init()

base_url = "https://pokeapi.co/api/v2/"

def get_pokemon_info(name):
    try:
        # Construct the URL for the Pokémon API using base_url and the name of the Pokémon
        url = f"{base_url}/pokemon/{name}"
        # Send a request to the API to fetch Pokémon data
        response = requests.get(url)

        # Check if the request was successful (HTTP status code 200)
        if response.status_code == 200:
            pokemon_data = response.json()
            return pokemon_data  # Return the data for further processing
        else:
            # If the request fails, print an error message with the status code
            print(f"Failed to retrieve data {response.status_code}")

    # Handle any exception that might occur during the try block
    except:
        pass

def playrandomsound():
    try:
        for i in range (0,1):
            random_pokemon = random.randint(1, 1025)
            pokemon_info = get_pokemon_info(random_pokemon)
            a = f"{str(random_pokemon).zfill(4)}_{pokemon_info['forms'][0]['name']}.latest"

            out_file = Path(f"RandomSound\{a.capitalize()}.ogg").expanduser()
            resp = requests.get(f"https://raw.githubusercontent.com/PokeAPI/cries/main/cries/pokemon/latest/{random_pokemon}.ogg")
            resp.raise_for_status()
            with open(out_file, "wb") as fout:
                fout.write(resp.content)
            time.sleep(1)
            
        lists_of_songs = os.listdir(r"RandomSound"'\\')

        for song in lists_of_songs:
            if song.endswith(".ogg"):
                file_path = r"RandomSound"'\\' + song
                pygame.mixer.music.load(str(file_path))
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy() == True:
                    continue
    except:
        pass

def playsound():
    try:
        # Get the Pokémon name from the entry field
        poke = entry_pokemon.get().strip().lower()
        if not poke:
            messagebox.showwarning("Input Error", "Please enter a Pokémon name!")
            return

        # Retrieve Pokémon information
        pokemon_info = get_pokemon_info(poke)
        if not pokemon_info:
            messagebox.showerror("Error", f"Pokémon '{poke}' not found!")
            return

        # Generate the sound file name using Pokémon ID and form name
        pokeID = str(pokemon_info['id']).zfill(4)
        pokesound = f"{pokeID}_{pokemon_info['forms'][0]['name']}.latest"
        out_file = Path(f"SoundStorage/{pokesound}.ogg").expanduser()

        # Check if the sound file exists locally
        if not out_file.exists():
            # Download the sound file
            try:
                url = f"https://raw.githubusercontent.com/PokeAPI/cries/main/cries/pokemon/latest/{pokeID}.ogg"
                resp = requests.get(url)
                resp.raise_for_status()

                out_file.parent.mkdir(parents=True, exist_ok=True)  # Create directory if it doesn't exist
                with open(out_file, "wb") as fout:
                    fout.write(resp.content)
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while downloading the sound file: {e}")
                return

        # Play the sound file using pygame
        try:
            pygame.mixer.quit()  # Reset pygame mixer settings
            pygame.mixer.init()
            pygame.mixer.music.load(str(out_file))
            pygame.mixer.music.play()
            messagebox.showinfo("Success", f"Playing sound for {poke.capitalize()}!")
            # Keep the program running while the sound is playing
            while pygame.mixer.music.get_busy():
                continue
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while playing the sound: {e}")

    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    # Ask the user to input the name of a Pokémon they want to hear
    poke = input("What Pokémon do you want to hear? ")

    # Retrieve Pokémon information
    pokemon_info = get_pokemon_info(poke)

    # Get the Pokémon's ID to create the sound file name
    pokeID = f"{pokemon_info['id']}"  # Extract Pokémon's ID
    pokesound = f"{str(pokeID).zfill(4)}_{pokemon_info['forms'][0]['name']}.latest"  # Create Filename

    # Define the path to save the sound file
    out_file = Path(os.path.join("SoundStorage", f"{pokesound}.ogg")).expanduser()

    # Check if the sound file already exists
    if not out_file.exists():
        # If not, download the sound file from the URL
        resp = requests.get(f"https://raw.githubusercontent.com/PokeAPI/cries/main/cries/pokemon/latest/{pokeID}.ogg")
        resp.raise_for_status()  # Raise an error if the request fails
        # Save the downloaded content to the file
        with open(out_file, "wb") as fout:
            fout.write(resp.content)
        print("File downloaded and saved.")
    else:
        # If the file already exists, skip the download
        print("File already exists. Skipping download.")

    pygame.mixer.quit()  # Reset pygame mixer settings
    pygame.mixer.init()  # Reinitialize the mixer

    # Load the sound file into pygame
    file_path = os.path.join("SoundStorage", f"{pokesound}.ogg")  # Get the full path to the sound file
    pygame.mixer.music.load(str(file_path))  # Load the sound file
    pygame.mixer.music.play()  # Play the sound

    # Keep the program running while the sound is playing
    while pygame.mixer.music.get_busy():
        continue

def playallstoredsound():
    try:
        list_of_songs = os.listdir(r"SoundStorage"'\\')
        
        for song in list_of_songs:
            if song.endswith(".ogg"):
                file_path = r"SoundStorage"'\\' + song
                pygame.mixer.music.load(str(file_path))
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy() == True:
                    continue
    except:
        pass
    
def viewstoresound():
    try:
        # Create a new Toplevel window for displaying stored sounds
        stored_window = tk.Toplevel(root)
        stored_window.title("Stored Pokémon Sounds")
        stored_window.geometry("300x400")

        sound_storage = Path("SoundStorage").expanduser()
        list_of_songs = os.listdir(sound_storage)
        stored_names = []

        # Collect the names of stored Pokémon sounds
        for song in list_of_songs:
            if song.endswith(".latest.ogg"):
                song = song.replace(song[0:5], "", 1)  # Remove ID prefix
                song = song.replace(".latest.ogg", "")  # Remove file extension
                stored_names.append(song.capitalize())  # Capitalize for better readability

        # Check if there are any stored sounds
        if not stored_names:
            label_empty = tk.Label(stored_window, text="No stored Pokémon sounds found!", font=("Arial", 12))
            label_empty.pack(pady=20)
        else:
            # Display the list of stored Pokémon names in a Listbox
            label_title = tk.Label(stored_window, text="Stored Pokémon Sounds:", font=("Arial", 14, "bold"))
            label_title.pack(pady=10)

            listbox = tk.Listbox(stored_window, height=20, width=30)
            for name in stored_names:
                listbox.insert(tk.END, name)
            listbox.pack(pady=10)

        # Add a Close button to the Toplevel window
        close_button = tk.Button(stored_window, text="Close", command=stored_window.destroy)
        close_button.pack(pady=10)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while viewing stored sounds: {e}")

    try:
        print("Here is all the pokemon sounds that have been stored.")
        list_of_songs = os.listdir(r"SoundStorage"'\\')
        for song in list_of_songs:
            if song.endswith(".latest.ogg"):
                song = song.replace(song[0:5],"",1)
                song = song.replace(".latest.ogg",'')
                songcap = song.capitalize()
                print(songcap)
    except:
        pass
   

root = tk.Tk()
root.title("Pokémon Sound Player")

# Entry for entering Pokémon name
label_pokemon = tk.Label(root, text="Enter Pokémon Name:")
label_pokemon.pack(pady=5)

entry_pokemon = tk.Entry(root)
entry_pokemon.pack(pady=5)

# Buttons for functions
button_play = tk.Button(root, text="Play Pokémon Sound", command=playsound)
button_play.pack(pady=5)

button_play_all = tk.Button(root, text="Play All Stored Sounds", command=playallstoredsound)
button_play_all.pack(pady=5)

button_random = tk.Button(root, text="Play Random Pokémon Sound", command=playrandomsound)
button_random.pack(pady=5)

button_view_stored = tk.Button(root, text="View Stored Pokémon Sounds", command=viewstoresound)
button_view_stored.pack(pady=5)

# Run the GUI loop
root.mainloop() 
 
def main():
    a = 2
    while a == 2:
        try:
            while True:
                print("To hear a pokemon sound input 1")
                print("To view stored pokemon, input 2")
                print("To play all of the stored pokemon. input 3")
                print("To quit, input 4")
                choice = int(input("What do you want to do (1 - 4): "))
                
                if choice == 1:
                    playsound()
                    time.sleep(2)
                    print("")
                    print("")
                elif choice == 2:
                    viewstoresound()
                    time.sleep(2)
                    print("")
                    print("")
                elif choice == 3:
                    playallstoredsound()
                    time.sleep(2)
                    print("")
                    print("")
                elif choice == 4:
                    a = 1
                    exit
                    quit
                    break
            

        except:
            print("ERROR - U stupid Please try again")
            playrandomsound()
            time.sleep(2)
            print("")
            print("")

GUI()







    

