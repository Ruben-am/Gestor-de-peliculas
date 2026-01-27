# main.py
from omdb_api import search_movies
import pandas as pd

query = "Avatar"
movies = search_movies(query)

print(movies)

df = pd.DataFrame(movies)
df.to_csv("movies.csv", index=False)
print("CSV creado con éxito!")
