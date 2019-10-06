FROM python:3.5

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libatlas-base-dev gfortran

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY . /app

WORKDIR /app

copy ./data /app/data

CMD ["python", "creating_db.py"]

