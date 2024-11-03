from kafka import KafkaProducer
import time
import json
import random

# Inisialisasi producer Kafka
producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

sensor_ids = ['S1', 'S2', 'S3']  # ID sensor

while True:
    # Simulasi suhu acak antara 60°C dan 100°C
    for sensor_id in sensor_ids:
        temperature = random.randint(60, 100)
        data = {
            'sensor_id': sensor_id,
            'temperature': temperature
        }
        
        # Kirim data ke topik
        producer.send('sensor-suhu', value=data)
        print(f'Sent: {data}')
        
    time.sleep(1)  # Kirim setiap detik
