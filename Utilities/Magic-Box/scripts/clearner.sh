rm -rf /home/enzo/tech_view/*
rm -rf /home/enzo/Builder/database.sql
docker-compose -f /home/enzo/composers/dbs/docker-compose.yml down
docker-compose -f /home/enzo/composers/elasticsearch/docker-compose.yml down

docker volume rm  elasticsearch_esdata

exit 0
