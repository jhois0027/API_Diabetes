# Dockerfile para Railway
FROM python:3.11

# Directorio de trabajo en el contenedor
WORKDIR /app

# Copiar dependencias e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el proyecto al contenedor
COPY . .

# Exponer puerto (opcional, Railway lo maneja)
EXPOSE 8000

# Comando para iniciar la API usando la variable $PORT de Railway
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT"]