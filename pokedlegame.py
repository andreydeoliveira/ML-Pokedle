import json
import random

class Pokedle:

    def __init__(self):
        with open("pokedle_data.json",'r', encoding="utf-8") as data:
            self.pokedata = json.load(data)

    def newgame(self):
        self.pokemondia = random.choice(self.pokedata)

    def check(self, name):
        pokemonCheck = next((p for p in self.pokedata if p["championName"] == name), None)

        if (pokemonCheck == None):
            return None
                
        return (pokemonCheck["type1"] == self.pokemondia["type1"],
                pokemonCheck["type2"] == self.pokemondia["type2"],
                pokemonCheck["habitat"] == self.pokemondia["habitat"],
                pokemonCheck["color"] == self.pokemondia["color"],
                pokemonCheck["evolutionStage"] == self.pokemondia["evolutionStage"],
                pokemonCheck["height"] == self.pokemondia["height"],
                pokemonCheck["weight"] == self.pokemondia["weight"])
                

# Criando instância
poke = Pokedle()
poke.newgame()

# Mostrando só o nome
print(poke.pokemondia["championName"])

print('-------')

lista = ['Poliwrath', 'Arcanine', 'Patolino', poke.pokemondia["championName"]]

for data in lista:
    result = poke.check(data)
    if (result == None):
        print(f'Pokémon não encontrado: {data}')
    elif (all(result)):
        print(f'Pokémon encontrado: {data}')
        break
    else:
        print(result)
