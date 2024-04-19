import os
import json
import boto3
from confluent_kafka import Producer
from chalicelib.dbConnections import getDgDbConnection

bootstrap_servers = os.getenv('bootstrap_servers')
sasl_username = os.getenv('sasl_username')
sasl_password = os.getenv('sasl_password')
kafkaTopic = os.getenv('GODREJ_TOPIC')

ERROR_LOGS_ENABLE = True
ERROR_EMAIL_ENABLE = False


def writeToKafka(message):
    conf = {
        'bootstrap.servers': bootstrap_servers,
        'sasl.username': sasl_username,
        'sasl.password': sasl_password,
        'security.protocol': 'SASL_SSL',
        'sasl.mechanism': 'SCRAM-SHA-512'
    }

    producer = Producer(conf)

    message = json.dumps(message).encode()
    producer.produce(kafkaTopic, value = message)
    producer.flush()
    
    if ERROR_LOGS_ENABLE:
        print ("Message {} push to kafka {}".format(message,kafkaTopic))

