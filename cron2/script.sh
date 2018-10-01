#!/bin/sh

# code goes here.
echo "Running script..."

PG_USER="postgres"
DATABASE="postgres"
CONTAINER=docker_django_db
DATE="_"$(date +"%m-%d-%Y_%H-%M-%S")
NAME=$DATABASE$DATE
FILE=$NAME

PG_BAK_NOW () {
  # pg_dump -U $PG_USER $DATABASE | gzip > default_backup.sql
  # pg_dump -U $PG_USER $DATABASE | gzip > $FILE.sql
  docker exec -t $CONTAINER pg_dump -c -U $PG_USER $DATABASE > /backups/default_backup.sql
  docker exec -t $CONTAINER pg_dump -c -U $PG_USER $DATABASE | gzip > /backups/$FILE.sql.gz
}

PG_BAK_NOW

echo "$(date): pg_dump default_backup && pg_dump $FILE.sql success"