#! /usr/bin/env bash
# Let the DB start
export PYTHONPATH='/code'
python backend_pre_start.py

# Run migrations
alembic upgrade head

# Create initial data in DB
python initial_data.py
