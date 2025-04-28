#!/bin/bash

# Check if the .env file exists.
if [ ! -f .env ]; then
   echo "CRITICAL: Environment file .env not found. Creating a template."
   touch .env
   echo "OPENAI_API_KEY=" >> .env
   echo "OPENAI_ORGANIZATION_ID=" >> .env 
   echo "VECTOR_DB=redis" >> .env
   exit 1
fi

# Check if any Docker containers are running. If they are, stop them.
if [ `docker compose ps | egrep "^IMAGE" | wc -l | tr -d ' '` -gt 0 ]; then
  echo "WARNING: Found containers running. Stopping them."
  docker compose down
fi

# Check for the Vector DB environment variable.
VDB=`grep VECTOR_DB .env | cut -f2 -d'='`
if [ "${VDB}" = "redis" ]; then
  echo "INFO: Will set up docker images for Redis."

  if [ ! -f docker-compose-redis.yml ]; then
    echo "CRITICAL: Unable to find docker compose file for Redis docker-compose-redis.yml"
    exit 1
  fi
  rm docker-compose.yml
  ln -s docker-compose-redis.yml docker-compose.yml
elif [ "${VDB}" = "weaviate" ]; then
  echo "INFO: Will set up docker images for Weaviate."

  if [ ! -f docker-compose-weaviate.yml ]; then
    echo "CRITICAL: Unable to find docker compose file for Weviate docker-compose-weaviate.yml"
    exit 1
  fi
  rm docker-compose.yml
  ln -s docker-compose-weaviate.yml docker-compose.yml
fi


# Build the Docker images.
echo "INFO: Building docker images and starting services."
docker compose down
docker compose build
docker compose down
docker volume rm openai_docquery_data
docker compose up -d
docker compose logs -f
