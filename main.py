from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
import joblib
import numpy as np
import os

app = FastAPI()

class PrediccionInput(BaseModel):
    glucosa: int
    edad: int

# Cargar modelo
MODEL_PATH = "model.pkl"
try:
    modelo = joblib.load(MODEL_PATH)
except:
    modelo = None

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "mysql"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "rootpass"),
        database=os.getenv("DB_NAME", "diabetes")
    )

@app.get("/")
def read_root():
    return {"mensaje": "API de Predicción de Diabetes funcionando", "modelo_cargado": modelo is not None}

# CRUD
@app.get("/datos")
def listar():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pacientes")
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultado

@app.post("/crear")
def crear(glucosa: int, edad: int, riesgo: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pacientes (glucosa, edad, riesgo) VALUES (%s, %s, %s)",
                   (glucosa, edad, riesgo))
    conn.commit()
    cursor.close()
    conn.close()
    return {"mensaje": "Registro creado exitosamente"}

@app.put("/actualizar/{id}")
def actualizar(id: int, glucosa: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE pacientes SET glucosa=%s WHERE id=%s", (glucosa, id))
    conn.commit()
    cursor.close()
    conn.close()
    return {"mensaje": f"Paciente {id} actualizado"}

@app.delete("/eliminar/{id}")
def eliminar(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pacientes WHERE id=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"mensaje": f"Registro {id} eliminado"}

# Predicción
@app.post("/prediccion")
def prediccion(input: PrediccionInput):
    if modelo is None:
        raise HTTPException(status_code=500, detail="Modelo no encontrado. Ejecuta train.py primero.")
    datos = np.array([[input.glucosa, input.edad]])
    resultado = modelo.predict(datos)
    return {
        "glucosa": input.glucosa,
        "edad": input.edad,
        "prediccion_riesgo": int(resultado[0])
    }