import requests
from config import OMDB_API_KEY, BASE_URL

#def search_movies(query):
#  response = requests.get(BASE_URL, params={"apikey": OMDB_API_KEY, "s": query})
#    data = response.json()
#    if data.get("Response") == "True":
#        return data["Search"]
#    return []



def search_movies(query):
    #Buscamos pelis por nombre y devolvemos una lista de diccionarios
    params = {
        "apikey": OMDB_API_KEY,
        "s": query
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if data.get("Response") == "False":
        return []

    resultados = []

    for item in data.get("Search", []):
        imdb_id = item.get("imdbID") #para las estadisticas
        detalle = get_movie_detail(imdb_id)
        if detalle:
            resultados.append(detalle)

    return resultados


def get_movie_detail(imdb_id):
    #detalle completo de la peli
    params = {
        "apikey": OMDB_API_KEY,
        "i": imdb_id,
        "plot": "short"
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if data.get("Response") == "False":
        return None

    return {
        "Title": data.get("Title"),
        "Year": data.get("Year"),
        "Type": data.get("Type"),
        "imdbRating": data.get("imdbRating"),
        "imdbVotes": data.get("imdbVotes"),
        "Metascore": data.get("Metascore")
    }