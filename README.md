## 📡 Pengumpulan Data Sensor IoT dengan Apache Kafka dan PySpark

### 👥 Anggota Kelompok
| Nama                    | NRP         |
|-------------------------|-------------|
| Mutiara Nurhaliza       | 5027221010  |
| Rehana Putri Salsabilla | 5027221015  |

### 📝 Deskripsi Proyek
Proyek ini adalah simulasi pengumpulan dan pemrosesan data dari sensor suhu di mesin pabrik menggunakan Apache Kafka dan PySpark. Data dikirim secara real-time setiap detik oleh beberapa sensor yang menghasilkan data suhu acak. Kafka digunakan sebagai penghubung aliran data, sementara PySpark digunakan untuk memfilter data yang dihasilkan, khususnya mendeteksi suhu tinggi (di atas 80°C) sebagai tanda peringatan sederhana.

### 📑 Daftar Isi
1. [Persyaratan Sistem](#persyaratan-sistem)
2. [Instalasi](#instalasi)
3. [Menjalankan Kafka dan Membuat Topik](#menjalankan-kafka-dan-membuat-topik)
4. [Menjalankan Producer dan Consumer](#menjalankan-producer-dan-consumer)
5. [Struktur Kode](#struktur-kode)
6. [Catatan Tambahan](#catatan-tambahan)

---

### 💻 Persyaratan Sistem
- **Python 3.x** untuk menjalankan producer dan dependencies PySpark
- **Apache Kafka** untuk mengelola topik dan mengirim data
- **Apache Spark** untuk konsumsi dan pemrosesan data

### 🛠️ Instalasi

1. **Install Kafka**
   - Unduh Apache Kafka dari [situs resmi](https://kafka.apache.org/downloads) dan ekstrak file ZIP atau TAR.
   - Tambahkan Kafka ke `PATH` dengan menambahkan `bin` directory ke konfigurasi sistem.
   - Mulai Zookeeper dan Kafka dengan perintah:
     ```bash
     # Mulai Zookeeper
     bin/zookeeper-server-start.sh config/zookeeper.properties

     # Mulai Kafka
     bin/kafka-server-start.sh config/server.properties
     ```

2. **Install Dependencies Python**
   - Install package yang dibutuhkan, seperti `kafka-python` untuk producer dan PySpark untuk consumer.
     ```bash
     pip install kafka-python pyspark
     ```

### 🚀 Menjalankan Kafka dan Membuat Topik

1. **Buat Topik untuk Data Sensor**
   - Jalankan perintah ini untuk membuat topik bernama `sensor-suhu` di Kafka:
     ```bash
     bin/kafka-topics.sh --create --topic sensor-suhu --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
     ```

2. **Cek Topik**
   - Pastikan topik `sensor-suhu` berhasil dibuat:
     ```bash
     bin/kafka-topics.sh --list --bootstrap-server localhost:9092
     ```

### ▶️ Menjalankan Producer dan Consumer

#### Langkah 1: Menjalankan Producer
- **Kode Producer** akan mengirim data suhu acak dari tiga sensor setiap detik.
- Simpan kode berikut di file bernama `producer.py` dan jalankan.

   ```python
   from kafka import KafkaProducer
   import time
   import json
   import random

   producer = KafkaProducer(bootstrap_servers='localhost:9092',
                            value_serializer=lambda v: json.dumps(v).encode('utf-8'))

   sensor_ids = ['S1', 'S2', 'S3']

   while True:
       for sensor_id in sensor_ids:
           temperature = random.randint(60, 100)
           data = {
               'sensor_id': sensor_id,
               'temperature': temperature
           }
           producer.send('sensor-suhu', value=data)
           print(f'Sent: {data}')
       time.sleep(1)
   ```

- **Menjalankan Producer**:
   ```bash
   python producer.py
   ```

#### Langkah 2: Menjalankan Consumer
- **Kode Consumer** akan membaca data dari topik `sensor-suhu` dan menampilkan data suhu di atas 80°C sebagai peringatan.
- Simpan kode berikut di file bernama `consumer.py` dan jalankan.

   ```python
   from pyspark.sql import SparkSession
   from pyspark.sql import functions as F
   from pyspark.sql.types import StructType, StructField, StringType, IntegerType

   spark = SparkSession.builder \
       .appName("Sensor Temperature Consumer") \
       .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1") \
       .getOrCreate()

   df = spark.readStream \
       .format("kafka") \
       .option("kafka.bootstrap.servers", "localhost:9092") \
       .option("subscribe", "sensor-suhu") \
       .load()

   schema = StructType([
       StructField("sensor_id", StringType(), True),
       StructField("temperature", IntegerType(), True)
   ])

   sensor_data = df.selectExpr("CAST(value AS STRING)").select(F.from_json(F.col("value"), schema).alias("data"))
   sensor_data = sensor_data.select("data.sensor_id", "data.temperature")
   filtered_data = sensor_data.filter(sensor_data.temperature > 80)

   query = filtered_data.writeStream \
       .outputMode("append") \
       .format("console") \
       .start()

   query.awaitTermination()
   ```

- **Menjalankan Consumer**:
   ```bash
   spark-submit consumer.py
   ```

### 🗂️ Struktur Kode

- **producer.py**: Script yang mensimulasikan data suhu dari beberapa sensor dan mengirimkannya ke topik `sensor-suhu` di Kafka setiap detik.
- **consumer.py**: Script PySpark yang membaca data suhu dari topik `sensor-suhu`, memfilter suhu di atas 80°C, dan mencetak data tersebut di console.

### 📌 Catatan Tambahan
- Pastikan Kafka dan Zookeeper sudah berjalan sebelum menjalankan producer dan consumer.
- Pastikan semua dependencies sudah terpasang sesuai dengan versi yang digunakan di Spark dan Kafka.
- Kamu bisa menyesuaikan interval pengiriman dan ambang suhu di script `producer.py` jika diperlukan.

Selamat mencoba, dan semoga berhasil! 😊
