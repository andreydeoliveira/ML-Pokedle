import requests
from PIL import Image
from io import BytesIO
from sklearn.cluster import KMeans
import numpy as np

COR_ALVO = {
    "blue": [(0, 0, 255), (30, 144, 255), (70, 130, 180)],
    "red": [(255, 0, 0), (178, 34, 34)],
    "yellow": [(255, 255, 0), (255, 215, 0)],
    "purple": [(128, 0, 128), (148, 0, 211)],
    "brown": [(139, 69, 19), (160, 82, 45)],
    "black": [(0, 0, 0), (40, 40, 40)],
    "gray": [(128, 128, 128), (169, 169, 169)],
    "white": [(255, 255, 255), (245, 245, 245)],
    "pink": [(255, 192, 203), (255, 105, 180)],
    "green": [(0, 128, 0), (60, 179, 113)],
}

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

def remover_fundo(imagem, cor_fundo=(230, 230, 230), tolerancia=10):
    pixels = np.array(imagem)
    diff = np.abs(pixels - np.array(cor_fundo))
    mask = np.any(diff > tolerancia, axis=-1)  # True para pixels que não são fundo
    pixels_sem_fundo = pixels[mask]
    return pixels_sem_fundo

def cor_mais_proxima(rgb):
    menor_distancia = float('inf')
    cor_aproximada = None
    for nome, tons in COR_ALVO.items():
        for ref_rgb in tons:
            dist = sum((a - b) ** 2 for a, b in zip(rgb, ref_rgb))
            if dist < menor_distancia:
                menor_distancia = dist
                cor_aproximada = nome
    return cor_aproximada

def cores_dominantes(pixels, num_cores=5):
    modelo = KMeans(n_clusters=num_cores, random_state=42)
    modelo.fit(pixels)
    contagem = np.bincount(modelo.labels_)
    total = len(pixels)

    resultado = []
    for i, centro in enumerate(modelo.cluster_centers_.astype(int)):
        percentual = contagem[i] / total
        if percentual >= 0.25:
            cor_nome = cor_mais_proxima(tuple(centro))
            resultado.append((cor_nome, percentual))
    return resultado

def salvar_imagem_sem_fundo(imagem, cor_fundo=(230, 230, 230), tolerancia=10, nome_arquivo="sem_fundo.png"):
    imagem = imagem.convert("RGBA")
    dados = np.array(imagem)

    r, g, b, a = dados.T
    fundo = (
        (np.abs(r - cor_fundo[0]) <= tolerancia) &
        (np.abs(g - cor_fundo[1]) <= tolerancia) &
        (np.abs(b - cor_fundo[2]) <= tolerancia)
    )

    dados[..., 3][fundo] = 0  # define alpha como 0 (transparente) para os pixels de fundo

    imagem_sem_fundo = Image.fromarray(dados)
    imagem_sem_fundo.save(nome_arquivo)
    print(f"🖼️ Imagem sem fundo salva como: {nome_arquivo}")


def analisar_cores_pokemon(pokemon_nome):
    print(f"\n🎨 Analisando: {pokemon_nome}")
    imagem = baixar_imagem_oficial(pokemon_nome)

    salvar_imagem_sem_fundo(imagem, nome_arquivo=f"{pokemon_nome}.png")

    pixels = remover_fundo(imagem)

    cores = cores_dominantes(pixels)

    if not cores:
        print("Nenhuma cor dominante encontrada com pelo menos 25%.")
    else:
        for cor, percentual in cores:
            print(f"Cor: {cor} ({percentual:.0%})")
    salvar_imagem_sem_fundo(imagem, nome_arquivo=f"{pokemon_nome}_sem_fundo.png")

# Testar novamente
analisar_cores_pokemon("tentacruel")
