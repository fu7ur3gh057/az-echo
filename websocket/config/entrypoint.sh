#!/bin/sh

until cd /app/websocket
do
    echo "Waiting for websocket volume..."
done

set -o errexit
set -o nounset

uvicorn app:app --host "0.0.0.0" --port 8088 --reload --ws 'auto' \
  --loop 'auto' --workers 4

#uvicorn app:app --host 0.0.0.0 --port 8088

exec "$@"
