import requests
from PIL import Image
from io import BytesIO
from sklearn.cluster import KMeans
import numpy as np
import webcolors

def baixar_imagem_oficial(pokemon_nome):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_nome.lower()}"    
    resposta = requests.get(url)
    if resposta.status_code != 200:
        raise Exception(f"Erro ao buscar {pokemon_nome}")
    
    dados = resposta.json()
    url_img = dados["sprites"]["other"]["official-artwork"]["front_default"]
    print(url_img)
    img_bytes = requests.get(url_img).content
    return Image.open(BytesIO(img_bytes)).convert('RGB')

def cores_dominantes(imagem, num_cores=2):
    imagem = imagem.resize((100, 100))
    pixels = np.array(imagem).reshape(-1, 3)

    modelo = KMeans(n_clusters=num_cores, random_state=42)
    modelo.fit(pixels)

    cores = modelo.cluster_centers_.astype(int)
     # converte para tupla de int padrão do Python
    return [tuple(int(c) for c in cor) for cor in cores]

def analisar_cores_pokemon(pokemon_nome):
    print(f"\n🎨 Analisando: {pokemon_nome}")
    imagem = baixar_imagem_oficial(pokemon_nome)
    cores = cores_dominantes(imagem)

    for i, cor in enumerate(cores, start=1):        
        print(f"Cor {i}: RGB{cor}")

# Exemplo:
analisar_cores_pokemon("tentacruel")
