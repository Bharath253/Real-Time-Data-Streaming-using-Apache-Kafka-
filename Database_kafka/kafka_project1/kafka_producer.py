from confluent_kafka import Producer
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.json_schema import JSONSerializer
import config
import schema_registry


def init_kafka_producer():
    return Producer(config.sasl_conf())

def produce_message(producer, topic, key, value):
    schema_registry_client = SchemaRegistryClient(schema_registry.schema_config())
    my_schema = schema_registry_client.get_latest_version(f"{topic}-value").schema.schema_str
    string_serializer = StringSerializer('utf_8')
    json_serializer = JSONSerializer(my_schema, schema_registry_client)

    try:
        producer.produce(
            topic=topic,
            key=string_serializer(key, value),
            value=json_serializer(value, SerializationContext(topic, MessageField.VALUE)),
            on_delivery=config.delivery_report
        )
        producer.flush()
    except ValueError as e:
        print(f"Kafka ValueError: {e}")
