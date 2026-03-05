# -*- coding: utf-8 -*-
import mysql.connector
import pandas as pd
from sklearn.linear_model import LogisticRegression
import joblib
import os

DB_HOST = os.getenv("DB_HOST", "mysql")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "rootpass")
DB_NAME = os.getenv("DB_NAME", "diabetes")

def train_model():
    # Conexión a la base de datos
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
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

    # Guardar modelo
    joblib.dump(modelo, "model.pkl")
    print("Modelo entrenado y guardado en model.pkl")

if __name__ == "__main__":
    train_model()