#!/bin/bash

echo "Setting up Kong as Simple gRPC Gateway..."

echo "Creating gRPC service..."
curl -i -X POST --url http://localhost:8001/services/ \
    --data name=restaurant-grpc-service \
    --data url=grpc://restaurants-server:30043

echo "Creating gRPC route..."
curl -i -X POST --url http://localhost:8001/services/restaurant-grpc-service/routes \
    --data name=grpc-catchall-route \
    --data protocols=grpc \
    --data paths=/RestaurantService/

echo "Simple gRPC Gateway setup complete!"
echo "gRPC endpoint: localhost:8000"
echo "Note: Use gRPC client tools to test, not HTTP requests"
