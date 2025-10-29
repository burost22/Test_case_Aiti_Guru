FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1
ENV DB_HOST=db
ENV DB_NAME=orders_db
ENV DB_USER=postgres
ENV DB_PASS=postgres

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]