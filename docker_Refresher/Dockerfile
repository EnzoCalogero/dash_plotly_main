FROM artifactory.enzo.net:8000/analytics:2018_08_21local

WORKDIR /app

COPY ./index.py /app/index.py
COPY ./apps/*.py /app/apps/
 
ENTRYPOINT [ "python3" ]

CMD [ "index.py" ]


