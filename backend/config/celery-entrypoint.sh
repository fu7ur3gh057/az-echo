#!/bin/sh

# CELERY WORKER & BEAT

until cd /app/server; do
  echo "Waiting for server volume..."
done

# Adding needed Az data files to libraries for extracting text, make sure that you use correct Python path
# add file to langdetect
cp stopwords/az /usr/local/lib/python3.10/site-packages/langdetect/profiles
# add file to newspaper3k
cp stopwords/stopwords-az.txt /usr/local/lib/python3.10/site-packages/newspaper/resources/text
# add file to goose3
cp stopwords/stopwords-az.txt /usr/local/lib/python3.10/site-packages/goose3/resources/text

# run a worker and beat
celery -A server worker --beat --scheduler django --loglevel=info
