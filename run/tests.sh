#!/bin/bash

# Permet au code de s'arrêter et renvoyer une erreur en cas de problème. 
set -e

cd ./api
docker compose up  -f compose.yml -f compose.dev.yml --build -d

cd ../tests
docker compose up  --build -d