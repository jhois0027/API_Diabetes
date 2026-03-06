FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir fastapi uvicorn mysql-connector-python pandas scikit-learn joblib pytest httpx

EXPOSE 8000

CMD uvicorn main:app --host 0.0.0.0 --port $PORT