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

## Init services
```bash
node ./SimpleHTTP/main1.js
node ./SimpleHTTP/main2.js
node ./SimpleREST/app.js

cd ./SimplegRPC/node
node ./greeter_server.js

# cd ./SimplegRPC/node
# node ./greeter_client.js

```

## Set services/routes
```bash
./http-scipt.sh
./grpc-scipt.sh
```
