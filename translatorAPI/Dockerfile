FROM python:3.8-slim-buster

WORKDIR /translatorAPI

USER root

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python3","translatorAPI.py"]

