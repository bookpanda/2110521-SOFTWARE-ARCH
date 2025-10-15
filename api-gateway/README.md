```bash
# docker-compose down -v
# docker-compose up -d kong-database
# docker-compose up kong-migrations
# docker-compose up -d kong konga
docker-compose up -d
```
- Gateway: http://localhost:8000/
- Kong Admin API: http://localhost:8001/
- Konga UI: http://localhost:1337/

## Set connection
- name: Connect1
- url: http://kong:8001

## Set services/routes
```bash
./scipt.sh
```
- Restaurant client: http://localhost:8000/client
- Restaurant server: http://localhost:8000/server
- Mongo Express: http://localhost:8000/mongo
    - admin: admin