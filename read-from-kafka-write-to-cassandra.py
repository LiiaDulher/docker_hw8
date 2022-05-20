from cassandra.cluster import Cluster
from kafka import KafkaConsumer, TopicPartition

import json
import uuid


class CassandraClient:
    def __init__(self, host, port, keyspace):
        self.host = host
        self.port = port
        self.keyspace = keyspace
        self.session = None

    def connect(self):
        cluster = Cluster([self.host], port=self.port)
        self.session = cluster.connect(self.keyspace)

    def execute(self, query):
        self.session.execute(query)

    def close(self):
        self.session.shutdown()

    def write_data(self, step, transaction_type, amount, name_orig, old_balance_org, new_balance_orig, name_dest,
                       old_balance_dest, new_balance_dest, is_fraud, transaction_date):
        is_fraud = 'true' if is_fraud == '1' else 'false'
        query1 = "INSERT INTO transactions (transaction_id, step, type, amount, nameOrig, oldbalanceOrg," \
                 " newbalanceOrig, nameDest, oldbalanceDest, newbalanceDest, isFraud, transaction_date )" \
                 " VALUES (%s, %s, '%s', %s, '%s', %s, %s, '%s', %s, %s, %s, '%s')" % (uuid.uuid1(), step,
                                                                                       transaction_type, amount,
                                                                                       name_orig, old_balance_org,
                                                                                       new_balance_orig, name_dest,
                                                                                       old_balance_dest,
                                                                                       new_balance_dest,
                                                                                       is_fraud, transaction_date)
        query2 = "INSERT INTO amount_only_transactions (transaction_id, amount, nameDest, transaction_date)" \
                 " VALUES (%s, %s, '%s', '%s')" % (uuid.uuid1(), amount, name_dest, transaction_date)
        self.execute(query1)
        self.execute(query2)


class KafkaTransactionsReader:
    def __init__(self, kafka_host, topic_name, cassandra_host, cassandra_port, keyspace):
        self.consumer = KafkaConsumer(bootstrap_servers=kafka_host)
        self.consumer.assign([TopicPartition(topic_name, 1), TopicPartition(topic_name, 2),
                              TopicPartition(topic_name, 3)])

        self.client = CassandraClient(cassandra_host, cassandra_port, keyspace)
        self.client.connect()

    def read_transactions(self):
        while True:
            msg = next(self.consumer)
            value = msg.value.decode('utf-8')
            json_tweet = json.loads(value)
            step = json_tweet['step']
            transaction_type = json_tweet['type']
            amount = json_tweet['amount']
            name_orig = json_tweet['nameOrig']
            old_balance_org = json_tweet['oldbalanceOrg']
            new_balance_orig = json_tweet['newbalanceOrig']
            name_dest = json_tweet['nameDest']
            old_balance_dest = json_tweet['oldbalanceDest']
            new_balance_dest = json_tweet['newbalanceDest']
            is_fraud = json_tweet['isFraud']
            transaction_date = json_tweet['transaction_date']
            self.client.write_data(step, transaction_type, amount, name_orig, old_balance_org, new_balance_orig,
                                   name_dest, old_balance_dest, new_balance_dest, is_fraud, transaction_date)

    def __del__(self):
        self.client.close()


def main():
    cassandra_host = 'cassandra-node'
    cassandra_port = 9042
    keyspace = 'transactions_dulher'
    kafka_host_name = "kafka-server:9092"
    topic_name = "transactions"
    kafka_tweets = KafkaTransactionsReader(kafka_host_name, topic_name, cassandra_host, cassandra_port, keyspace)
    kafka_tweets.read_transactions()


if __name__ == "__main__":
    main()
