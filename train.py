import numpy as np
from pokedlegame import Pokedle
import time

start_time = time.time()

# ===========================
# Hiperparâmetros
# ===========================
alpha = 0.1
gamma = 0.99
epsilon = 0.99
epsilon_min = 0.01
epsilon_decay = 0.995
episodes = 150000  # Defina maior para treino real, ex: 500

n_actions = 151  # número de pokémons possíveis

# Inicializa Q-table: 4 atributos categóricos (2 valores) + 3 atributos numéricos (-1,0,1 -> 3 valores) + n_actions
q_table = np.zeros([2,2,2,2,3,3,3,n_actions])

# ===========================
# Funções
# ===========================

def state_to_index(check_result):
    """Converte o retorno do check() em índices para Q-table"""
    indices = []
    for i, val in enumerate(check_result):
        if i < 4:  # atributos categóricos: True/False → 0/1
            indices.append(int(val))
        else:      # atributos numéricos: -1,0,1 → 0,1,2
            indices.append(val + 1)
    return tuple(indices)

def choose_action(state_idx, epsilon_local, available_actions):
    """Escolhe ação ε-greedy entre as disponíveis"""
    # Verifica se ainda há ações disponíveis
    if not available_actions:
        return None
        
    if np.random.rand() < epsilon_local:
        action = np.random.choice(available_actions)
    else:
        q_values = q_table[state_idx]
        # Seleciona apenas Q-values das ações disponíveis
        available_q_values = {a: q_values[a] for a in available_actions}
        if not available_q_values:  # Verifica se o dicionário não está vazio
            action = np.random.choice(available_actions)
        else:
            action = max(available_q_values, key=available_q_values.get)

    available_actions.remove(action)
    return action

# ===========================
# Treinamento
# ===========================

for ep in range(episodes):
    poke_game = Pokedle()
    poke_game.newgame()
    done = False
    total_reward = 0
    epsilon_local = epsilon
    
    # Lista de ações disponíveis no episódio
    available_actions = list(range(n_actions))

    # Estado inicial fictício
    state_idx = (0,0,0,0,1,1,1)

    while not done:
        # Verificar se ainda há ações disponíveis
        if not available_actions:
            print(f"Sem mais ações disponíveis no episódio {ep+1}")
            break
            
        # Escolher ação
        action = choose_action(state_idx, epsilon_local, available_actions)
        
        # Verificar se a ação é válida
        if action is None:
            print(f"Nenhuma ação válida retornada no episódio {ep+1}")
            break

        # Fazer o palpite
        guess_name = poke_game.pokedata[action]["championName"]
        check_result = poke_game.check(guess_name)

        # Transformar estado em índice
        next_state_idx = state_to_index(check_result)

        # Recompensa: quantos atributos acertou
        # Para atributos categóricos (0-3): True = acertou, False = errou
        # Para atributos numéricos (4-6): 0 = acertou, -1/1 = errou
        categorical_correct = sum([1 if check_result[i] else 0 for i in range(4)])
        numerical_correct = sum([1 if check_result[i] == 0 else 0 for i in range(4, 7)])
        reward = categorical_correct + numerical_correct
        
        # Bônus se acertou tudo
        if all([check_result[i] for i in range(4)]) and all([check_result[i] == 0 for i in range(4, 7)]):
            reward += 10  # Bônus por acertar o Pokémon
            
        total_reward += reward

        # Atualizar Q-table
        q_table[state_idx][action] = q_table[state_idx][action] + alpha * (
            reward + gamma * np.max(q_table[next_state_idx]) - q_table[state_idx][action]
        )

        # Próximo estado
        state_idx = next_state_idx

        # Verifica se acertou todos os atributos
        # Categóricos devem ser True, numéricos devem ser 0
        categorical_correct = all([check_result[i] for i in range(4)])
        numerical_correct = all([check_result[i] == 0 for i in range(4, 7)])
        done = categorical_correct and numerical_correct

        # Decai epsilon local
        epsilon_local = max(epsilon_min, epsilon_local * epsilon_decay)

    # Atualiza epsilon global
    epsilon = epsilon_local
    
    # Informações do episódio
    status = "VENCEU" if done else "SEM AÇÕES" if not available_actions else "INCOMPLETO"
    # print(f"Episódio {ep+1}: {status} | Recompensa: {total_reward} | Epsilon: {epsilon:.3f} | Tentativas: {151-len(available_actions)}")

end_time = time.time()

training_time = end_time - start_time
print(f"Tempo de treinamento: {training_time:.2f} segundos")

# Salvar a Q-table treinada
np.save("q_table_pokedle.npy", q_table)
print("Treinamento finalizado e Q-table salva em q_table_pokedle.npy")
