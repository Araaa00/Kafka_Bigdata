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
