from kafka import KafkaProducer, KafkaConsumer
import json
import numpy as np

consumer = KafkaConsumer('pb', bootstrap_servers=['nowledgeable.com:9092'], value_deserializer=lambda m: json.loads(m.decode('utf8')))
producer = KafkaProducer(bootstrap_servers=['nowledgeable.com:9092'], value_serializer=lambda m: json.dumps(m).encode('utf8'))

for message in consumer:
    print(f'Received : {message.value}')
    producer.send('processed', { 'result': int(np.sum(np.array(message.value['data']))) })
