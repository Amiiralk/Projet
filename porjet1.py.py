# -*- coding: utf-8 -*-
"""Untitled12.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1OtHMMijGOHGNTz3bUUrm0Q1JS-0x5lH_
"""

import threading
import random
import time

GRID_SIZE = 5
NUM_PLAYERS = 2

# Structures et constantes
class Player:
    def __init__(self, player_id):
        self.player_id = player_id
        self.grid = [[random.choice([0, 1]) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.is_alive = True

# Initialisation des joueurs
players = [Player(i) for i in range(NUM_PLAYERS)]
grid_locks = [threading.Lock() for _ in range(NUM_PLAYERS)]

# Affiche la grille d'un joueur
def print_grid(player):
    print(f"Grille du joueur {player.player_id}:")
    for row in player.grid:
        print(" ".join(str(cell) for cell in row))
    print()

# Fonction pour tirer sur la grille d'un autre joueur
def fire(attacker, target_id, x, y):
    with grid_locks[target_id]:
        target = players[target_id]
        hit = False
        if target.grid[x][y] == 1:
            target.grid[x][y] = -1  # -1 indique un bateau touché
            hit = True
            print(f"Joueur {attacker.player_id} a touché le joueur {target_id} en ({x}, {y})!")
        else:
            print(f"Joueur {attacker.player_id} a raté le joueur {target_id} en ({x}, {y}).")
        return hit

# Vérifie si un joueur est encore en jeu
def check_alive(player):
    for row in player.grid:
        if 1 in row:
            return True
    player.is_alive = False
    return False

# Fonction pour chaque joueur (thread)
def player_turn(player):
    target_id = (player.player_id + 1) % NUM_PLAYERS

    while player.is_alive and players[target_id].is_alive:
        x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        fire(player, target_id, x, y)

        if not check_alive(players[target_id]):
            print(f"Joueur {player.player_id} a gagné!")
            break
        time.sleep(1)

# Main
def main():
    print("Initialisation des grilles :")
    for player in players:
        print_grid(player)

    threads = []
    for player in players:
        thread = threading.Thread(target=player_turn, args=(player,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("Fin de la partie.")

if __name__ == "__main__":
    main()