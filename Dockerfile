FROM continuumio/anaconda:latest
MAINTAINER Iván Martínez

RUN mkdir -p /usr/local/hotelbot
ENV HOTELBOT_HOME /usr/local/hotelbot
ADD agents.py /usr/local/hotelbot
ADD facts.py /usr/local/hotelbot
ADD hotelbot.py /usr/local/hotelbot
ADD resources.py /usr/local/hotelbot
ADD requirements.txt /usr/local/hotelbot

COPY policies /usr/local/hotelbot/policies
COPY utils /usr/local/hotelbot/utils

WORKDIR $HOTELBOT_HOME
RUN pip install -r requirements.txt
RUN python -m nltk.downloader punkt
RUN python -m nltk.downloader stopwords
RUN python -m nltk.downloader averaged_perceptron_tagger
RUN sed -i "s/MongoClient()/MongoClient('hotelbot_mongodb')/g" resources.py
CMD ["python","hotelbot.py"]