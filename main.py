from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
import joblib
import numpy as np
import os
import uvicorn

app = FastAPI()

# Modelo ML
MODEL_PATH = "model.pkl"
try:
    modelo = joblib.load(MODEL_PATH)
except FileNotFoundError:
    modelo = None
    print("⚠️ Modelo no encontrado, asegúrate de subir model.pkl al repositorio.")

# Entrada para predicción
class PrediccionInput(BaseModel):
    glucosa: int
    edad: int

# Conexión a la base de datos
def get_db_connection():
    try:
        return mysql.connector.connect(
            host=os.getenv("MYSQLHOST"),
            user=os.getenv("MYSQLUSER"),
            password=os.getenv("MYSQLPASSWORD"),
            database=os.getenv("MYSQLDATABASE"),
            port=int(os.getenv("MYSQLPORT", 3306))
        )
    except mysql.connector.Error as e:
        print("Error conectando a MySQL:", e)
        return None

# Rutas
@app.get("/")
def read_root():
    return {"mensaje": "API de Predicción de Diabetes funcionando", "modelo_cargado": modelo is not None}

@app.get("/datos")
def listar():
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pacientes")
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultado

@app.post("/crear")
def crear(glucosa: int, edad: int, riesgo: int):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pacientes (glucosa, edad, riesgo) VALUES (%s, %s, %s)",
                   (glucosa, edad, riesgo))
    conn.commit()
    cursor.close()
    conn.close()
    return {"mensaje": "Registro creado exitosamente"}

@app.post("/prediccion")
def prediccion(input: PrediccionInput):
    if modelo is None:
        raise HTTPException(status_code=500, detail="Modelo no encontrado. Sube model.pkl primero.")
    datos = np.array([[input.glucosa, input.edad]])
    resultado = modelo.predict(datos)
    return {
        "glucosa": input.glucosa,
        "edad": input.edad,
        "prediccion_riesgo": int(resultado[0])
    }

# Main
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))  # Railway asigna este puerto
    uvicorn.run("main:app", host="0.0.0.0", port=port)