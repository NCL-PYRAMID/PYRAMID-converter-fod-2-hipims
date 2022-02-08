FROM python:3.8

RUN mkdir /app

WORKDIR /app

COPY ./bbox_to_object.py ./
COPY ./requirements.txt ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV PLATFORM="docker"

CMD python bbox_to_object.py
