from pokedlegame import Pokedle
import numpy as np

# ===========================
# Hiperparâmetros
# ===========================
alpha = 0.1
gamma = 0.99
epsilon = 0.99
epsilon_min = 0.01
epsilon_decay = 0.995
episodes = 15000  # Defina maior para treino real, ex: 500

poke_game = Pokedle()

lista_pokemons = [p['championName'] for p in poke_game.pokedata]
name_to_index = {name: i for i, name in enumerate(lista_pokemons)}

# def obterPalpite(lista_pokemons_podem_se_escolhidos):

def pegaRemovePokemon(available_list, state, q_table, epsilon):
    if np.random.rand() < epsilon:
        # exploração: escolhe aleatório
        palpite = np.random.choice(available_list)
    else:

        indices_disponiveis = [name_to_index[name] for name in available_list]
        qvals = q_table[state][indices_disponiveis]
        indice_escolhido = indices_disponiveis[np.argmax(qvals)]
        palpite = lista_pokemons[indice_escolhido]
    
    available_list.remove(palpite)
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

for pokemon in lista_pokemons:
    for tentativas in range(episodes):    

        lista_pokemons_podem_se_escolhidos = lista_pokemons.copy()

        #poke_game.newgame()    
        poke_game.setpokemon(pokemon)
        print(poke_game.pokemondia['championName'])

        done = False
        reward = 0
        valor_tupla = (0, 0, 0, 0, 1, 1, 1)

        qtd = 0
        while not done:
            qtd += 1
            indice_acao, palpite = pegaRemovePokemon(lista_pokemons_podem_se_escolhidos, valor_tupla, q_table, epsilon)

            state_atual = valor_tupla
            valor = poke_game.check(palpite)
            print(palpite, valor)

            if (valor == (True, True, True, True, 0, 0, 0)):
                reward = 1000
                done = True
                print(f"Acertou - Quantidade: {qtd}")
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


np.save('q_table.npy', q_table)