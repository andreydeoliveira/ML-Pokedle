from pokedlegame import Pokedle # importa sua classe do arquivo onde ela está

poke = Pokedle()
poke.newgame()

print("Novo jogo iniciado! Tente adivinhar o Pokémon.")
print("Dicas: type1, type2, habitat, color, evolução(-1/0/1), altura(-1/0/1), peso(-1/0/1)")

while True:
    pokemon = input("\nNome do Pokémon: ").strip()
    result = poke.check(pokemon)

    if result is None:
        print("Pokémon não encontrado. Tente novamente.")
        continue

    print("Resultado:", result)

    # Verifica se acertou todos
    acertou = (
        result[0] == True and
        result[1] == True and
        result[2] == True and
        result[3] == True and
        result[4] == 0 and
        result[5] == 0 and
        result[6] == 0
    )

    if acertou:
        print("🎉 Acertou! Era o", poke.pokemondia["championName"])
        break
    else:
        print("❌ Ainda não é esse Pokémon!")