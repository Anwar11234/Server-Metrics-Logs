from kafka import KafkaConsumer
from database_config import Session
from schema import SystemMetrics
import logging

def parse_message(message_value):
    metrics = {}
    parts = message_value.decode('utf-8').split(',')
    for part in parts:
        key, value = part.split(':')
        metrics[key.strip()] = value.strip()
    return metrics

def write_to_database(metrics_data):
    session = Session()
    try:
        metrics = SystemMetrics(
            server_id=metrics_data['id'],
            cpu=metrics_data['cpu'],
            mem=metrics_data['mem'],
            disk=metrics_data['disk']
        )
        session.add(metrics)
        session.commit()
        logging.info(f"Successfully wrote metrics to database: {metrics_data}")
    except Exception as e:
        session.rollback()
        logging.error(f"Error writing to database: {e}")
    finally:
        session.close()

def main():
    logging.basicConfig(
        level=logging.INFO,  
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    consumer = KafkaConsumer(
                'test-topic4',
                auto_offset_reset='earliest',
                group_id='metrics-group',
                bootstrap_servers=['localhost:9092','localhost:9093','localhost:9094']
            )
    
    for message in consumer:    
        try:
            metrics_data = parse_message(message.value)
            print(message.partition)
            write_to_database(metrics_data)
        except Exception as e:
            logging.error(f"Error processing message: {e}")

if __name__ == "__main__":
    main()