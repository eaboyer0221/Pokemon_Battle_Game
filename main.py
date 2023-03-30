import math
import random
from tkinter import messagebox

import pandas as pd
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageTk
import io
import tkinter as tk

cached_windows = []
cached_player = None


def pokedex(url='https://pokemondb.net/pokedex/all'):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'id': 'pokedex'})
    headers = []
    for th in table.find('thead').find_all('th'):
        headers.append(th.text.strip())
    headers.append('image_url')
    rows = []
    for tr in table.find('tbody').find_all('tr'):
        row = []
        for td in tr.find_all('td'):
            row.append(td.text.strip())
        row.append(tr.find("img")['src'])
        rows.append(row)
    return pd.DataFrame(rows, columns=headers)


# Define Pokemon Class that has three attributes:
# 1) name    2) hit power   3) life points
class Pokemon:
    def __init__(self, pokemon_data):
        if pokemon_data is None:
            pokemon_data = pokedex.sample()

        self.name = pokemon_data['Name'].values[0]
        self.pokemon_type = pokemon_data['Type'].values[0]
        self.life_points = pokemon_data['HP'].values[0]
        self.hit_power = pokemon_data['Attack'].values[0]
        self.defense = pokemon_data['Defense'].values[0]
        self.image_url = pokemon_data['image_url'].values[0]
        self.is_legendary = False

    # Create "say_hi" method to print pokemon's basic info (name, hit power, and life points)
    def say_hi(self):
        messagebox.showinfo("Battle", f"{self.name} says hello! {self.name} has {self.hit_power} hit power and {self.life_points} life points.")

    # "attack" method that reduces the enemy's life point by the attacking pokemon's hit power, and prints out the enemy's life point after attack.
    def attack(self, enemy):
        enemy.life_points = max(enemy.life_points - self.hit_power, 0)
        return enemy.life_points


def handle_attack_click(player_pokemon, enemy_pokemon):
    enemy_life_points = player_pokemon.attack(enemy_pokemon)
    if enemy_life_points <= 0:
        print(f"{enemy_pokemon.name} fainted. {player_pokemon.name} won the battle!")
    else:
        enemy_pokemon.attack(player_pokemon)
        if player_pokemon.life_points <= 0:
            print(f"{player_pokemon.name} fainted. {enemy_pokemon.name} won the battle!")
        # print(f"{self.name} attacks!")
        # print(f"{enemy.name} loses life power!")
        # print(f"{enemy.name} life power is {enemy.life_points}!")

        # let the player's Pokemon attack the enemy Pokemon until one of them loses the game
        while player_pokemon.life_points > 0 and enemy_pokemon.life_points > 0:
            player_pokemon.attack(enemy_pokemon)
            if enemy_pokemon.life_points <= 0:
                print(f"{enemy_pokemon.name} fainted. {player_pokemon.name} won the battle!")
                break
            enemy_pokemon.attack(player_pokemon)
            if player_pokemon.life_points <= 0:
                print(f"{player_pokemon.name} fainted. {enemy_pokemon.name} won the battle!")
            break


class Legendary(Pokemon):
    def __init__(self, name: str, hit_power: int, life_points: int):
        super().__init__(name, hit_power, life_points)
        if self.name not in legendary_pokemon:
            raise Exception("Not Legendary")
            self.is_legendary = False
        self.hit_power *= 1.3


def make_suitable_enemy_stat(self, pokemon_stat, percent_range_factor):
    percent_stat_adjustment = (percent_range_factor * pokemon_stat)
    return random.randint(pokemon_stat - percent_stat_adjustment, pokemon_stat + percent_stat_adjustment)


pokedex = pokedex()
filter = pokedex['Name'].str.contains(" ")
pokedex = pokedex[~filter]
print(pokedex)

legendary_pokemon = ["Articuno", "Moltres", "Mewtwo", "Zapdos", "Lugia", "Ho-oh"]


def display_pokemon(player_type, player, root):
    # Create a new window to display the Pokemon info
    if player_type == "player":
        info_window = tk.Frame(root)
        info_window.grid(row=6, column=1)
    elif player_type == "enemy":
        info_window = tk.Frame(root)
        info_window.grid(row=6, column=3)

    # Add labels and values to display the Pokemon info
    tk.Label(info_window, text="Name:").grid(row=0, column=0)
    pokemon = player.pokemon
    tk.Label(info_window, text=pokemon.name).grid(row=0, column=1)
    tk.Label(info_window, text="Type:").grid(row=1, column=0)
    tk.Label(info_window, text=pokemon.pokemon_type).grid(row=1, column=1)
    tk.Label(info_window, text="HP:").grid(row=2, column=0)
    tk.Label(info_window, text=pokemon.life_points).grid(row=2, column=1)
    tk.Label(info_window, text="Attack:").grid(row=3, column=0)
    tk.Label(info_window, text=pokemon.hit_power).grid(row=3, column=1)
    tk.Label(info_window, text="Defense:").grid(row=4, column=0)
    tk.Label(info_window, text=pokemon.defense).grid(row=4, column=1)
    # Add an image of the Pokemon to the window
    response = requests.get(pokemon.image_url)
    img = Image.open(io.BytesIO(response.content))
    img = img.resize((100, 100))
    img = ImageTk.PhotoImage(img)
    tk.Label(info_window, image=img).grid(row=0, column=2, rowspan=5, padx=10)
    player.pokemon_img = img  # save the img object as an instance variable
    cached_windows.append(info_window)
    return info_window


if __name__ == "__main__":
    # create the player's Pokemon
    print("Welcome to the Pokemon battle!")
