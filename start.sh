#!/bin/bash

# Start Gunicorn processes
echo Starting Gunicorn.
cd world2jam
exec gunicorn world2jam.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4