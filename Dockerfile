FROM python:3.12-slim

WORKDIR /app

ENV PYTHONPATH=/app

COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 80

CMD ["python", "src/app.py"]
