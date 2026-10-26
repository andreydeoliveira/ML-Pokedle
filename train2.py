from pokedlegame import Pokedle
import numpy as np
import argparse
from tqdm import tqdm

parser = argparse.ArgumentParser(description="Treinamento do Pokedle Q-Learning")
parser.add_argument("--verbose", action="store_true", help="Exibe logs detalhados durante o treino")
args = parser.parse_args()

# ===========================
# Hiperparâmetros
# ===========================
alpha = 0.1
gamma = 0.99
epsilon = 0.99
epsilon_min = 0.01
epsilon_decay = 0.995
episodes = 150000  # Defina maior para treino real, ex: 500

poke_game = Pokedle()

lista_pokemons = [p['championName'] for p in poke_game.pokedata]
name_to_index = {name: i for i, name in enumerate(lista_pokemons)}

# def obterPalpite(lista_pokemons_podem_se_escolhidos):

def debugMessage(*valor):
    if args.verbose:
        print(*valor)


def pegaRemovePokemon(available_list, state, q_table, epsilon):
    if np.random.rand() < epsilon:
        # exploração: escolhe aleatório
        palpite = np.random.choice(list(available_list))
    else:

        indices_disponiveis = [name_to_index[name] for name in available_list]
        qvals = q_table[state][indices_disponiveis]
        indice_escolhido = indices_disponiveis[np.argmax(qvals)]
        palpite = lista_pokemons[indice_escolhido]
    
    available_list.discard(palpite)
    return name_to_index[palpite], palpite

def toTupla(valor):
    return (
        int(valor[0]),
        int(valor[1]),
        int(valor[2]),
        int(valor[3]),
        int(valor[4])+1,
        int(valor[5])+1,
        int(valor[6])+1
    )

q_table = np.zeros([2,2,2,2,3,3,3, len(lista_pokemons)])

bar = tqdm(lista_pokemons, desc='Treinando pokémon')
for pokemon in bar:
    bar.set_description(f"Treinando: {pokemon}")  # atualiza a barra
    for tentativas in range(episodes):    

        lista_pokemons_podem_se_escolhidos = set(lista_pokemons)

        #poke_game.newgame()    
        poke_game.setpokemon(pokemon)
        debugMessage(poke_game.pokemondia['championName'])

        done = False
        reward = 0
        valor_tupla = (0, 0, 0, 0, 1, 1, 1)

        qtd = 0
        while not done:
            qtd += 1
            indice_acao, palpite = pegaRemovePokemon(lista_pokemons_podem_se_escolhidos, valor_tupla, q_table, epsilon)

            state_atual = valor_tupla
            valor = poke_game.check(palpite)
            debugMessage(palpite, valor)

            if (valor == (True, True, True, True, 0, 0, 0)):
                reward = 1000
                done = True
                debugMessage(f"Acertou - Quantidade: {qtd}")
            else:
                peso_bool = 10     # menor que o final, mas significativo
                peso_num = 15      # ligeiramente maior que bool 

                # Atributos booleanos
                for i in range(4):
                    reward += peso_bool if valor[i] else -peso_bool

                # Atributos numéricos (considerando 0 como “acerto”)
                for i in range(4, 7):
                    reward += peso_num if valor[i] == 0 else -peso_num                       
            
            valor_tupla = toTupla(valor)         
            q_table[state_atual][indice_acao] += alpha * (
                reward + gamma * np.max(q_table[valor_tupla]) - q_table[state_atual][indice_acao]
            )

        epsilon = max(epsilon_min, epsilon * epsilon_decay)
    tqdm.write(f"Finalizado treinamento para {pokemon}")


np.save('q_table.npy', q_table)