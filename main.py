import requests
import pygame
import time
import threading
from pathlib import Path
import random
import os

pygame.init()
pygame.mixer.init()

base_url = "https://pokeapi.co/api/v2/"

def get_pokemon_info(name):
    url = f"{base_url}/pokemon/{name}"
    response = requests.get(url)

    if response.status_code == 200:
        pokemon_data = response.json()
        return pokemon_data
    else:
        print(f"Failed to retrieve data {response.status_code}")

def download_all_pokemon():
    print("Do you want to have all the pokemon sound files? ")
    print("This will remove the need to download a pokemon call every time you want to play a sound from a new pokemon.")
    print("This may take a long time.")
    download = input("Y/N ")

    if download == "Y":
        print("Downloading")
        print("Estimated time: 20 minutes")
        for i in range(1,1026):
            pokemon_info = get_pokemon_info(i)
            a = f"{i:04}_{pokemon_info['forms'][0]['name']}.latest"

            out_file = Path(f"~/Documents/Github\Y10DataScienceProject\SoundStorageALL\{a.capitalize()}.mp3").expanduser()
            resp = requests.get(f"https://raw.githubusercontent.com/PokeAPI/cries/main/cries/pokemon/latest/{i}.ogg")
            resp.raise_for_status()
            with open(out_file, "wb") as fout:
                fout.write(resp.content)
    elif download == "N":
        pass
    else:
        playrandomsound()

def playrandomsound():
    for i in range (0,10):
        random_pokemon = random.randint(1, 1025)
        pokemon_info = get_pokemon_info(random_pokemon)
        a = f"{random_pokemon:04}_{pokemon_info['forms'][0]['name']}.latest"

        out_file = Path(f"~/Documents/Github\Y10DataScienceProject\RandomSound\{a.capitalize()}.ogg").expanduser()
        resp = requests.get(f"https://raw.githubusercontent.com/PokeAPI/cries/main/cries/pokemon/latest/{random_pokemon}.ogg")
        resp.raise_for_status()
        with open(out_file, "wb") as fout:
            fout.write(resp.content)
        time.sleep(1)
        
    lists_of_songs = os.listdir(r"c:\Users\Yyoung Du\Documents\Github\Y10DataScienceProject\RandomSound"'\\')

    for song in lists_of_songs:
        if song.endswith(".mp3"):
            file_path = r"c:\Users\Yyoung Du\Documents\Github\Y10DataScienceProject\RandomSound"'\\' + song
            pygame.mixer.music.load(str(file_path))
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() == True:
                continue
    time.sleep(20)

def main():
    download_all_pokemon()
    playrandomsound()

main()








    

