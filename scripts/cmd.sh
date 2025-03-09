
clear && echo -e "\n\n=================== Docker Images ===================" && docker images && echo -e "\n\n=================== Docker Volumes ===================" && docker volume ls && echo -e "\n\n=================== Docker Networks ==================" && docker network ls && echo -e "\n\n=================== Docker Stacks ===================" && docker stack ls && echo -e "\n\n=================== Docker Services ==================" && docker service ls && echo -e "\n"

docker run -d \
    --name plsql_authman \
    -e POSTGRES_PASSWORD=root \
    -e POSTGRES_USER=root \
    -e POSTGRES_DB=authman \
    -p 5431:5432 \
    -v plsql_authman:/var/lib/postgresql/data \
    postgres:17.2-alpine3.20
