#!/bin/bash

docker run --name cassandra-node --network dulher-kafka-cassandra-network -p 9042:9042 -d cassandra:latest
sleep 70s
echo "Creating keyspace and tables"
docker build -t ddl_image -f Dockerfile3 .
docker run -it --network dulher-kafka-cassandra-network --rm ddl_image
