from kafka import KafkaProducer
import json

producer = KafkaProducer(bootstrap_servers=['nowledgeable.com:9092'], value_serializer=lambda m: json.dumps(m).encode('utf8'))

future = producer.send('pb', { 'data': [[1, 2,], [3, 4]] })
