FROM python:3.12-slim

WORKDIR /app

COPY . .

EXPOSE 9123

USER 1000

CMD ["python3", "app.py"]
