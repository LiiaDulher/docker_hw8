# Docker hw8
Kafka-Cassandra

## Team: [Liia_Dulher](https://github.com/LiiaDulher)

### Prerequiments
Please put file <b>PS_20174392719_1491204439457_log.csv</b> in this directory.<br>
It takes about 65 seconds for Cassandra node to start, so <i>run-cassandra.sh</i> will start node about <b>1 minute</b>.

### Usage
````
$ sudo chmod +x run-kafka-cluster.sh
$ sudo chmod +x run-cassandra-cluster.sh
$ sudo chmod +x shutdown-cassandra-cluster.sh
$ sudo chmod +x shutdown-cluster.sh
$ sudo chmod +x python-producer.sh
$ sudo chmod +x python-consumer.sh
````
Run <i>python-producer.sh</i> and <i>python-consumer.sh</i> in different windows. You can stop them using Ctrl+C.
````
$ ./run-kafka-cluster.sh
$ ./run-cassandra-cluster.sh
$ ./python-producer.sh
$ ./python-consumer.sh
$ ./shutdown-cluster.sh
$ ./shutdown-cassandra-cluster.sh
$ docker network rm dulher-kafka-cassandra-network
````
