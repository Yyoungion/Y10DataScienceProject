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
                pygame.mixer.quit()
                time.sleep(0.5)
                os.remove(out_file)
        else:
            pass

    root.after(0, ask_pokemon)

def playrandomsound():
    try:
        random_pokemon = random.randint(1, 1025)
        pokemon_info = get_pokemon_info(str(random_pokemon))
        if not pokemon_info:
            return
        
        pokesound = f"{str(random_pokemon).zfill(4)}_{pokemon_info['forms'][0]['name']}.latest"
        pokeID = str(pokemon_info['id'])
        out_file = Path(os.path.join("RandomSound", f"{pokesound}.ogg")).expanduser()
        out_file2 = Path(os.path.join("SoundStorage", f"{pokesound}.ogg")).expanduser()

        already_stored = out_file2.exists()
        
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
        if not already_stored:
            store_sound = messagebox.askyesno(pokemon_info['forms'][0]['name'].capitalize(), "Do you want to store this Pokémon sound?")
            if not store_sound:
                pygame.mixer.quit()
                time.sleep(0.5)
                os.remove(out_file)
            
            if store_sound:
                pygame.mixer.quit()
                time.sleep(0.5)
                os.remove(out_file)
                resp = requests.get(f"https://raw.githubusercontent.com/PokeAPI/cries/main/cries/pokemon/latest/{pokeID}.ogg", stream=True)
                resp.raise_for_status()
                with open(out_file2, "wb") as fout:
                    fout.write(resp.content)


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
        songs = [song for song in list_of_songs if song.endswith(".latest.ogg")]

        if not songs:
            messagebox.showinfo("Stored Pokémon Sounds", "No stored sounds found.")
            return

        root = tk.Tk()
        root.title("Stored Pokémon Sounds")

        def play_sound(file_path):
            try:
                pygame.mixer.init()
                pygame.mixer.music.load(file_path)
                pygame.mixer.music.play()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to play sound: {e}")

        for song in songs:
            root.geometry("400x300")
            pokemon_name = song.replace(song[0:5], "", 1).replace(".latest.ogg", "").capitalize()
            file_path = os.path.join("SoundStorage", song)
            COLORS  =['snow', 'ghost white', 'white smoke', 'gainsboro', 'floral white', 'old lace',
'linen', 'antique white', 'papaya whip', 'blanched almond', 'bisque', 'peach puff',
'navajo white', 'lemon chiffon', 'mint cream', 'azure', 'alice blue', 'lavender',
'lavender blush', 'misty rose', 'dark slate gray', 'dim gray', 'slate gray',
'light slate gray', 'gray', 'light grey', 'midnight blue', 'navy', 'cornflower blue', 'dark slate blue',
'slate blue', 'medium slate blue', 'light slate blue', 'medium blue', 'royal blue',  'blue',
'dodger blue', 'deep sky blue', 'sky blue', 'light sky blue', 'steel blue', 'light steel blue',
'light blue', 'powder blue', 'pale turquoise', 'dark turquoise', 'medium turquoise', 'turquoise',
'cyan', 'light cyan', 'cadet blue', 'medium aquamarine', 'aquamarine', 'dark green', 'dark olive green',
'dark sea green', 'sea green', 'medium sea green', 'light sea green', 'pale green', 'spring green',
'lawn green', 'medium spring green', 'green yellow', 'lime green', 'yellow green',
'forest green', 'olive drab', 'dark khaki', 'khaki', 'pale goldenrod', 'light goldenrod yellow',
'light yellow', 'yellow', 'gold', 'light goldenrod', 'goldenrod', 'dark goldenrod', 'rosy brown',
'indian red', 'saddle brown', 'sandy brown',
'dark salmon', 'salmon', 'light salmon', 'orange', 'dark orange',
'coral', 'light coral', 'tomato', 'orange red', 'red', 'hot pink', 'deep pink', 'pink', 'light pink',
'pale violet red', 'maroon', 'medium violet red', 'violet red',
'medium orchid', 'dark orchid', 'dark violet', 'blue violet', 'purple', 'medium purple',
'thistle', 'snow2', 'snow3',
'snow4', 'seashell2', 'seashell3', 'seashell4', 'AntiqueWhite1', 'AntiqueWhite2',
'AntiqueWhite3', 'AntiqueWhite4', 'bisque2', 'bisque3', 'bisque4', 'PeachPuff2',
'PeachPuff3', 'PeachPuff4', 'NavajoWhite2', 'NavajoWhite3', 'NavajoWhite4',
'LemonChiffon2', 'LemonChiffon3', 'LemonChiffon4', 'cornsilk2', 'cornsilk3',
'cornsilk4', 'ivory2', 'ivory3', 'ivory4', 'honeydew2', 'honeydew3', 'honeydew4',
'LavenderBlush2', 'LavenderBlush3', 'LavenderBlush4', 'MistyRose2', 'MistyRose3',
'MistyRose4', 'azure2', 'azure3', 'azure4', 'SlateBlue1', 'SlateBlue2', 'SlateBlue3',
'SlateBlue4', 'RoyalBlue1', 'RoyalBlue2', 'RoyalBlue3', 'RoyalBlue4', 'blue2', 'blue4',
'DodgerBlue2', 'DodgerBlue3', 'DodgerBlue4', 'SteelBlue1', 'SteelBlue2',
'SteelBlue3', 'SteelBlue4', 'DeepSkyBlue2', 'DeepSkyBlue3', 'DeepSkyBlue4',
'SkyBlue1', 'SkyBlue2', 'SkyBlue3', 'SkyBlue4', 'LightSkyBlue1', 'LightSkyBlue2',
'LightSkyBlue3', 'LightSkyBlue4', 'SlateGray1', 'SlateGray2', 'SlateGray3',
'SlateGray4', 'LightSteelBlue1', 'LightSteelBlue2', 'LightSteelBlue3',
'LightSteelBlue4', 'LightBlue1', 'LightBlue2', 'LightBlue3', 'LightBlue4',
'LightCyan2', 'LightCyan3', 'LightCyan4', 'PaleTurquoise1', 'PaleTurquoise2',
'PaleTurquoise3', 'PaleTurquoise4', 'CadetBlue1', 'CadetBlue2', 'CadetBlue3',
'CadetBlue4', 'turquoise1', 'turquoise2', 'turquoise3', 'turquoise4', 'cyan2', 'cyan3',
'cyan4', 'DarkSlateGray1', 'DarkSlateGray2', 'DarkSlateGray3', 'DarkSlateGray4',
'aquamarine2', 'aquamarine4', 'DarkSeaGreen1', 'DarkSeaGreen2', 'DarkSeaGreen3',
'DarkSeaGreen4', 'SeaGreen1', 'SeaGreen2', 'SeaGreen3', 'PaleGreen1', 'PaleGreen2',
'PaleGreen3', 'PaleGreen4', 'SpringGreen2', 'SpringGreen3', 'SpringGreen4',
'green2', 'green3', 'green4', 'chartreuse2', 'chartreuse3', 'chartreuse4',
'OliveDrab1', 'OliveDrab2', 'OliveDrab4', 'DarkOliveGreen1', 'DarkOliveGreen2',
'DarkOliveGreen3', 'DarkOliveGreen4', 'khaki1', 'khaki2', 'khaki3', 'khaki4',
'LightGoldenrod1', 'LightGoldenrod2', 'LightGoldenrod3', 'LightGoldenrod4',
'LightYellow2', 'LightYellow3', 'LightYellow4', 'yellow2', 'yellow3', 'yellow4',
'gold2', 'gold3', 'gold4', 'goldenrod1', 'goldenrod2', 'goldenrod3', 'goldenrod4',
'DarkGoldenrod1', 'DarkGoldenrod2', 'DarkGoldenrod3', 'DarkGoldenrod4',
'RosyBrown1', 'RosyBrown2', 'RosyBrown3', 'RosyBrown4', 'IndianRed1', 'IndianRed2',
'IndianRed3', 'IndianRed4', 'sienna1', 'sienna2', 'sienna3', 'sienna4', 'burlywood1',
'burlywood2', 'burlywood3', 'burlywood4', 'wheat1', 'wheat2', 'wheat3', 'wheat4', 'tan1',
'tan2', 'tan4', 'chocolate1', 'chocolate2', 'chocolate3', 'firebrick1', 'firebrick2',
'firebrick3', 'firebrick4', 'brown1', 'brown2', 'brown3', 'brown4', 'salmon1', 'salmon2',
'salmon3', 'salmon4', 'LightSalmon2', 'LightSalmon3', 'LightSalmon4', 'orange2',
'orange3', 'orange4', 'DarkOrange1', 'DarkOrange2', 'DarkOrange3', 'DarkOrange4',
'coral1', 'coral2', 'coral3', 'coral4', 'tomato2', 'tomato3', 'tomato4', 'OrangeRed2',
'OrangeRed3', 'OrangeRed4', 'red2', 'red3', 'red4', 'DeepPink2', 'DeepPink3', 'DeepPink4',
'HotPink1', 'HotPink2', 'HotPink3', 'HotPink4', 'pink1', 'pink2', 'pink3', 'pink4',
'LightPink1', 'LightPink2', 'LightPink3', 'LightPink4', 'PaleVioletRed1',
'PaleVioletRed2', 'PaleVioletRed3', 'PaleVioletRed4', 'maroon1', 'maroon2',
'maroon3', 'maroon4', 'VioletRed1', 'VioletRed2', 'VioletRed3', 'VioletRed4',
'magenta2', 'magenta3', 'magenta4', 'orchid1', 'orchid2', 'orchid3', 'orchid4', 'plum1',
'plum2', 'plum3', 'plum4', 'MediumOrchid1', 'MediumOrchid2', 'MediumOrchid3',
'MediumOrchid4', 'DarkOrchid1', 'DarkOrchid2', 'DarkOrchid3', 'DarkOrchid4',
'purple1', 'purple2', 'purple3', 'purple4', 'MediumPurple1', 'MediumPurple2',
'MediumPurple3', 'MediumPurple4', 'thistle1', 'thistle2', 'thistle3', 'thistle4',
'gray1', 'gray2', 'gray3', 'gray4', 'gray5', 'gray6', 'gray7', 'gray8', 'gray9', 'gray10',
'gray11', 'gray12', 'gray13', 'gray14', 'gray15', 'gray16', 'gray17', 'gray18', 'gray19']
            
            button = tk.Button(root, 
                               text=pokemon_name, 
                               command=lambda path=file_path: play_sound(path),
                                bg=COLORS[random.randint(0,len(COLORS)-1)])
        
            button.pack(pady=2)

        root.mainloop()

    except Exception as e:
        messagebox.showerror("Error", f"Failed to load stored sounds: {e}")

def main():
    root = tk.Tk()
    root.title("Pokémon Sound Player")
    root.geometry("400x300")
    
    tk.Label(root, 
             text="Pokémon Sound Player", 
             font=("Arial", 14, "bold")).pack(pady=10)
    
    tk.Button(root, 
              text="Play Pokémon Sound", 
              command=lambda: threading.Thread(target=playsound, args=(root,)).start(), 
              width=30, bg="light blue").pack(pady=5)
    
    tk.Button(root, 
              text="Play Random Pokémon Sound", 
              command=lambda: threading.Thread(target=playrandomsound).start(), 
              width=30, bg="light blue").pack(pady=5)
    
    tk.Button(root, 
              text="View Stored Pokémon Sounds", 
              command=lambda: threading.Thread(target=viewstoresound).start(), 
              width=30, bg="light blue").pack(pady=5)
    
    tk.Button(root, 
              text="Play All Stored Sounds", 
              command=lambda: threading.Thread(target=playallstoredsound).start(), 
              width=30, bg="light blue").pack(pady=5)
    
    tk.Button(root, 
              text="Exit", 
              command=root.quit, 
              width=30, bg='red').pack(pady=5)
    
    root.mainloop()

main()