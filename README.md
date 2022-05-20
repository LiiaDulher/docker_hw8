# Docker hw8
Kafka-Cassandra

## Team: [Liia_Dulher](https://github.com/LiiaDulher)

### API 
<b>API_description.txt</b> contains description of API.

### Important
It takes about 65 seconds for Cassandra node to start, so <i>run-cassandra.sh</i> will start node about <b>1 minute</b>.

### Prerequiments
Please put file <b>PS_20174392719_1491204439457_log.csv</b> in this directory.<br>

### Usage
````
$ sudo chmod +x run-kafka-cluster.sh
$ sudo chmod +x run-cassandra-cluster.sh
$ sudo chmod +x shutdown-cassandra-cluster.sh
$ sudo chmod +x shutdown-cluster.sh
$ sudo chmod +x python-producer.sh
$ sudo chmod +x python-consumer.sh
$ sudo chmod +x cassandra-app.sh
$ sudo chmod +x shutdown-app.sh
````
Run <i>python-producer.sh</i> and <i>python-consumer.sh</i> in different windows. You can stop them using Ctrl+C.
````
$ ./run-kafka-cluster.sh
$ ./run-cassandra-cluster.sh
$ ./python-producer.sh
$ ./python-consumer.sh
$ ./shutdown-cluster.sh
````
Run app:
````
$ ./cassandra-app.sh
# use given client or any other program
$ ./shutdown-app.sh
````
Client usage:
````
pip install requests
python3 client.py
````
In the end:
````
$ ./shutdown-cassandra-cluster.sh
$ docker network rm dulher-kafka-cassandra-network
````

### Results
All files with results are in <i>results</i> directory.
