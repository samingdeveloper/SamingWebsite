Backup your databases
docker exec -t your-db-container pg_dumpall -c -U postgres > dump_`date +%d-%m-%Y"_"%H_%M_%S`.sql
docker exec -t $CONTAINER pg_dump -c -U $PG_USER $DATABASE > /var/backup/default_backup.sql
docker exec -t $CONTAINER pg_dump -c -U $PG_USER $DATABASE | gzip > /var/backup/$FILE.sql.gz

Restore your databases
cat your_dump.sql | docker exec -i your-db-container psql -U postgres

To save some space on disk you might want to pipe the dump to 
gzip: docker exec -t your-db-container pg_dumpall -c -U postgres | gzip > /var/data/postgres/backups/dump_date +%d-%m-%Y"_"%H_%M_%S.gz


How can I restore .xz or .gz packed this way?
Just unzip the data before you restore it. To do it as a one liner 
you will have to replace the cat your_dump.sql with the unzip command 
and pipe that instead of the cat result to docker exec. 