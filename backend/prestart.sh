#! /usr/bin/env bash

# Let the DB start
python /app/app db init

# Run migrations
python /app/app db alembic upgrade head

# Test connection
python /app/app db test-connect

# Create initial data in DB
python /app/app db seed
