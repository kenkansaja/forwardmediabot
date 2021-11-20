FROM alpine:3.13
RUN mkdir /app/
WORKDIR /app/
COPY . /app/

CMD pyton3 -m forwardscoverbot
