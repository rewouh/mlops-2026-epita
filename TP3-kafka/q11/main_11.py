from kafka import KafkaConsumer, KafkaProducer
import joblib
import json

consumer = KafkaConsumer('pb', group_id='hiya', bootstrap_servers=['nowledgeable.com:9092'], value_deserializer=lambda m: json.loads(m.decode('utf8')))
producer = KafkaProducer(bootstrap_servers=['nowledgeable.com:9092'], value_serializer=lambda m: json.dumps(m).encode('utf8'))

model = joblib.load("./regression.joblib")

for message in consumer:
    mv = message.value
    result = model.predict([[mv['size'], mv['nb_rooms'], mv['garden']]])[0]
    print(f'result is {result}')
    future = producer.send('prediction_pierre', { 'y_pred' : result})
    producer.flush()

