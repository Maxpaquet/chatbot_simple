FROM python:3.12-slim
WORKDIR /app

# Copier uniquement ce qu'il faut
COPY requirements.lock ./
RUN pip install --no-cache-dir -r requirements.lock


COPY ./app ./app


EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]