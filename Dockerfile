FROM python:3.10-slim-bullseye

WORKDIR /usr/app/src

COPY . .

RUN pip install -r requirements.txt

RUN apt update && apt install tzdata -y

ENV TZ="Europe/Madrid"


