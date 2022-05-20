#!/bin/bash

docker build -t read_kafka_write_cassandra_image -f Dockerfile2 .

docker run -it --name python-consumer --network dulher-kafka-cassandra-network --rm read_kafka_write_cassandra_image
