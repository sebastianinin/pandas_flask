# Usa la imagen oficial de Python
FROM python:3.8

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo requirements.txt al contenedor
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el contenido actual del directorio al contenedor en /app
COPY . /app

# Instala gdown y wget para descargar el archivo
RUN pip install gdown && \
    apt-get update && \
    apt-get install -y wget && \
    rm -rf /var/lib/apt/lists/*

# Descarga y descomprime el archivo
RUN gdown --id 1_sRMeV_jdECnAb51e6fUke79F3x0JzcJ --output ratings.zip && \
    unzip ratings.zip && \
    rm ratings.zip

# Expone el puerto 5000 para que Flask pueda escuchar
EXPOSE 5000

# Define la variable de entorno para Flask
ENV FLASK_APP=app.py

# Ejecuta la aplicación cuando se inicia el contenedor
CMD ["flask", "run", "--host=0.0.0.0"]
