import pandas as pd
import matplotlib.pyplot as plt
from omdb_api import search_movies

# Variable global para guardar los datos en memoria
df = pd.DataFrame()

def cargar_datos():
    # Carga un archivo csv o excel
    global df
    nombre = input("Nombre del archivo (nombre.csv / nombre.xlsx): ")
    try:
        if nombre.endswith(".csv"):
            df = pd.read_csv(nombre)
        elif nombre.endswith(".xlsx"):
            df = pd.read_excel(nombre)
        print(f"Cargados {len(df)} elementos")
    except:
        print("archivo no encontrado o formato incorrecto")

def seleccionar_pelicula():
    #funcion secundaria para la funcion de graficos
    if df.empty:
        print("No hay datos cargados")
        return None

    titulo = input("Introduce el titulo de la pelicula: ")

    filtrado = df[df['Title'].str.contains(titulo, case=False, na=False)]

    if filtrado.empty:
        print("No se encontraron peliculas con ese titulo")
        return None

    return filtrado


def graficos():
    #muestra un grafico de una pelicula, pero antes hay q importar un archivo o hacer una consulta a la api
    datos = seleccionar_pelicula()
    if datos is None:
        return

    datos['imdbRating'] = pd.to_numeric(datos['imdbRating'], errors='coerce')

    print(" ----------- GRAFICOS DE ACEPTACION ----------- ")
    print("1. Histograma de ratings")
    print("2. Evolucion del rating por año")
    opcion = input("Elige grafico: ")

    # grafico en horganigrama
    if opcion == "1":
        datos['imdbRating'].dropna().plot(kind='hist', bins=5)
        plt.title("Distribucion del rating IMDb")
        plt.xlabel("Rating")
        plt.ylabel("Cantidad")
        plt.tight_layout()
        plt.show()

    # grafico en linea
    elif opcion == "2" and 'Year' in datos.columns:
        datos['Year_Num'] = pd.to_numeric(datos['Year'], errors='coerce')
        datos.sort_values('Year_Num').plot(
            x='Year_Num',
            y='imdbRating',
            kind='line',
            marker='o'
        )
        plt.title("Evolucion del rating por año")
        plt.xlabel("Año")
        plt.ylabel("Rating IMDb")
        plt.tight_layout()
        plt.show()

    else:
        print("No se puede generar el grafico")


def estadisticas():
    datos = seleccionar_pelicula()
    if datos is None:
        return

    print(" ----------- ESTADISTICAS DE ACEPTACION ----------- ")

    if 'imdbRating' in datos.columns:
        datos['imdbRating'] = pd.to_numeric(datos['imdbRating'], errors='coerce')

        print(f"Numero de registros: {len(datos)}")
        print(f"Rating medio: {datos['imdbRating'].mean():.2f}")
        print(f"Rating maximo: {datos['imdbRating'].max()}")
        print(f"Rating minimo: {datos['imdbRating'].min()}")

    if 'Year' in datos.columns:
        print("\nAños disponibles:")
        print(datos['Year'].unique())

def buscar_y_annadir():
    global df
    buscar = input("Pelicula a buscar: ")
    resultados = search_movies(buscar)
    
    if resultados:
        nuevoDf = pd.DataFrame(resultados)
        if df.empty:
            df = nuevoDf
        else:
            df = pd.concat([df, nuevoDf], ignore_index=True)
        print(f"peliculas añadidas")
    else:
        print("No se encontraron resultados")

def ver_datos():
    # Muestra los datos y permite filtrar
    if df.empty:
        print("No hay datos carga un archivo o busca en la API")
        return

    print("1. Ver todo")
    print("2. Filtrar por Título (Buscar)")
    opcion = input("Opcion: ")

    if opcion == "1":
        print(df)
    elif opcion == "2":
        texto = input("Introduce texto a buscar: ")
        filtro = df[df['Title'].str.contains(texto, case=False, na=False)]
        print(filtro)


def exportar_csv():
    # Guarda los datos en un archivo csv
    if df.empty:
        print("No hay datos para guardar")
        return
    nombre = input("Nombre del archivo (resultado.csv): ")
    if 'Year_Num' in df.columns:
        dfFinal = df.drop(columns=['Year_Num'])
    else:
        dfFinal = df
        
    dfFinal.to_csv(nombre, index=False)
    print("Archivo guardado correctamente")

def menu():
    while True:
        print(" ----------- GESTOR DE PELICULAS ----------- " )
        print(" | 1. Cargar archivo (CSV/Excel)           | " )
        print(" | 2. Buscar en API y añadir               | " )
        print(" | 3. Listar datos actuales                | " )
        print(" | 4. Estadisticas (Pendiente)             | " )
        print(" | 5. Graficos (Pendiente)                 | " )
        print(" | 6. Exportar resultados                  | " )
        print(" | 7. Salir                                | " )
        print(" ------------------------------------------- " )
        
        opcion = input("Elige una opcion: ")
        
        if opcion == "1": cargar_datos()
        elif opcion == "2": buscar_y_annadir()
        elif opcion == "3": ver_datos()
        elif opcion == "4": estadisticas() 
        elif opcion == "5": graficos()
        elif opcion == "6": exportar_csv()
        elif opcion == "7": break
        else: print("Opcion no valida")

if __name__ == "__main__":
    menu()