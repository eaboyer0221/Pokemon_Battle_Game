

import tkinter as tk

#main window of game
root = tk.Tk()
root.title("Pokemon Battle")

#labels to display the player's and enemy's basic information
player_info = tk.Label(root, text=f"{player_pokemon.name} - Hit Power: {player_pokemon.hit_power} - Life Points: {player_pokemon.life_points}")
player_info.pack()

enemy_info = tk.Label(root, text=f"{enemy_pokemon.name} - Hit Power: {enemy_pokemon.hit_power} - Life Points: {enemy_pokemon.life_points}")
enemy_info.pack()

#buttons for the player to attack or quit the game:
def attack():
    player_pokemon.attack(enemy_pokemon)
    player_info.config(text=f"{player_pokemon.name} - Hit Power: {player_pokemon.hit_power} - Life Points: {player_pokemon.life_points}")
    enemy_info.config(text=f"{enemy_pokemon.name} - Hit Power: {enemy_pokemon.hit_power} - Life Points: {enemy_pokemon.life_points}")
    if enemy_pokemon.life_points <= 0:
        result.config(text=f"{enemy_pokemon.name} fainted. {player_pokemon.name} won the battle!")
        attack_btn.config(state="disabled")
    else:
        enemy_attack()

def enemy_attack():
    enemy_pokemon.attack(player_pokemon)
    player_info.config(text=f"{player_pokemon.name} - Hit Power: {player_pokemon.hit_power} - Life Points: {player_pokemon.life_points}")
    enemy_info.config(text=f"{enemy_pokemon.name} - Hit Power: {enemy_pokemon.hit_power} - Life Points: {enemy_pokemon.life_points}")
    if player_pokemon.life_points <= 0:
        result.config(text=f"{player_pokemon.name} fainted. {enemy_pokemon.name} won the battle!")
        attack_btn.config(state="disabled")

attack_btn = tk.Button(root, text="Attack", command=attack)
attack_btn.pack()

quit_btn = tk.Button(root, text="Quit", command=root.destroy)
quit_btn.pack()

#label to display the result of the game
result = tk.Label(root, text="")
result.pack()


