from kafka import KafkaProducer

import csv
import datetime
import json
import random
import time


class KafkaTransactionsWriter:
    def __init__(self, kafka_host, topic_name, tweets_file):
        self.producer = KafkaProducer(bootstrap_servers=kafka_host,
                                      value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        self.topic = topic_name
        self.file = open(tweets_file, 'r')
        self.tweets = csv.reader(self.file)
        self.header = next(self.tweets)

    def write_tweets(self):
        k = 0
        while True:
            start_time = time.time()
            data = next(self.tweets)
            transaction = {}
            for i in range(len(self.header)):
                transaction[self.header[i]] = data[i]
            random_number_of_days = random.randrange(30)
            transaction_date = datetime.date.today() - datetime.timedelta(days=random_number_of_days)
            transaction['transaction_date'] = transaction_date.strftime("%Y-%m-%d")
            self.producer.send(self.topic, transaction)
            k += 1
            if k == 20:
                time.sleep(start_time + 1 - time.time())
                k = 0

    def __del__(self):
        self.file.close()


def main():
    kafka_host_name = "kafka-server:9092"
    topic_name = "transactions"
    file_name = "/opt/app/PS_20174392719_1491204439457_log.csv"
    kafka_tweets = KafkaTransactionsWriter(kafka_host_name, topic_name, file_name)
    kafka_tweets.write_tweets()


if __name__ == "__main__":
    main()
