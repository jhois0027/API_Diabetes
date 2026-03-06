# -*- coding: utf-8 -*-
import mysql.connector
import pandas as pd
from sklearn.linear_model import LogisticRegression
import joblib
import os

# Variables de entorno para Railway
DB_HOST = os.getenv("MYSQLHOST", "mysql.railway.internal")
DB_USER = os.getenv("MYSQLUSER", "root")
DB_PASSWORD = os.getenv("MYSQLPASSWORD", "rootpass")
DB_NAME = os.getenv("MYSQLDATABASE", "railway")
DB_PORT = int(os.getenv("MYSQLPORT", 3306))

def train_model():
    # Conexión a la base de datos
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT
    )

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