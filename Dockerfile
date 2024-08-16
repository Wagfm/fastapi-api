FROM python:3.12.3-alpine
LABEL authors="wagner"

ENV PYTHONPATH=/app/src

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY src ./src

EXPOSE 8000/tcp

CMD ["fastapi", "run", "src/app.py", "--host", "127.0.0.1", "--port", "8000", "--reload"]
