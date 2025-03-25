import tkinter as tk
from tkinter import simpledialog, messagebox
import threading
import requests
import pygame
import os
import random
from pathlib import Path
import time
def get_pokemon_info(name):
    base_url = "https://pokeapi.co/api/v2/pokemon/"
    try:
        response = requests.get(f"{base_url}{name.lower()}")
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except:
        return None

def playsound(root):
    def ask_pokemon():
        poke = simpledialog.askstring("Pokémon Sound", "Enter Pokémon name:", parent=root)
        if not poke:
            return
        
        pokemon_info = get_pokemon_info(poke)
        if not pokemon_info:
            messagebox.showerror("Error", "Pokémon not found.")
            return
        
        pokeID = str(pokemon_info['id'])
        pokesound = f"{pokeID.zfill(4)}_{pokemon_info['forms'][0]['name']}.latest"
        
        sound_dir = "SoundStorage"
        os.makedirs(sound_dir, exist_ok=True)
        out_file = Path(os.path.join(sound_dir, f"{pokesound}.ogg")).expanduser()
        
        already_stored = out_file.exists()

        if not already_stored:
            try:
                resp = requests.get(f"https://raw.githubusercontent.com/PokeAPI/cries/main/cries/pokemon/latest/{pokeID}.ogg", stream=True)
                resp.raise_for_status()
                with open(out_file, "wb") as fout:
                    fout.write(resp.content)
            except:
                messagebox.showerror("Error", "Failed to download sound.")
                return
        
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(str(out_file))
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                continue
        except Exception as e:
            messagebox.showerror("Error", f"Failed to play sound: {e}")
            return
        
        if not already_stored:
            store_sound = messagebox.askyesno("Save Sound", "Do you want to store this Pokémon sound?")
            if not store_sound:
                os.remove(out_file)
        else:
            messagebox.showinfo("Info", f"{poke.capitalize()} sound is already stored.")

    root.after(0, ask_pokemon)


def playrandomsound():
    try:
        random_pokemon = random.randint(1, 1025)
        pokemon_info = get_pokemon_info(str(random_pokemon))
        if not pokemon_info:
            return
        
        pokesound = f"{str(random_pokemon).zfill(4)}_{pokemon_info['forms'][0]['name']}.latest"
        out_file = Path(os.path.join("RandomSound", f"{pokesound}.ogg")).expanduser()
        
        if not out_file.exists():
            resp = requests.get(f"https://raw.githubusercontent.com/PokeAPI/cries/main/cries/pokemon/latest/{random_pokemon}.ogg")
            resp.raise_for_status()
            with open(out_file, "wb") as fout:
                fout.write(resp.content)
        
        pygame.mixer.init()
        pygame.mixer.music.load(str(out_file))
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        time.sleep(0.5)
        os.remove(out_file)
    except:
        messagebox.showerror("Error", "Failed to play random sound.")

def playallstoredsound():
    try:
        list_of_songs = os.listdir("SoundStorage")
        for song in list_of_songs:
            if song.endswith(".ogg"):
                file_path = os.path.join("SoundStorage", song)
                pygame.mixer.init()
                pygame.mixer.music.load(str(file_path))
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    continue
    except:
        messagebox.showerror("Error", "Failed to play all stored sounds.")

def viewstoresound():
    try:
        list_of_songs = os.listdir("SoundStorage")
        stored_sounds = "\n".join([song.replace(song[0:5], "", 1).replace(".latest.ogg", "").capitalize() for song in list_of_songs if song.endswith(".latest.ogg")])
        messagebox.showinfo("Stored Pokémon Sounds", stored_sounds if stored_sounds else "No stored sounds found.")
    except:
        messagebox.showerror("Error", "Failed to load stored sounds.")

def main():
    root = tk.Tk()
    root.title("Pokémon Sound Player")
    root.geometry("400x300")
    
    tk.Label(root, text="Pokémon Sound Player", font=("Arial", 14, "bold")).pack(pady=10)
    
    tk.Button(root, text="Play Pokémon Sound", command=lambda: threading.Thread(target=playsound, args=(root,)).start(), width=30).pack(pady=5)
    tk.Button(root, text="Play Random Pokémon Sound", command=lambda: threading.Thread(target=playrandomsound).start(), width=30).pack(pady=5)
    tk.Button(root, text="View Stored Pokémon Sounds", command=lambda: threading.Thread(target=viewstoresound).start(), width=30).pack(pady=5)
    tk.Button(root, text="Play All Stored Sounds", command=lambda: threading.Thread(target=playallstoredsound).start(), width=30).pack(pady=5)
    tk.Button(root, text="Exit", command=root.quit, width=30).pack(pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    main()
