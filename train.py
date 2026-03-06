import os
import mysql.connector
import pandas as pd
from sklearn.linear_model import LogisticRegression
import joblib

# Variables de entorno correctas para Docker Compose
DB_HOST = os.getenv("DB_HOST", "mysql")  # coincide con tu servicio MySQL
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "rootpass")
DB_NAME = os.getenv("DB_NAME", "diabetes")
DB_PORT = int(os.getenv("DB_PORT", 3306))

def train_model():
    # Conexión a la base de datos
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT
        )
        print("✅ Conectado a MySQL correctamente")
    except mysql.connector.Error as e:
        print("❌ Error conectando a MySQL:", e)
        return

    # Leer datos
    df = pd.read_sql("SELECT glucosa, edad, riesgo FROM pacientes", conn)
    conn.close()

    # Preparar X e y
    X = df[["glucosa", "edad"]]
    y = df["riesgo"]

    # Entrenar modelo
    modelo = LogisticRegression()
    modelo.fit(X, y)

    # Guardar modelo dentro del contenedor en /app/
    joblib.dump(modelo, "/app/model.pkl")
    print("✅ Modelo entrenado y guardado en /app/model.pkl")

if __name__ == "__main__":
    train_model()