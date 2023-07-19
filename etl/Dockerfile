FROM python:3.10-buster

WORKDIR /app

COPY . .

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

CMD ["python3", "main.py"]
