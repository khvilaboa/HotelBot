FROM continuumio/anaconda:latest
MAINTAINER Iván Martínez

ARG DB_ADDRESS
ARG DB_PORT

RUN mkdir -p /usr/local/hotelbot
ENV HOTELBOT_HOME /usr/local/hotelbot
ADD agents.py /usr/local/hotelbot
ADD facts.py /usr/local/hotelbot
ADD handlers.py /usr/local/hotelbot
ADD hotelbot.py /usr/local/hotelbot
ADD resources.py /usr/local/hotelbot
ADD requirements.txt /usr/local/hotelbot

COPY policies /usr/local/hotelbot/policies
COPY utils /usr/local/hotelbot/utils

WORKDIR $HOTELBOT_HOME
RUN pip install -r requirements.txt

CMD ["python","hotelbot.py"]