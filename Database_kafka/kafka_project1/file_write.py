import argparse
from confluent_kafka import Consumer
from confluent_kafka.serialization import SerializationContext, MessageField
import config
import schema_registry
import csv_operations
import time  # Importing time module to measure execution time

def main(topic):
    # Configuration for the Kafka Consumer
    consumer_conf = config.writer_conf()
    consumer = Consumer(consumer_conf)
    consumer.subscribe([topic])

    # Creating a deserializer for the message based on the schema
    json_deserializer = schema_registry.create_deserializer(topic)

    counter = 0
    try:
        start_time = time.time()  # Start time measurement
        while True:
            msg = consumer.poll(1.0)
            if msg is None:  # If no message is received, continue polling
                continue

            # Deserialize the message
            bid = json_deserializer(msg.value(), SerializationContext(msg.topic(), MessageField.VALUE))
            if bid is not None:
                counter += 1
                print(f"User record {msg.key()}: bid {bid}")
                # Writing the bid data to a CSV file
                csv_operations.write_to_csv('./output.csv', bid)
                print(f'Total messages fetched till now: {counter}')
    except KeyboardInterrupt:
        # Handling interruption gracefully
        print("Consumer closed")
    finally:
        # Always close the consumer in the end
        consumer.close()
        end_time = time.time()  # End time of the execution
        print(f"Execution Time: {end_time - start_time} seconds")  # Printing the total execution time

if __name__ == '__main__':
    # The script starts execution here and takes the topic as an argument
    main("bidding")
