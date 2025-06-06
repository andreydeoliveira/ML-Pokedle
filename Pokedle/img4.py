import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
from collections import Counter
import colorsys

# === Função para converter RGB para HSV normalizado (0-1) ===
def rgb_to_hsv(rgb):
    r, g, b = rgb / 255
    return colorsys.rgb_to_hsv(r, g, b)  # h, s, v ∈ [0, 1]

# === Mapeia HSV para cor básica humana ===
def map_to_visual_color(rgb):
    h, s, v = rgb_to_hsv(rgb)

    if v < 0.2:
        return "black"
    elif v > 0.85 and s < 0.2:
        return "white"
    elif s < 0.25:
        return "gray"
    
    if h < 0.04 or h > 0.96:
        return "red"
    elif h < 0.10:
        return "orange"
    elif h < 0.17:
        return "yellow"
    elif h < 0.45:
        return "green"
    elif h < 0.55:
        return "cyan"
    elif h < 0.75:
        return "blue"
    elif h < 0.90:
        return "purple"
    else:
        return "pink"

# === Carrega imagem RGBA ===
image = Image.open("tentacruel.png").convert("RGBA")
data = np.array(image)

# === Separa canais RGBA ===
r, g, b, a = data[..., 0], data[..., 1], data[..., 2], data[..., 3]

# === Máscara para remover fundo transparente ===
mask = a > 0
visible_pixels = np.stack([r[mask], g[mask], b[mask]], axis=1)

# === KMeans para detectar cores dominantes ===
kmeans = KMeans(n_clusters=6, random_state=0)
kmeans.fit(visible_pixels)
labels = kmeans.labels_

# === Mapeia centros para cores visuais básicas ===
color_names = [map_to_visual_color(center) for center in kmeans.cluster_centers_]

# === Conta frequência de cada cor ===
basic_color_counts = Counter()
for label in labels:
    basic_color = color_names[label]
    basic_color_counts[basic_color] += 1

# === Total de pixels visíveis ===
total_visible = len(visible_pixels)

# === Resultado ===
print("Cores básicas na imagem (ignorando fundo transparente):\n")
for color, count in basic_color_counts.items():
    percent = (count / total_visible) * 100
    print(f"- {color}: {percent:.2f}% da área visível")
