FROM python:3.8-slim

RUN mkdir /app

WORKDIR /app

COPY ./bbox_to_object.py ./
COPY ./requirements.txt ./

COPY ./dl-outputs-sample.zip ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV PLATFORM="docker"

CMD ["python" "-u" "bbox_to_object.py"]
