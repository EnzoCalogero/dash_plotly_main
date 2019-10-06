FROM logstash

RUN mkdir /enzo
RUN mkdir /import

COPY ./server_docker.conf /enzo/logstash.conf


RUN chmod -R 777 /import

CMD ["-f", "enzo/*.conf"]
