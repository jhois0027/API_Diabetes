import requests
import random

# Si es en local usa http://localhost:8080
# Si es en Railway usa la URL que te den https://tu-app.up.railway.app
BASE_URL = "https://apidiabetes-production.up.railway.app" 

def poblar_datos(n=50):
    print(f"Iniciando carga de {n} pacientes...")
    
    for i in range(n):
        # Generar datos aleatorios pero realistas
        glucosa = random.randint(70, 250)
        edad = random.randint(18, 90)
        
        # Lógica simple para el campo 'riesgo'
        riesgo = 1 if glucosa > 140 else 0
        
        # Enviar a la API usando el endpoint que creamos en main.py
        # Nota: Usamos params porque en tu main.py los definiste como argumentos de función
        url = f"{BASE_URL}/crear?glucosa={glucosa}&edad={edad}&riesgo={riesgo}"
        
        try:
            response = requests.post(url)
            if response.status_code == 200:
                print(f"[{i+1}] Paciente insertado: G:{glucosa} E:{edad} R:{riesgo}")
            else:
                print(f"Error en el registro {i+1}: {response.text}")
        except Exception as e:
            print(f"Error de conexión: {e}")
            break

    print("\n✅ Carga masiva completada.")

if __name__ == "__main__":
    poblar_datos(50)