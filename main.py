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
    a = f"{pokemon_info['cries']['latest']}"
    print(a)
    

