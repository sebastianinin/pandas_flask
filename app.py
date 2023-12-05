from flask import Flask, render_template, request
import pandas as pd
from scipy.spatial.distance import euclidean

app = Flask(__name__)

# Cargar el archivo CSV
archivo_csv = 'ratings.csv'
df = pd.read_csv(archivo_csv)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calcular_distancias', methods=['POST'])
def calcular_distancias():
    try:
        # Obtener el userId del formulario
        usuario_id = int(request.form['userId'])

        # Filtrar el DataFrame para el usuario específico
        usuario_data = df[df['userId'] == usuario_id]

        # Filtrar usuarios con al menos 3 películas en común
        usuarios_comunes = df.groupby('userId').filter(lambda x: len(set(x['movieId']).intersection(set(usuario_data['movieId']))) >= 3)

        # Incluir solo las películas en común
        merged_data = pd.merge(usuario_data, usuarios_comunes, on='movieId', suffixes=('_usuario', '_otro'))

        # Calcular la distancia euclidiana entre el usuario ingresado y los demás usuarios
        distancias = {}
        for user in usuarios_comunes['userId'].unique():
            if user != usuario_id:
                user_data = merged_data[merged_data['userId_otro'] == user]
                distancia = euclidean(user_data['rating_usuario'], user_data['rating_otro'])
                distancias[user] = distancia

        # Encontrar los 3 usuarios más cercanos
        usuarios_cercanos = sorted(distancias.items(), key=lambda x: x[1])[:3]

        # Mostrar los usuarios más cercanos y sus datos
        resultados = []
        for user, distancia in usuarios_cercanos:
            user_data = usuarios_comunes[usuarios_comunes['userId'] == user]
            common_movies = set(user_data['movieId']).intersection(set(usuario_data['movieId']))
            resultados.append({
                'user': user,
                'distancia': distancia,
                'datos_usuario': user_data[user_data['movieId'].isin(common_movies)][['movieId', 'rating']],
                'datos_usuario_ingresado': usuario_data[usuario_data['movieId'].isin(common_movies)][['movieId', 'rating']]
            })

        return render_template('resultados.html', resultados=resultados)

    except Exception as e:
        return render_template('error.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
