
import requests
import json
import os

class Pokemon:    
    def __init__(self):
        self.id = None
        self.name = None
        self.tipo1 = None
        self.tipo2 = None
        self.habitat = None
        self.cor = None
        self.evol = None
        self.altura = None
        self.peso = None

    def toJSON(self):
        return json.dumps(self.__dict__, indent=4)
    
def get_evolution_stage(pokemon_name, species_data):
    # Pega URL da cadeia evolutiva
    evo_url = species_data['evolution_chain']['url']
    evo_data = requests.get(evo_url).json()

    # Percorre a cadeia e conta em que fase o Pokémon está
    stage = 1
    chain = evo_data['chain']
    
    while True:
        if chain['species']['name'] == pokemon_name:
            return stage
        elif chain['evolves_to']:
            chain = chain['evolves_to'][0]
            stage += 1
        else:
            return None  # Não encontrado na cadeia


id = 0

pokelist = []

for id in range(1,152):
    url_pokeapi = f'https://pokeapi.co/api/v2/pokemon/{id}'

    response = requests.get(url_pokeapi)
    data = response.json()
    
    pokemon = Pokemon()

    pokemon.id = id
    pokemon.name = data['name']
    pokemon.tipo1 = data['types'][0]['type']['name']
    if len(data['types']) > 1:
        pokemon.tipo2 = data['types'][1]['type']['name']
    
    species = requests.get(f'https://pokeapi.co/api/v2/pokemon-species/{id}/').json()
    pokemon.habitat = species['habitat']['name']
 
    pokemon.cor = species['color']['name']

    pokemon.evol = get_evolution_stage(pokemon_name=pokemon.name, species_data=species)

    pokemon.altura = f'{data['height']}0'
    pokemon.peso = data['weight']*10

    pokelist.append(pokemon)

with open('pokemon_list.json', 'w') as f:
    f.write(json.dumps([p.__dict__ for p in pokelist], indent=4))
