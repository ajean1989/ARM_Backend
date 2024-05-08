cd ./api

docker compose -f compose.yml -f compose.dev.yml up --build --force-recreate -d

cd ..