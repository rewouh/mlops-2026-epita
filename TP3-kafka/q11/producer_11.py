from kafka import KafkaProducer
import json

producer = KafkaProducer(bootstrap_servers=['nowledgeable.com:9092'], value_serializer=lambda m: json.dumps(m).encode('utf8'))

future = producer.send('pb', { 'size': 100, 'nb_rooms': 5, 'garden': False })

producer.flush()
