#!/bin/bash

# Permet au code de s'arrêter et renvoyer une erreur en cas de problème. 
set -e

cd ./api
docker compose -f compose.yml -f compose.test.yml up --build -d

cd ../tests
docker compose up  --build -d