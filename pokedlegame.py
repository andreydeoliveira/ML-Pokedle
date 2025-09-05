import json
import random

class Pokedle:

    def __init__(self):
        with open("pokedle_data.json",'r', encoding="utf-8") as data:
            self.pokedata = json.load(data)

    def newgame(self):
        self.pokemondia = random.choice(self.pokedata)

    def setpokemon(self, name):
        self.pokemondia = next((p for p in self.pokedata if p["championName"] == name), None)

    def check(self, name):
        pokemonCheck = next((p for p in self.pokedata if p["championName"] == name), None)

        if (pokemonCheck is None):
            return None
                
        return (pokemonCheck["type1"] == self.pokemondia["type1"],
                pokemonCheck["type2"] == self.pokemondia["type2"],
                pokemonCheck["habitat"] == self.pokemondia["habitat"],
                pokemonCheck["color"] == self.pokemondia["color"],
                
                0 if pokemonCheck["evolutionStageGen1"] == self.pokemondia["evolutionStageGen1"] else -1 if int(pokemonCheck["evolutionStageGen1"]) < int(self.pokemondia["evolutionStageGen1"]) else 1,                
                0 if pokemonCheck["height"] == self.pokemondia["height"] else -1 if float(pokemonCheck["height"]) < float(self.pokemondia["height"]) else 1,                
                0 if pokemonCheck["weight"] == self.pokemondia["weight"] else -1 if float(pokemonCheck["weight"]) < float(self.pokemondia["weight"]) else 1)                

# Criando instância
# poke = Pokedle()
# poke.newgame()
# 
# 
# pokemon = input("Nome do pokemon: ")
# result = poke.check(pokemon)
# print(result)
# 
# while not all(result):
#     print("Pokemon errado")
#     pokemon = input("Nome do pokemon: ")
#     result = poke.check(pokemon)
#     print(result)
# 
# print("Acertou")

