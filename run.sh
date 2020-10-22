#!/bin/bash
# start postgres in the background
/usr/lib/postgresql/11/bin/postgres -D /var/lib/postgresql/11/main -c config_file=/etc/postgresql/11/main/postgresql.conf &

# Wait for the db to start up.
# We should add logic here to validate the database server and continue running
# this script once it's confirmed that it's started.
sleep 15
python ingest.py --verbosity=INFO create-tables
python ingest.py --verbosity=INFO scrape-and-insert-all

# Quick and dirty validation that the data was entered correctly.
# Ideally, I would add a CLI command to output these tables as pandas tables,
# but installing Pandas can take a few minutes and I didn't consider it
# worthwhile for a quick script like this.
psql -U postgres -d drugbank-postgres -c "SELECT * FROM drugs;"
psql -U postgres -d drugbank-postgres -c "SELECT * FROM identifiers;"
psql -U postgres -d drugbank-postgres -c "SELECT * FROM targets;"
