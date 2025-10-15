#e) Check if Kong is up and running with

curl -i http://localhost:8001/

#f) Add service

curl -i -X POST --url http://localhost:8001/services/ --data name=exampleservice1 --data url=http://mockbin.org

#Add route

At cmd prompt:
curl -i -X POST --url http://localhost:8001/services/exampleservice1/routes --data paths=/mock

#f) Add restaurant-client service
curl -i -X POST --url http://localhost:8001/services/ --data name=restaurant-client --data url=http://restaurants-client:3000

#Add route for restaurant-client
curl -i -X POST --url http://localhost:8001/services/restaurant-client/routes --data 'paths=/client'

#g) Add mongo-express service
curl -i -X POST --url http://localhost:8001/services/ --data name=mongo-express --data url=http://mongo-express:8081

#Add route for mongo-express
curl -i -X POST --url http://localhost:8001/services/mongo-express/routes --data 'paths=/mongo'
