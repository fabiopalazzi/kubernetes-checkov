# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster

EXPOSE 5000

WORKDIR /python

COPY requirements.txt requirements.txt
RUN pip3.9 install -r requirements.txt

COPY . .

CMD [ "python3.9", "-m" , "flask", "run", "--host=0.0.0.0"]