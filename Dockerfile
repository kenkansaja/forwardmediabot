FROM python:3.9.6-slim-buster

RUN apt update && apt upgrade -y
RUN mkdir /app/
WORKDIR /app
ADD . /app
RUN pip3 install -U -r requirements.txt

CMD python3 -m forwardscoverbot
