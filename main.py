import requests
import pygame
import time
import threading

base_url = "https://pokeapi.co/api/v2/"

def get_pokemon_info(name):
    url = f"{base_url}/pokemon/{name}"
    response = requests.get(url)

    if response.status_code == 200:
        pokemon_data = response.json()
        return pokemon_data
    else:
        print(f"Failed to retrieve data {response.status_code}")
        
        
pokemon_name = "ditto"
pokemon_info = get_pokemon_info(pokemon_name)

if pokemon_info:
    a = f"{pokemon_info["cries"]["latest"]  }"
    b = requests.get(a)
    
doc = requests.get(b)
f = open("movie.mp3","wb")
f.write(doc.text)
f.close()
    
    
    
def playmusic():       
    def play_music(b):
        pygame.mixer.init()
        pygame.mixer.music.load(b)
        pygame.mixer.play_music()
    
    def wait_for_input():
        input()
        pygame.mixer.music.stop()
  

    music_thread = threading.Thread(target=play_music, args=(b))
    input_thread = threading.Thread(target=wait_for_input)

    music_thread.start()
    input_thread.start()