FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python3 python3-pip

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt

COPY . /app
COPY ./apps /app/apps
COPY ./pics /app/pics
COPY ./data /app/data
COPY ./templates /app/templates
COPY ./current_docker.ini /app/data/current.ini
 
ENTRYPOINT [ "python3" ]

CMD [ "index.py" ]


