** RECOMENDACIONES! **


Descripción

Este proyecto consiste en transformar y limpiar datos, crear una API utilizando el framework FastAPI, realizar un análisis exploratorio de datos, y entrenar un modelo de machine learning para crear un sistema de recomendación de películas para usuarios.

Transformaciones
El objetivo es hacer estas transformaciones a los datos:

Generar un campo ID: Cada ID se compondrá de la primera letra del nombre de la plataforma, seguido del show_id ya presente en los datasets (por ejemplo, para títulos de Amazon, sería "as123").
Reemplazar los valores nulos del campo rating por el string “G” (corresponde al maturity rating: “general for all audiences”).
Dar formato AAAA-mm-dd a las fechas presentes.
Convertir los campos de texto a minúsculas, sin excepciones.
Convertir el campo duration en dos campos: duration_int y duration_type. El primero será un integer y el segundo un string indicando la unidad de medición de duración: min (minutos) o season (temporadas).
Desarrollo de la API
La API se desarrollará utilizando el framework FastAPI, y se propondrán las siguientes consultas:

Película con mayor duración con filtros opcionales de AÑO, PLATAFORMA Y TIPO DE DURACIÓN. (la función debe llamarse get_max_duration(year, platform, duration_type))
Cantidad de películas por plataforma con un puntaje mayor a XX en determinado año (la función debe llamarse get_score_count(platform, scored, year))
Cantidad de películas por plataforma con filtro de PLATAFORMA. (La función debe llamarse get_count_platform(platform))
Actor que más se repite según plataforma y año. (La función debe llamarse get_actor(platform, year))
Deployment
El proyecto se desplegará en Deta, ya que no necesita dockerización. Sin embargo, también se considerarán opciones como Railway y Render, aunque estas necesitan dockerización.

Análisis exploratorio de los datos
Una vez que los datos estén limpios, se realizará un análisis exploratorio de datos para investigar las relaciones que hay entre las variables de los datasets, ver si hay outliers o anomalías, y ver si hay algún patrón interesante que valga la pena explorar en un análisis posterior. Se utilizarán librerías como pandas profiling, sweetviz, autoviz, entre otros para obtener conclusiones.

Sistema de recomendación
Una vez que los datos sean consumibles por la API, se entrenará un modelo de machine learning para crear un sistema de recomendación de películas para usuarios, donde dado un id de usuario y una película, nos dirá si la recomienda o no para dicho usuario. Si es posible, se desplegará el sistema de recomendación con una interfaz gráfica amigable para su uso utilizando Gradio o Deta Space para el despliegue, o bien con alguna solución como Streamlit o algo similar en local (tener el despliegue del sistema de recomendación o una interfaz gráfica es un plus al proyecto).
