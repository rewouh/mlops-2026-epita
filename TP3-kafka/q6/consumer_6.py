from kafka import KafkaConsumer
import json
import numpy as np

consumer = KafkaConsumer('exo6', bootstrap_servers=['nowledgeable.com:9092'], value_deserializer=lambda m: json.loads(m.decode('utf8')))

for message in consumer:
    print(np.sum(np.array(message.value['data'])))
    
