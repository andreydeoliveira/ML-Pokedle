import requests
from sklearn.cluster import KMeans


def downloadImage(pokemon_nome):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_nome.lower()}"

    payload = requests.get(url)

    dados = payload.json()
    url_img = dados["sprites"]["other"]["official-artwork"]["front_default"]
    
    payload = requests.get(url_img)
    png_data = payload.content

    #with open(f"{pokemon_nome}.png", 'wb') as f:
        #f.write(payload.content)
    print(f"PNG image data successfully retrieved and stored in 'png_data' variable.")
    print(f"Type of png_data: {type(png_data)}")
    print(f"Size of png_data (bytes): {len(png_data)}")



downloadImage('tentacruel')
