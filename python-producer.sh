#!/bin/bash

docker build -t write_to_kafka_image -f Dockerfile1 .

docker run -it --name python-producer --network dulher-kafka-cassandra-network --rm write_to_kafka_image
