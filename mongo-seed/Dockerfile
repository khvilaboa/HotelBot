FROM continuumio/anaconda:latest

COPY init_db.py /init_db.py
RUN pip install pymongo
CMD python init_db.py