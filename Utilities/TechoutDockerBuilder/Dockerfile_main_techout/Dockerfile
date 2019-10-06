FROM artifactory.enzo.net:8000/tech_view:mio


COPY database.sql /sql/

user postgres

RUN ( /usr/lib/postgresql/10/bin/pg_ctl -D "${PGDATA}" -w start) \

  && psql -c 'CREATE ROLE "enzo-tasktracker"' \
  && psql -c 'CREATE ROLE "enzo-syslog"' \
  && psql -c 'CREATE ROLE "enzo-proxy"' \
  && psql -c 'CREATE ROLE "enzo-notifications"' \
  && psql -c 'CREATE ROLE "enzo-mail"' \
  && psql -c 'CREATE ROLE "enzo-logstash"' \
  && psql -c 'CREATE ROLE "enzo-console"' \
  && psql -c 'CREATE ROLE "enzo-behaviour"' \

  && pg_restore -c --if-exists -d enzo /sql/database.sql \

  && (/usr/lib/postgresql/10/bin/pg_ctl -D "${PGDATA}" -m fast -w stop)



