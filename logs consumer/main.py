from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_extract, col, to_timestamp, when, window
from pyspark.sql.types import StringType, IntegerType, LongType

def create_spark_session(app_name = "KafkaLogAnalysis"):
    spark = SparkSession.builder \
        .appName(app_name) \
        .config("spark.sql.legacy.timeParserPolicy", "LEGACY") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
        .getOrCreate()
        
    return spark

def read_kafka_stream(spark, bootstrap_servers, topic, starting_offsets = "earliest"):
    return spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", bootstrap_servers) \
        .option("subscribe", topic) \
        .option("startingOffsets", starting_offsets) \
        .load()

def parse_log_data(raw_df):
    return raw_df.select(
        regexp_extract(col("value"), r"^(\S+)", 1).alias("ip").cast(StringType()),
        regexp_extract(col("value"), r"- (\d{3}) \[", 1).cast(IntegerType()).alias("user_id"),
        regexp_extract(col("value"), r"\[(.*?)\]", 1).alias("timestamp"), 
        regexp_extract(col("value"), r"\] (\S+)", 1).alias("request_method").cast(StringType()),
        regexp_extract(col("value"), r"\] \S+ (\S+)", 1).alias("requested_resource").cast(StringType()),
        regexp_extract(col("value"), r" (\d{3}) \d+$", 1).cast(IntegerType()).alias("response_status_code"),
        regexp_extract(col("value"), r" (\d+)$", 1).cast(LongType()).alias("file_size")
    ).withColumn("timestamp", to_timestamp("timestamp", "EEE, dd MMM yyyy HH:mm:ss z"))

def add_response_type(parsed_df):
    return parsed_df.withColumn(
        "response_type",
        when(col("response_status_code") == 200, "successful").otherwise("failed")   
    )

def calculate_stats(processed_df, window_duration = "5 minute", watermark_duration = "10 minute"):
    return processed_df \
        .withWatermark("timestamp", watermark_duration) \
        .groupby("request_method", "response_type", window("timestamp", window_duration)) \
        .count()

def write_streaming_output(stats_df, output_path, checkpoint_path, output_mode = "append", output_format = "parquet"):
    return stats_df.writeStream \
        .outputMode(output_mode) \
        .format(output_format) \
        .option("path", output_path) \
        .option("checkpointLocation", checkpoint_path) \
        .start()

def main():
    spark = create_spark_session()
    
    kafka_df = read_kafka_stream(
        spark,
        bootstrap_servers="kafka1:19092,kafka2:29092,kafka3:39092",
        topic="test-topic3"
    )
    
    parsed_df = parse_log_data(kafka_df)
    response_df = add_response_type(parsed_df)
    stats_df = calculate_stats(response_df)
    
    query = write_streaming_output(
        stats_df,
        output_path="hdfs://NameNode:8020/user/spark/log_stats",
        checkpoint_path="hdfs://NameNode:8020/user/spark/checkpoint"
    )
    
    query.awaitTermination()

if __name__ == "__main__":
    main()