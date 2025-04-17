FROM python:3.11-slim-buster

WORKDIR /app
ENV PYTHONPATH=/app/app:/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip show uvicorn

COPY ../app /app/app
COPY ./alembic.ini /app/alembic.ini
COPY ./alembic /app/alembic

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "debug"]