FROM rocker/shiny

RUN apt-get update && apt-get install -y  libpq-dev

RUN R -e "install.packages(c('visNetwork','igraph','RPostgreSQL','ConfigParser'), repos='https://cran.rstudio.com/')"

COPY . /srv/shiny-server/
 
EXPOSE 3838

CMD ["/usr/bin/shiny-server.sh"]

