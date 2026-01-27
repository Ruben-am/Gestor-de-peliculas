# omdb_api.py
import requests
from config import OMDB_API_KEY, BASE_URL

def search_movies(query):
    #Buscamos pelis por nombre y devolvemos una lista de diccionarios
    response = requests.get(BASE_URL, params={"apikey": OMDB_API_KEY, "s": query})
    data = response.json()
    if data.get("Response") == "True":
        return data["Search"]
    return []