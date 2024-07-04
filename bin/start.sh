#!/bin/sh

# Spin up the mysql service
docker-compose up -d 

# Sleep for 4 minutes before running migrations.
python src/infrastructure/migrate.py 

# start the API
fastapi dev src/app/main.py