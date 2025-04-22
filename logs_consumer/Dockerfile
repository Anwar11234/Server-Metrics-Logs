FROM bitnami/spark:3.5

WORKDIR /app

COPY main.py /app/

CMD ["spark-submit", \
    "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0", \
    "/app/main.py"]