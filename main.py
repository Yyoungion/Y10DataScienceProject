from playsound import playsound
import requests
import pygame, sys, time

pygame.mixer.init()

API_URL = "https://pokeapi.co/api/v2/pokemon"

dex = {}

def search_pokemon(pokemon_name):
    """Search for a Pokémon in the PokéAPI and return its details."""
    response = requests.get(API_URL + pokemon_name.lower())
    if response.status_code == 200:
        data = response.json()
        return {
            "name": data["name"].capitalize(),
            "id": data["id"],
            "type": [t["type"]["name"] for t in data["types"]],
            "hp": data["stats"][0]["base_stat"]  # HP stat
        }
    else:
        print("Pokémon not found.")
        return None


x = requests.get("https://raw.githubusercontent.com/PokeAPI/cries/main/cries/pokemon/latest/132.ogg")


pygame.mixer.Sound(x)


