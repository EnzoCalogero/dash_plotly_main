FROM python:3.5

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libatlas-base-dev gfortran
COPY requirement /

RUN pip install -r /requirement

COPY . /app
COPY ./data /app/data
WORKDIR /app

CMD ["python", "main.py"]

