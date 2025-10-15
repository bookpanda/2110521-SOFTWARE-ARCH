- http://localhost:1337/
```bash
curl -i http://localhost:8001/
curl -i -X POST --url http://localhost:8001/services/ --data name=exampleservice1 --data url=http://mockbin.org
curl -i -X POST --url http://localhost:8001/services/exampleservice1/routes --data paths[]=/mock


# docker run --rm –-network=kong-net pantsel/konga -c prepare -a postgres -u postgresql://kong:kong@kong-database:5432/konga

docker-compose down -v
docker-compose up -d kong-database
docker-compose up kong-migrations
docker-compose up -d kong konga
```