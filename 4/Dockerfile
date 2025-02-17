# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV STORAGE_PATH=/tmp/todos.txt

EXPOSE 5000

CMD ["python", "app.py"]