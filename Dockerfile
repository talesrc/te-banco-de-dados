FROM python:3.9-alpine

WORKDIR /app

COPY main.py main.py

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

CMD ["python3", "main.py"]