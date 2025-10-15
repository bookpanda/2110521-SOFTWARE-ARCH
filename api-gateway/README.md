```bash
# docker-compose down -v
# docker-compose up -d kong-database
# docker-compose up kong-migrations
# docker-compose up -d kong konga
docker-compose up -d
docker run --rm --network api-gateway_kong-net -e KONG_DATABASE=postgres -e KONG_PG_HOST=kong-database -e KONG_PG_PASSWORD=kong kong:latest kong migrations bootstrap
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
httpservices1,http,192.168.105.1,8081
httpservice1route,/myservice1
http://localhost:8000/myservice1

httpservicegroup,80,http,upstream
httpservicegrouproute,/servicegroup
### Upstream
upstream
targets:
- 192.168.105.1:8081
- 192.168.105.1:8082
http://localhost:8000/servicegroup

restservice,http,192.168.105.1,3000
restroute,/rest
http://localhost:8000/rest
http://localhost:8000/rest/account?username=nraboy

grpcservice,grpc,192.168.105.1,50051
grpcroute,/ (no strippath),grpc
can test on postman on localhost:9080


## Auth
### Consumer
consumer,cred user, cred pass
Bob,Bob,Bob

httpservice1 -> plugin Basic Auth
httpservice1 -> plugin Key Auth, turn off `key in query`
replicate to rest/grpc services
```bash
./http-scipt.sh
./grpc-scipt.sh
```
