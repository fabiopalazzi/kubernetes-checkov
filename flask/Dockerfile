# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster

ENV PYTHONUNBUFFERED=0

EXPOSE 5000

WORKDIR /python

RUN apt-get update && apt-get install -y default-libmysqlclient-dev
RUN apt-get -y install build-essential

COPY requirements.txt requirements.txt
RUN pip3.9 install -r requirements.txt
RUN pip3.9 install pymysql

COPY . .

CMD [ "python3.9", "-m" , "flask", "run", "--host=0.0.0.0"]