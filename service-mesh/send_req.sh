#!/bin/bash

GATEWAY_URL="http://localhost:8080"

for i in $(seq 1 100); do
    curl -s -o /dev/null "http://$GATEWAY_URL/productpage"; 
done

echo "Requests sent successfully"