import numpy as np
from pokedlegame import Pokedle

# ===========================
# Configurações
# ===========================
n_actions = 151
q_table_file = "q_table_pokedle.npy"

# Carrega Q-table treinada
q_table = np.load(q_table_file)

# Inicializa o jogo
poke_game = Pokedle()
#poke_game.newgame()
poke_game.setpokemon('Machop')

# Estado inicial fictício
state_idx = (0,0,0,0,1,1,1)

# Lista de ações disponíveis
available_actions = list(range(n_actions))

done = False
tentativas = 0
total_reward = 0

print("Jogo iniciado! Tentando adivinhar o Pokémon do dia...\n")

while not done and available_actions:
    # Escolher a ação com maior Q-value entre as disponíveis
    q_values = q_table[state_idx]
    available_q_values = {a: q_values[a] for a in available_actions}
    action = max(available_q_values, key=available_q_values.get)
    available_actions.remove(action)
    
    # Fazer o palpite
    guess_name = poke_game.pokedata[action]["championName"]
    check_result = poke_game.check(guess_name)
    
    # Atualiza estado
    state_idx = tuple([int(val) if i<4 else val+1 for i, val in enumerate(check_result)])
    
    # Contagem de tentativas e recompensa
    tentativas += 1
    reward = sum([1 if (check_result[i]==0 if i>=4 else check_result[i]) else 0 for i in range(7)])
    total_reward += reward
    
    # Verifica se acertou todos os atributos
    done = all([check_result[i] for i in range(4)]) and all([check_result[i]==0 for i in range(4,7)])
    
    print(f"Tentativa {tentativas}: {guess_name} | Resultado: {check_result} | Recompensa: {reward}")

# Resultado final
if done:
    print(f"\nParabéns! O Pokémon era {poke_game.pokemondia['championName']}. Acertou em {tentativas} tentativas!")
else:
    print(f"\nAcabaram as ações disponíveis! O Pokémon era {poke_game.pokemondia['championName']}. Total de tentativas: {tentativas}")
