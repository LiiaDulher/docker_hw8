#!/bin/bash

docker stop kafka-server
docker stop zookeeper-server
docker rm kafka-server
docker rm zookeeper-server
