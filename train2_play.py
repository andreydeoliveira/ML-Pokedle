from pokedlegame import Pokedle
import numpy as np

# Carrega Q-table treinada
q_table = np.load('q_table.npy')

poke_game = Pokedle()
lista_pokemons = [p['championName'] for p in poke_game.pokedata]
name_to_index = {name: i for i, name in enumerate(lista_pokemons)}

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

# Começa um novo jogo
#poke_game.newgame()  # se existir esse método
# ou definir manualmente
#poke_game.setpokemon(lista_pokemons[0])  # exemplo, pega o primeiro Pokémon
#poke_game.newgame()
poke_game.setpokemon('Oddish')

# Lista de Pokémon disponíveis
available_list = lista_pokemons.copy()

done = False
valor_tupla = (0, 0, 0, 0, 1, 1, 1)
qtd = 0
while not done:
    qtd += 1

    # Escolhe a melhor ação da Q-table (greedy)
    indices_disponiveis = [name_to_index[name] for name in available_list]
    qvals = q_table[valor_tupla][indices_disponiveis]
    indice_escolhido = indices_disponiveis[np.argmax(qvals)]
    palpite = lista_pokemons[indice_escolhido]

    # Remove da lista de disponíveis
    available_list.remove(palpite)

    # Faz o palpite no jogo
    valor = poke_game.check(palpite)
    print(f"Palpite: {palpite}, Feedback: {valor}")

    # Atualiza estado
    valor_tupla = toTupla(valor)

    # Se acertou, termina
    if valor == (True, True, True, True, 0, 0, 0):
        print(f"Acertou o Pokémon! Tentativas: {qtd}")
        done = True        
    else:
        print(palpite)

    # Se acabar lista sem acerto, termina
    if not available_list:
        print("Todos os palpites foram usados. Fim do jogo.")
        done = True
