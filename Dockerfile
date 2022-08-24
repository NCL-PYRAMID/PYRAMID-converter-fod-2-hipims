FROM python:3.8-slim

RUN mkdir -p /data/inputs
RUN mkdir -p /data/outputs

WORKDIR /app

COPY ./bbox_to_object.py ./
COPY ./requirements.txt ./
COPY ./sample_car_data.txt ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV PLATFORM="docker"

ENTRYPOINT ["python","-u","bbox_to_object.py"]
