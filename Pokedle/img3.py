import requests
import cv2
import numpy as np
from sklearn.cluster import KMeans
from collections import defaultdict

accepted_colors = {
    "blue": [0, 0, 255],
    "red": [255, 0, 0],
    "yellow": [255, 255, 0],
    "purple": [128, 0, 128],
    "brown": [139, 69, 19],
    "black": [0, 0, 0],
    "gray": [128, 128, 128],
    "white": [255, 255, 255],
    "pink": [255, 192, 203],
    "green": [0, 128, 0],
}

def rgb_to_named_color(rgb):
    rgb = np.array(rgb)
    min_dist = float('inf')
    closest_color = None
    for name, ref_rgb in accepted_colors.items():
        dist = np.linalg.norm(rgb - ref_rgb)
        if dist < min_dist:
            min_dist = dist
            closest_color = name
    return closest_color

def downloadPokemon(pokemon_nome):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_nome.lower()}"
    payload = requests.get(url)
    dados = payload.json()
    url_img = dados["sprites"]["other"]["official-artwork"]["front_default"]
    payload = requests.get(url_img)
    png_data = payload.content
    return png_data

def get_dominant_named_colors(image_path, k=10, threshold=0.05, save_filtered_path=None):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pixels = img.reshape(-1, 3)

    # Filtra pixels muito claros e muito escuros (quase branco e preto)
    mask = (
        (pixels[:, 0] > 20) & (pixels[:, 0] < 235) &
        (pixels[:, 1] > 20) & (pixels[:, 1] < 235) &
        (pixels[:, 2] > 20) & (pixels[:, 2] < 235)
    )
    filtered_pixels = pixels[mask]

    # Salva imagem filtrada, reconstruindo a imagem para visualização
    if save_filtered_path:
        filtered_img = np.zeros_like(pixels)
        filtered_img[mask] = pixels[mask]
        filtered_img = filtered_img.reshape(img.shape)
        filtered_img = cv2.cvtColor(filtered_img, cv2.COLOR_RGB2BGR)
        cv2.imwrite(save_filtered_path, filtered_img)

    if len(filtered_pixels) == 0:
        filtered_pixels = pixels  # fallback

    kmeans = KMeans(n_clusters=k, random_state=0, n_init='auto')
    kmeans.fit(filtered_pixels)

    labels, counts = np.unique(kmeans.labels_, return_counts=True)
    total_pixels = len(filtered_pixels)

    color_weights = defaultdict(float)

    for label, count in zip(labels, counts):
        percent = count / total_pixels
        if percent < threshold:
            continue

        rgb = kmeans.cluster_centers_[label].astype(int)
        named_color = rgb_to_named_color(rgb)
        color_weights[named_color] += percent

    sorted_colors = sorted(color_weights.items(), key=lambda x: x[1], reverse=True)
    return sorted_colors

# Uso
pokemon = 'tentacruel'
pokedata = downloadPokemon(pokemon)
filename = f"{pokemon}.png"
with open(filename, 'wb') as f:
    f.write(pokedata)

dominant_named_colors = get_dominant_named_colors(filename, k=10, threshold=0.05, save_filtered_path=f"{pokemon}_filtered.png")
print("Cores dominantes (nome e percentual):")
for color, pct in dominant_named_colors:
    print(f"{color.capitalize()}: {pct*100:.2f}%")
