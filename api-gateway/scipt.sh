# mockbin
curl -i -X POST --url http://localhost:8001/services/ --data name=exampleservice1 --data url=http://mockbin.org
#Add route
curl -i -X POST --url http://localhost:8001/services/exampleservice1/routes --data paths=/mock

# restaurant-client
curl -i -X POST --url http://localhost:8001/services/ --data name=restaurant-client --data url=http://restaurants-client:3000
curl -i -X POST --url http://localhost:8001/services/restaurant-client/routes --data 'paths=/client' --data 'strip_path=true'

# restaurant-server
curl -i -X POST --url http://localhost:8001/services/ --data name=restaurant-server --data url=http://restaurants-server:30043
curl -i -X POST --url http://localhost:8001/services/restaurant-server/routes --data 'paths=/server' --data 'strip_path=true'

# mongo-express
curl -i -X POST --url http://localhost:8001/services/ --data name=mongo-express --data url=http://mongo-express:8081
curl -i -X POST --url http://localhost:8001/services/mongo-express/routes --data 'paths=/mongo' --data 'strip_path=true'
