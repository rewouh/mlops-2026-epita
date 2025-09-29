from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=['nowledgeable.com:9092'])

future = producer.send('exo1', b'coucou Pierre')
