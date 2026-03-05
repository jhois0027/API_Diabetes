🩺 **Proyecto Final - API de Predicción de Riesgo de Diabetes**

API RESTful desarrollada con FastAPI para gestionar información de pacientes y predecir el riesgo de diabetes mediante un modelo de Machine Learning entrenado. La aplicación utiliza MySQL como base de datos y se ejecuta con Docker Compose para asegurar portabilidad y facilidad de despliegue.

🔹 **Tecnologías utilizadas**

**Lenguaje:** Python 3.10+

**Framework API:** FastAPI

**Base de datos:** MySQL 8.0

**Machine Learning:** scikit-learn

**Contenedores:** Docker & Docker Compose

**Pruebas automatizadas:** pytest

**Despliegue:** Railway / Docker

📂 **Estructura del proyecto**
Proyect/
├── .vagrant/                  # Configuración de Vagrant
├── modelo.pkl                 # Modelo entrenado
├── test/
│   └── test_main.py           # Pruebas automatizadas de la API
├── docker-compose.yml         # Configuración de servicios Docker
├── Dockerfile                 # Imagen de la aplicación
├── init.sql                   # Script de inicialización de MySQL
├── main.py                    # API principal
├── readme.md                  # Documentación del proyecto
├── requirements.txt           # Dependencias de Python
├── seed_data/                 # Datos iniciales para la base de datos
├── images_prueba/             # Imágenes de ejemplo para pruebas y documentación
├── train.py                   # Entrenamiento del modelo ML
└── Vagrantfile                # Configuración de máquina virtual (opcional)


📦 **Requisitos / Dependencias**
fastapi
uvicorn
mysql-connector-python
pandas
scikit-learn
joblib
pytest
requests
pymysql

💡 Si ejecutas la aplicación dentro del contenedor Docker, estas dependencias se instalarán automáticamente desde requirements.txt.


⚙ Instalación y ejecución local
# Clonar el repositorio
git clone https://github.com/jhois0027/API_Diabetes.git
cd API_Diabetes

# Levantar servicios con Docker Compose
docker-compose up --build -d

Verificar la API en:
http://localhost:8000/docs

La documentación interactiva de FastAPI permite probar todos los endpoints fácilmente.

🛠 **Endpoints**
Endpoint de prueba

GET /test

CRUD de pacientes

Crear paciente: POST /patients (glucosa, edad, riesgo)

Listar pacientes: GET /patients

Actualizar paciente: PUT /patients/{id}

Eliminar paciente: DELETE /patients/{id}

Predicción de riesgo de diabetes

POST /predict

Ejemplo de JSON de entrada:

{
  "glucosa": 120,
  "edad": 45
}

Devuelve la predicción de riesgo.


🧠 **Entrenamiento del modelo**
docker exec -it fastapi_app python /app/train.py
🧪 Pruebas automatizadas

Ubicadas en test/test_main.py:

Validan endpoint de prueba GET /test

CRUD de pacientes

Endpoint de predicción POST /predict


**Ejecutar pruebas dentro del contenedor:**

docker exec -it fastapi_app pytest test/


🐳 **#Docker y Docker Compose**

MySQL 8.0 con persistencia mediante volúmenes y init.sql

API FastAPI con dependencias instaladas automáticamente

Carpeta pkl/ montada para almacenar el modelo .pkl


🚀 **Publicación en Docker Hub**
docker login
docker tag proyect-api ingrij27/proyect-api:1.0
docker push ingrij27/proyect-api:1.0# API_Diabetes
