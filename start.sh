#!/bin/bash

# Ensure the script exits on any error
set -e

# Ensure the logging folder exists
mkdir -p $ITS_JOBS_LOGGING_FOLDER

# Start the Celery worker for the "maintenance" queue
echo "Starting Celery worker for the 'maintenance' queue..."
celery -A app worker --loglevel=info -n maintenance -Q maintenance \
    > "$ITS_JOBS_LOGGING_FOLDER/WORKER_MAINTENANCE.log" 2>&1 &

WORKER_MAINTENANCE_PID=$!


echo "Starting Celery worker for the 'notifications' queue..."
celery -A app worker --loglevel=info -n notifications -Q notifications \
    > "$ITS_JOBS_LOGGING_FOLDER/WORKER_NOTIFICATIONS.log" 2>&1 &

WORKER_NOTIFICATIONS_PID=$!


# Wait for the worker to initialize (adjust time if necessary)
# Start the Celery Beat scheduler
echo "Starting Celery Beat scheduler..."
celery -A app beat --loglevel=info \
    > "$ITS_JOBS_LOGGING_FOLDER/BEAT_PROCESS.log" 2>&1 &

BEAT_PID=$!

sleep 5


# Check the Celery task registry
echo "Checking the Celery task registry..."
celery -A app inspect registered || {
    echo "Error: Unable to inspect registered tasks. Check worker logs."
    exit 1
}

# Keep the script alive to allow the worker and beat processes to continue running
echo "Celery worker and beat scheduler are running."
echo "Worker maintenance PID: $WORKER_MAINTENANCE_PID"
echo "Worker notifications PID: $WORKER_NOTIFICATIONS_PID"

echo "Beat PID: $BEAT_PID"

wait $WORKER_PID $BEAT_PID
