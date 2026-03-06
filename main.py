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

# Función para conectarse a la base de datos
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQLHOST"),
        user=os.getenv("MYSQLUSER"),
        password=os.getenv("MYSQLPASSWORD"),
        database=os.getenv("MYSQLDATABASE"),
        port=int(os.getenv("MYSQLPORT", 3306))
    )

# Rutas
@app.get("/")
def read_root():
    return {"mensaje": "API de Predicción de Diabetes funcionando", "modelo_cargado": modelo is not None}

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
    port = int(os.getenv("PORT", 8080))  # Puerto dinámico que Railway asigna
    uvicorn.run(app, host="0.0.0.0", port=port)