from fastapi import FastAPI
import pandas as pd

df = pd.read_csv('datasets/movies.csv')
app = FastAPI()


##### * Consulta 1: Película con mayor duración con filtros opcionales de AÑO, PLATAFORMA Y TIPO DE DURACIÓN

@app.get('/max_duration')
def get_max_duration(year: int = None, platform: str = None, duration_type: str = None):

    # Filtrar los datos según los parámetros opcionales

    filtered_data = df
    if year is not None:
        filtered_data = filtered_data[filtered_data['release_year'] == year]
    if platform is not None:
        filtered_data = filtered_data[filtered_data['platform'] == platform]
    if duration_type is not None:
        filtered_data = filtered_data[filtered_data['duration_type'] == duration_type]

    # Encontrar la película con la duración máxima
    
    max_duration = filtered_data['duration_int'].max()
    max_duration_movie = filtered_data[filtered_data['duration_int'] == max_duration].iloc[0]

    # Devolver los datos de la película encontrada
    
    return {
        'title': max_duration_movie['title'],
        'duration': max_duration_movie['duration'],
        'platform': max_duration_movie['platform'],
        'year': max_duration_movie['release_year']
    }


##### * Consulta 2: Cantidad de películas por plataforma con un puntaje mayor a XX en determinado año
@app.get('/score_count')
def get_score_count(platform: str, score: int, year: int):
    
    # Filtrar los datos según la plataforma y el año
    
    filtered_data = df[(df['platform'] == platform) & (df['release_year'] == year)]

    # Contar las películas con el puntaje mayor al especificado
    
    count = len(filtered_data[filtered_data['score'] > score])

    # Devolver la cantidad encontrada
    
    return {'count': count}


##### * Consulta 3: Cantidad de películas por plataforma con filtro de PLATAFORMA
@app.get('/count_platform')
def get_count_platform(platform: str):
    
    # Filtrar los datos según la plataforma
    
    filtered_data = df[df['platform'] == platform]

    # Contar las películas
    
    count = len(filtered_data)

    # Devolver la cantidad encontrada
    
    return {'count': count}


##### * Consulta 4: Actor que más se repite según plataforma y año

@app.get('/most_common_actor')
def get_most_common_actor(platform: str, year: int):
    
    # Filtrar los datos según la plataforma y el año
    
    filtered_data = df[(df['platform'] == platform) & (df['release_year'] == year)]

    # Dividir la columna de actores en una lista de actores para cada película
    
    actors = filtered_data['actors'].str.split(', ')

    # Contar la frecuencia de cada actor y seleccionar el que aparece más veces
    
    actor_counts = pd.Series([actor for sublist in actors for actor in sublist]).value_counts()
    most_common_actor = actor_counts.index[0]

    # Devolver el actor más común encontrado
    
    return {'most_common_actor': most_common_actor}