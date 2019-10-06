FROM artifactory.enzo.net:8000/tech_view:mio

COPY database.sql /sql/

user postgres

RUN ( /usr/lib/postgresql/10/bin/pg_ctl -D "${PGDATA}" -w start) \

  && pg_restore -c --no-acl --no-owner --role=postgres --if-exists -d enzo /sql/database.sql \

  && (/usr/lib/postgresql/10/bin/pg_ctl -D "${PGDATA}" -m fast -w stop)



