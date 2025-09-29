from kafka import KafkaConsumer

consumer = KafkaConsumer('exo1', bootstrap_servers=['nowledgeable.com:9092'])

for message in consumer:
    print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition, message.offset, message.key, message.value))
    
