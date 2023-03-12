import math
import random
import pandas as pd
import requests
from bs4 import BeautifulSoup



def pokedex(url = 'https://pokemondb.net/pokedex/all'):
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



#Define Pokemon Class that has three attributes:
#1) name    2) hit power   3) life points
class Pokemon:
    def __init__(self, chosen_pokemon_name):
        self.name = chosen_pokemon_name
        #info = pokedex.loc[pokedex['Name'] == chosen_pokemon_name]
        info = pokedex[pokedex['Name'] == chosen_pokemon_name].iloc[0]
        self.hit_power = int(info['Attack'])
        self.life_points = int(info['HP'])
        self.is_legendary = False

    #Create "say_hi" method to print pokemon's basic info (name, hit power, and life points)
    def say_hi(self):
        print(f"{self.name} says hello! {self.name} has {self.hit_power} hit power and {self.life_points} life points.")

    # "attack" method that reduces the enemy's life point by the attacking pokemon's hit power, and prints out the enemy's life point after attack.
    def attack(self, enemy):
        enemy.life_points = max(enemy.life_points - self.hit_power, 0)
        print(f"{self.name} attacks!")
        print(f"{enemy.name} loses life power!")
        print(f"{enemy.name} life power is {enemy.life_points}!")


#2. Define a child class (such as ElectricPokemon or WaterPokemon )
# that has a more powerful attack than usual attack (such as reduce the enemy's life points by double its hit power).
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

def create_enemy():
    enemy_pokemon = Pokemon(pokedex.sample()['Name'].iloc[0])
    print(f"The enemy is a {enemy_pokemon.name} with hit power {enemy_pokemon.hit_power} and life points {enemy_pokemon.life_points}.")
    return enemy_pokemon

# define a function to prompt the player to choose a Pokemon to use in the fight
def choose_pokemon():
    chosen_pokemon_name = input("What's your Pokemon's name? ")
    return Pokemon(chosen_pokemon_name)

pokedex = pokedex()
filter = pokedex['Name'].str.contains(" ")
pokedex = pokedex[~filter]
print(pokedex)

legendary_pokemon = ["Articuno", "Moltres", "Mewtwo", "Zapdos", "Lugia", "Ho-oh"]

if __name__ == "__main__":


    # create the player's Pokemon
    print("Welcome to the Pokemon battle!")
    print("Choose your Pokemon:")
    player_pokemon = choose_pokemon()
    enemy_pokemon = create_enemy()

    # print out their basic info
    player_pokemon.say_hi()
    enemy_pokemon.say_hi()

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






