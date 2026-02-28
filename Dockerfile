FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
ENV PYTHONUNBUFFERED=1
ENV DB_PATH=/app/data/history.db

ENTRYPOINT ["python", "entrypoint.py"]
CMD ["serve"]