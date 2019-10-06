FROM logstash

RUN mkdir /enzo
RUN mkdir /import

COPY ./server_docker2.conf /enzo/logstash2.conf

RUN chmod -R 777 /import

CMD ["-f", "enzo/logstash2.conf"]
