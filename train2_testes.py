from pokedlegame import Pokedle
import numpy as np

# Carrega Q-table treinada
q_table = np.load('q_table.npy')

poke_game = Pokedle()
lista_pokemons = [p['championName'] for p in poke_game.pokedata]
name_to_index = {name: i for i, name in enumerate(lista_pokemons)}

available_list = lista_pokemons.copy()

valor_tupla = (0, 0, 0, 0, 1, 1, 1)

indices_disponiveis = [name_to_index[name] for name in available_list]
qvals = q_table[valor_tupla][indices_disponiveis]
indice_escolhido = indices_disponiveis[np.argmax(qvals)]
palpite = lista_pokemons[indice_escolhido]

print(palpite)