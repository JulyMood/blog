FROM python:3.10
MAINTAINER ke

RUN set -ex && apt update && apt install curl -y
RUN set -ex && apt-get update && apt-get install  redis-server vim -y

COPY ./requirements.txt /data/requirements.txt
RUN set -ex && pip --no-cache-dir install -r /data/requirements.txt
COPY . /data
WORKDIR /data

EXPOSE 8880
ENV PYTHONPATH /data

CMD service redis-server start && streamlit run view/home.py --server.port 8880
