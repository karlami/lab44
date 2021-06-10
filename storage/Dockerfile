FROM python:3.8-slim-buster
WORKDIR /storage_api

USER root

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python3","storage_receiver.py"]

