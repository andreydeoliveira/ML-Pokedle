import requests
from sklearn.cluster import KMeans
from io import BytesIO
from PIL import Image
import numpy as np

# Lista de cores permitidas e seus valores RGB aproximados
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

def downloadImage(pokemon_nome):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_nome.lower()}"
    payload = requests.get(url)
    dados = payload.json()
    url_img = dados["sprites"]["other"]["official-artwork"]["front_default"]
    payload = requests.get(url_img)
    png_data = payload.content
    return png_data

def get_dominant_named_colors(png_data, n_clusters=5, threshold=0.15):
    img = Image.open(BytesIO(png_data)).convert('RGBA')
    img = img.resize((100, 100))
    pixels = np.array(img)
    mask = pixels[:, :, 3] > 0
    pixels_rgb = pixels[:, :, :3][mask]

    if len(pixels_rgb) == 0:
        return []

    kmeans = KMeans(n_clusters=n_clusters, n_init='auto')
    kmeans.fit(pixels_rgb)
    labels, counts = np.unique(kmeans.labels_, return_counts=True)
    total_pixels = len(pixels_rgb)
    percentages = counts / total_pixels

    named_colors = {}
    for label, percent in zip(labels, percentages):
        print(f"Cluster: {label}, Percentual: {percent*100:.2f}%")  # debug aqui
        if percent >= threshold:
            rgb = kmeans.cluster_centers_[label].astype(int)
            name = rgb_to_named_color(rgb)
            named_colors[name] = named_colors.get(name, 0) + percent

    return named_colors

# Uso
png_data = downloadImage('tentacruel')
named_colors = get_dominant_named_colors(png_data)

print("Cores dominantes mapeadas:")
for color_name, percent in named_colors.items():
    print(f"{color_name.capitalize()}: {percent*100:.2f}%")
