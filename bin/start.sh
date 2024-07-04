#!/bin/sh

# Spin up the mysql service
docker-compose up -d 

# Sleep for 6 minutes.
echo "Script paused for 6 seconds"
sleep 6

# Setup Python Environment and Install Dependencies.
echo "Setting up Python dependencies."
python -m venv env
source env/bin/activate
pip install -r requirement.txt

# Run Migrations.
echo "Running Migrations"
python src/infrastructure/migrate.py 

# start the API
echo "Starting API via FastApi."
fastapi dev src/app/main.py