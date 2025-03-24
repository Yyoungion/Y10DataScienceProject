import requests
import pygame
import time
from pathlib import Path
import random
import os

pygame.init()
pygame.mixer.init()

base_url = "https://pokeapi.co/api/v2/"

def get_pokemon_info(name):
    try:
        url = f"{base_url}/pokemon/{name}"
        response = requests.get(url)

        if response.status_code == 200:
            pokemon_data = response.json()
            return pokemon_data
        else:
            print(f"Failed to retrieve data {response.status_code}")
            
    except:
        pass

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
            a = f"{str(i).zfill(4)}_{pokemon_info['forms'][0]['name']}.latest"

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
        poke = input("What pokemon do you want to hear? ")
        pokemon_info = get_pokemon_info(poke)
        pokeID = f"{pokemon_info['id']}"
        pokesound = f"{str(pokeID).zfill(4)}_{pokemon_info['forms'][0]['name']}.latest"
        out_file = Path(f"SoundStorage\{pokesound.capitalize()}.ogg").expanduser()
        resp = requests.get(f"https://raw.githubusercontent.com/PokeAPI/cries/main/cries/pokemon/latest/{pokeID}.ogg")
        resp.raise_for_status()
        with open(out_file, "wb") as fout:
            fout.write(resp.content)
        time.sleep(1)
        file_path = r"SoundStorage"'\\' + pokesound + ".ogg"
        pygame.mixer.music.load(str(file_path))
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue
        print("This sound has been automatically saved (If it hasn't been already).")
    except:
        pass

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
    
def main():
    try:
        while True:
            print("To hear a pokemon sound input 1")
            print("To view stored pokemon, input 2")
            print("To play all of the stored pokemon. input 3")
            print("To quit, input 4")
            choice = int(input("What do you want to do (1 - 4): "))
            
            if choice == 1:
                playsound()
                time.sleep(3)
                print("")
                print("")
            elif choice == 2:
                viewstoresound()
                time.sleep(3)
                print("")
                print("")
            elif choice == 3:
                playallstoredsound()
                time.sleep(3)
                print("")
                print("")
            elif choice == 4:
                exit
                quit
                break
            else:
                print("ERROR - U stupid Please try again")
                playrandomsound()
                time.sleep(3)
                print("")
                print("")
    except:
        print("Error. Try again")
        print("")
        print("")
        main()
    
main()








    

