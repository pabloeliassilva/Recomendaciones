import pandas as pd

# * MOVIES * #

##### * Lectura de los archivos CSV
amazon = pd.read_csv('./MLOpsReviews/amazon_prime_titles.csv')
disney = pd.read_csv('./MLOpsReviews/disney_plus_titles.csv')
hulu = pd.read_csv('./MLOpsReviews/hulu_titles.csv')
netflix = pd.read_csv('./MLOpsReviews/netflix_titles.csv')


##### * Agregar identificador y plataforma: 
    # Se crea una lista llamada "platforms" que contiene los nombres de las plataformas de streaming. 
    # Luego, se usa un bucle "for" con la función "zip" para recorrer dos listas simultáneamente: 
    # una lista que contiene los dataframes de las plataformas
    # y la lista de nombres de las plataformas.
    # Dentro del bucle "for", se asigna a cada dataframe de plataforma una nueva columna llamada "id", 
    # que es una cadena compuesta por la primera letra del nombre de la plataforma 
    # y el valor de la columna "show_id" convertido a una cadena. 
    # Luego, se agrega otra columna llamada "platform", 
    # que es igual al nombre de la plataforma correspondiente en la lista "platforms". 
    # En resumen, esta línea de código agrega dos nuevas columnas a cada dataframe de plataforma: 
    # una columna de identificación y una columna de nombre de plataforma.

platforms = ['amazon', 'disney', 'hulu', 'netflix']

for df, platform in zip([amazon, disney, hulu, netflix], platforms):
    df['id'] = platform[0] + df['show_id'].astype(str)
    df['platform'] = platform


##### * Combinar los dataframes
    # Se crea un nuevo dataframe llamado df concatenando los cuatro dataframes previamente definidos (amazon, disney, hulu, netflix).

df = pd.concat([amazon, disney, hulu, netflix])


##### * Rellenar valores vacíos, convertir a minúsculas y limpiar duración
    # Se rellena los valores perdidos en la columna rating con el valor 'G' (clasificación para todo público) y modifica el dataframe df original.
    # Se aplica una función lambda que convierte a minúsculas todas las cadenas de texto (columnas de tipo object) en el dataframe df. 
    # Las columnas que no son de tipo object (por ejemplo, las columnas numéricas) no se modifican.
    # Se limpia y normaliza los valores en la columna duration del dataframe df. 
    # Primero, elimina todas las letras "s" en la columna duration. 
    # Luego, elimina la cadena "min" en la columna duration. 
    # Finalmente, elimina cualquier carácter no numérico que haya quedado en la columna 
    # y elimina los espacios en blanco al comienzo y al final de cada valor de la columna. 
    # El resultado es una columna duration con valores enteros que representan la duración en minutos de cada programa de televisión o película en el dataset.

df.fillna({'rating': 'G'}, inplace=True)
df = df.apply(lambda x: x.str.lower() if x.dtype == "object" else x)
df['duration'] = df['duration'].str.replace(r's', '').str.replace(r'min', '').str.replace(r'', '').str.strip()


##### * Dividir duración en entero y tipo, reemplazar "seasons" por "season"
    # Primero, se usa str.split() para separar el contenido de la columna "duration" en dos columnas diferentes, "duration_int" y "duration_type". 
    # La opción expand=True especifica que se deben crear dos columnas a partir de los valores separados.
    # Después, se convierte la columna "duration_int" en un tipo numérico usando pd.to_numeric() con la opción errors='coerce', 
    # que establece en NaN (Not a Number) cualquier valor que no se pueda convertir a un número.
    # Finalmente, se usa str.replace() para cambiar la cadena "seasons" en la columna "duration_type" a "season".

df[['duration_int','duration_type']] = df['duration'].str.split(expand=True)
df['duration_int'] = pd.to_numeric(df['duration_int'], errors='coerce')
df["duration_type"] = df["duration_type"].str.replace("seasons", "season")


# * SCORES * #

##### * Leer y combinar archivos de calificaciones
    # lee los archivos CSV de calificaciones para cada una de las 8 partes, 
    # cuyo nombre de archivo es del formato MLOpsReviews/ratings/{i}.csv, 
    # donde {i} es el número de parte que va desde 1 hasta 8. 
    # En lugar de escribir 8 líneas de código separadas, 
    # esta línea usa una comprensión de lista para leer todos los archivos y concatenarlos en un solo DataFrame. 
    # La función pd.concat() concatena los DataFrames leídos verticalmente, es decir, apila los datos uno encima del otro. 
    # Finalmente, el DataFrame resultante se guarda en la variable df_ratings.

df_ratings = pd.concat([pd.read_csv(f'MLOpsReviews/ratings/{i}.csv') for i in range(1, 9)])


##### * Cambiar el nombre de la columna "rating" a "score"
    # renombra la columna "rating" a "score" en el DataFrame df_ratings.
    # El parámetro columns especifica un diccionario que mapea los nombres antiguos de las columnas a los nuevos nombres. 
    # En este caso, "rating" se mapea a "score". 
    # El parámetro inplace se establece en True para que el DataFrame original se modifique en su lugar.
    
df_ratings.rename(columns={'rating': 'score'}, inplace=True)


##### * Convertir la marca de tiempo a formato de fecha
    # convierte la columna timestamp de un formato de tiempo UNIX en formato de fecha estándar. 
    # El tiempo UNIX es una representación numérica del tiempo, que cuenta los segundos transcurridos desde el 1 de enero de 1970. 
    # El parámetro unit='s' se utiliza para indicar que los valores en la columna timestamp se encuentran en segundos. 
    # La función pd.to_datetime() convierte los valores de la columna en objetos de fecha/hora, 
    # y dt.strftime('%Y-%m-%d') formatea la fecha en el formato 'año-mes-día'. 
    # El resultado es que la columna timestamp ahora contiene fechas en lugar de valores de tiempo UNIX.
    
df_ratings['timestamp'] = pd.to_datetime(df_ratings['timestamp'], unit='s').dt.strftime('%Y-%m-%d')


# * MEAN * #

##### * Calcular los promedios de calificaciones por película
    # Se calcula el promedio de los puntajes de todas las películas en el DataFrame df_ratings, 
    # agrupando los puntajes por el identificador de la película movieId. 
    # Es decir, se está generando un objeto DataFrameGroupBy agrupando los puntajes de cada película, 
    # y luego se está calculando la media del puntaje para cada grupo, utilizando el método .mean().
    # El resultado es un objeto Series que contiene el promedio de puntajes para cada movieId.
    
prom_scores = df_ratings.groupby("movieId")["score"].mean()


##### * Combinar los dataframes de películas y calificaciones
    # Se convierten los valores de la columna "id" en tipo str. 
    # Esto se hace para asegurar que los valores en la columna "id" son del mismo tipo que los valores en la columna "movieId" de prom_scores, 
    # la cual se utilizará más adelante en la fusión de datos.
    # Se fusiona df con prom_scores utilizando la columna "id" de df y la columna "movieId" de prom_scores como llaves de la fusión. 
    # La fusión agrega una nueva columna llamada "score" a df, que contiene los promedios de puntaje calculados en prom_scores para cada película.

df['id'] = df['id'].astype(str)
df = pd.merge(df, prom_scores, left_on="id", right_on="movieId")


# * EXPORT * #

##### * Escribir los resultados en dos archivos CSV

df.to_csv("datasets/movies.csv", index=False)
df_ratings.to_csv("datasets/scores.csv", index=False)