import argparse
import datetime
import time
import config
import schema_registry
from confluent_kafka import Consumer
from confluent_kafka.serialization import SerializationContext, MessageField
from confluent_kafka.schema_registry.json_schema import JSONDeserializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from db_operations import insert_bid_record

def main(topic):
    # Kafka consumer configuration
    consumer_conf = config.consumer_conf()
    consumer = Consumer(consumer_conf)
    consumer.subscribe([topic])

    # Deserializer for the message based on the schema
    json_deserializer = schema_registry.create_deserializer(topic)

    # Database configuration details
    db_config = {
        'host': config.DB_HOST,
        'user': config.DB_USER,
        'passwd': config.DB_PASSWORD,
        'database': config.DB_NAME
    }

    counter = 0
    try:
        while True:
            # Polling for messages
            msg = consumer.poll(1.0)
            if msg is None:  # If no message, continue polling
                continue

            # Deserialize the message
            bid = json_deserializer(msg.value(), SerializationContext(msg.topic(), MessageField.VALUE))
            if bid is not None:
                counter += 1
                name = bid['name']
                price = bid['price']
                bid_ts = bid['bid_ts']

                # Start timing the database insertion
                start_time = time.time()

                # Insert the bid record into the database
                if insert_bid_record(db_config, name, price, bid_ts) is not None:
                    # Calculate and print the time taken for the insertion
                    time_taken = time.time() - start_time
                    print(f"{counter} record(s) successfully added in {time_taken:.4f} seconds")

                    # Additional prints or logic can be added here...

    except KeyboardInterrupt:
        # Handle script interruption
        print("Consumer closed")
    finally:
        # Always close the consumer
        consumer.close()

if __name__ == '__main__':
    # Starting point of the script
    main("bidding")



