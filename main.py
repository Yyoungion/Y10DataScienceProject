from playsound import playsound
import requests
import pygame, sys, time

pygame.mixer.init()

y = "ditto"

API_URL = "https://pokeapi.co/api/v2/pokemon/{y}"


x = requests.get("https://raw.githubusercontent.com/PokeAPI/cries/main/cries/pokemon/latest/132.ogg")


pygame.mixer.Sound(x)


